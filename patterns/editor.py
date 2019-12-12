from typing import List

import pyglet
from pyglet import gl
import imgui
from imgui.integrations.pyglet import PygletRenderer

import widgets
from patterns import Pattern


def main():

    window = pyglet.window.Window(width=1280, height=720, resizable=True)
    gl.glClearColor(1, 1, 1, 1)
    imgui.create_context()
    impl = PygletRenderer(window)
    pyglet.resource.path.append('resources')

    patterns = PatternsManager()

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
            callback=patterns.add_pattern_from_form,
        ),
    )

    def update(dt):
        imgui.new_frame()
        imgui.begin('Patterns')
        add_pattern_button.gui()
        patterns.gui()

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
        self.widget = widgets.List(items=self.buttons)

    def add_pattern_from_form(self, form):
        self.add_pattern(self.make_pattern_from_form(form))

    def make_pattern_from_form(self, form):
        name = form['name']
        return Pattern(name=name)

    def add_pattern(self, pattern):
        self.patterns.append(pattern)
        self.widget.add_item(widgets.Button(pattern.name))

    def delete_pattern(self, pattern):
        self.patterns.remove(pattern)

    def gui(self):
        self.widget.gui()


if __name__ == "__main__":
    main()
