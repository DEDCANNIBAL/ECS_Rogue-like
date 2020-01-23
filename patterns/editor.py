from functools import partial, singledispatchmethod
from operator import attrgetter
from typing import List, Optional

import pyglet
from pyglet import gl
import imgui
from imgui.integrations.pyglet import PygletRenderer

import widgets
import components as _components
from patterns import EntityPattern, ComponentPattern, PATH_TO_PATTERNS, load


def main():

    window = pyglet.window.Window(width=1280, height=720, resizable=True)
    gl.glClearColor(1, 1, 1, 1)
    imgui.create_context()
    impl = PygletRenderer(window)
    pyglet.resource.path.append('resources')

    components = [component for name in dir(_components)
                  if type(component := getattr(_components, name)) is type]

    patterns_manager = PatternsManager()

    add_pattern_button = widgets.ButtonWithPopup(
        'Add pattern',
        popup=widgets.FormPopup(
            'Add pattern',
            form=widgets.Form(
                [widgets.FormField(
                    'name',
                    str,
                    description='Pattern name'
                )]
            ),
            callback=patterns_manager.add_pattern_from_form,
        ),
    )

    add_component_button = widgets.ButtonWithPopup(
        'Add component',
        popup=widgets.FormPopup(
            'Add component',
            form=widgets.Form(
                [widgets.FormField(
                    'component',
                    widgets.ForeignKey(
                        choices=components,
                        name_func=attrgetter('__name__')
                    ),
                    description='Choose component'
                )]
            ),
            callback=lambda form: patterns_manager.current_components_manager.add_component_from_form(form),
        ),
    )

    def entities_gui():
        imgui.begin('Patterns')
        add_pattern_button.gui()
        patterns_manager.gui()
        imgui.end()

    def components_gui():
        current_components_manager = patterns_manager.current_components_manager
        if patterns_manager.current_components_manager is not None:
            imgui.begin('Components')
            imgui.text(current_components_manager.entity_pattern.name)
            add_component_button.gui()
            current_components_manager.gui()
            imgui.end()

    def update(dt):
        imgui.new_frame()
        entities_gui()
        components_gui()


    @window.event
    def on_draw():
        update(1/60.0)
        window.clear()
        imgui.render()
        impl.render(imgui.get_draw_data())

    pyglet.app.run()
    impl.shutdown()


class PatternsManager:
    def __init__(self):
        self.patterns = []
        self.buttons: List[widgets.Button] = []
        self.widget = widgets.List(
            items=self.buttons,
            on_remove=lambda index: self.delete_pattern(self.patterns[index])
        )
        self.components_managers: List[ComponentsManager] = []
        self.current_components_manager: Optional[ComponentsManager] = None
        self.load()

    def add_pattern_from_form(self, form):
        self.add_pattern(self.make_pattern_from_form(form))

    def make_pattern_from_form(self, form):
        name = form['name']
        return EntityPattern(name=name)

    def add_pattern(self, pattern):
        self.patterns.append(pattern)
        components_manager = ComponentsManager(pattern)
        self.set_current_components_manager(components_manager)
        self.components_managers.append(components_manager)
        self.widget.add_item(widgets.Button(
            pattern.name,
            callback=partial(
                self.set_current_components_manager,
                components_manager
            )
        ))

    def load(self):
        for pattern_path in PATH_TO_PATTERNS.iterdir():
            pattern = load(pattern_path.name)
            self.add_pattern(pattern)

    def set_current_components_manager(self, components_manager):
        self.current_components_manager = components_manager

    def delete_pattern(self, pattern: EntityPattern):
        current_components_manager = self.current_components_manager
        if current_components_manager is not None and current_components_manager.entity_pattern is pattern:
            self.current_components_manager = None
        self.patterns.remove(pattern)
        pattern.delete()

    def gui(self):
        self.widget.gui()


class ComponentsManager:
    def __init__(self, entity_pattern: EntityPattern):
        self.entity_pattern = entity_pattern
        self.components = entity_pattern.component_patterns
        self.forms: List[widgets.Form] = []
        self.widget = widgets.List(
            items=self.forms,
            on_remove=self.delete_component,
        )
        self.load()
        self.save()

    def load(self):
        for component in self.entity_pattern.component_patterns:
            self.add_button_for_component(component)

    def gui(self):
        self.widget.gui()

    def add_component_from_form(self, form):
        self.add_component(self.make_component_from_form(form))

    def make_component_from_form(self, form):
        component = form['component']
        return ComponentPattern(component)

    def add_component(self, pattern: ComponentPattern):
        self.entity_pattern.component_patterns.append(pattern)
        self.add_button_for_component(pattern)

    def add_button_for_component(self, pattern: ComponentPattern):
        self.widget.add_item(widgets.ObjectForm(
            pattern.component,
            on_change=partial(self.update_component_field, pattern)
        ))

    @singledispatchmethod
    def delete_component(self, pattern: ComponentPattern):
        self.entity_pattern.component_patterns.remove(pattern)
        self.save()

    @delete_component.register
    def _(self, index: int):
        self.delete_component(self.components[index])

    def update_component_field(self, pattern, key, value):
        pattern.kwargs[key] = value
        self.save()

    def save(self):
        self.entity_pattern.save()


if __name__ == "__main__":
    main()
