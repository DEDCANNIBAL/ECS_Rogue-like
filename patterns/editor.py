from functools import partial
from operator import attrgetter
from typing import List, Optional

import pyglet
from pyglet import gl
import imgui
from imgui.integrations.pyglet import PygletRenderer

import widgets
import components as _components
from patterns import EntityPattern, ComponentPattern


def main():

    window = pyglet.window.Window(width=1280, height=720, resizable=True)
    gl.glClearColor(1, 1, 1, 1)
    imgui.create_context()
    impl = PygletRenderer(window)
    pyglet.resource.path.append('resources')

    components = [component for name in dir(_components) if type(component := getattr(_components, name)) is type]

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
                    widgets.ForeignKey(choices=components, name_func=attrgetter('__name__')),
                    description='Choose component'
                )]
            ),
            callback=lambda form: patterns_manager.current_components_manager.add_component_from_form(form),
        ),
    )

    def update(dt):
        imgui.new_frame()

        imgui.begin('Patterns')
        add_pattern_button.gui()
        patterns_manager.gui()
        imgui.end()

        if patterns_manager.current_components_manager is not None:
            imgui.begin('Components')
            add_component_button.gui()
            patterns_manager.current_components_manager.gui()
            imgui.end()

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

    def add_pattern_from_form(self, form):
        self.add_pattern(self.make_pattern_from_form(form))

    def make_pattern_from_form(self, form):
        name = form['name']
        return EntityPattern(name=name)

    def add_pattern(self, pattern):
        self.patterns.append(pattern)
        self.set_current_components_manager(ComponentsManager())
        self.components_managers.append(self.current_components_manager)
        self.widget.add_item(widgets.Button(
            pattern.name,
            callback=partial(self.set_current_components_manager, self.current_components_manager)
        ))

    def set_current_components_manager(self, components_manager):
        self.current_components_manager = components_manager

    def delete_pattern(self, pattern):
        self.patterns.remove(pattern)

    def gui(self):
        self.widget.gui()


class ComponentsManager:
    def __init__(self):
        self.components = []
        self.forms: List[widgets.Form] = []
        self.widget = widgets.List(
            items=self.forms,
        )

    def gui(self):
        self.widget.gui()

    def add_component_from_form(self, form):
        self.add_component(self.make_component_from_form(form))

    def make_component_from_form(self, form):
        component = form['component']
        return ComponentPattern(component)

    def add_component(self, pattern: ComponentPattern):
        self.components.append(pattern)
        self.widget.add_item(widgets.ObjectForm(pattern.component))


if __name__ == "__main__":
    main()
