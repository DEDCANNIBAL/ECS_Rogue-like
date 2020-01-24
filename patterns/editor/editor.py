from operator import attrgetter

import pyglet
from pyglet import gl
import imgui
from imgui.integrations.pyglet import PygletRenderer

import widgets
import components
from patterns.editor.patterns_manager import PatternsManager


class Editor:
    def __init__(self):
        self.components = [component for name in dir(components)
                      if type(component := getattr(components, name)) is type]

        patterns_manager = PatternsManager()
        self.patterns_manager = patterns_manager

        self.add_pattern_button = widgets.ButtonWithPopup(
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

        self.add_component_button = widgets.ButtonWithPopup(
            'Add component',
            popup=widgets.FormPopup(
                'Add component',
                form=widgets.Form(
                    [widgets.FormField(
                        'component',
                        widgets.ForeignKey(
                            choices=self.components,
                            name_func=attrgetter('__name__')
                        ),
                        description='Choose component'
                    )]
                ),
                callback=lambda form: patterns_manager.current_components_manager.add_component_from_form(form),
            ),
        )

    def entities_gui(self):
        imgui.begin('Patterns')
        self.add_pattern_button.gui()
        self.patterns_manager.gui()
        imgui.end()

    def components_gui(self):
        current_components_manager = self.patterns_manager.current_components_manager
        if self.patterns_manager.current_components_manager is not None:
            imgui.begin('Components')
            imgui.text(current_components_manager.entity_pattern.name)
            self.add_component_button.gui()
            current_components_manager.gui()
            imgui.end()

    def update(self, dt):
        imgui.new_frame()
        self.entities_gui()
        self.components_gui()

def main():
    #  Initialization
    window = pyglet.window.Window(width=1280, height=720, resizable=True)
    gl.glClearColor(1, 1, 1, 1)
    imgui.create_context()
    impl = PygletRenderer(window)
    pyglet.resource.path.append('../resources')

    editor = Editor()

    @window.event
    def on_draw():
        editor.update(1/60.0)
        window.clear()
        imgui.render()
        impl.render(imgui.get_draw_data())

    pyglet.app.run()
    impl.shutdown()


if __name__ == "__main__":
    main()
