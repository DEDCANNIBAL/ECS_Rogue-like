import pyglet
from pyglet import gl

import imgui
from imgui.integrations.pyglet import PygletRenderer

from patterns import Pattern


def main():

    window = pyglet.window.Window(width=1280, height=720, resizable=True)
    gl.glClearColor(1, 1, 1, 1)
    imgui.create_context()
    impl = PygletRenderer(window)
    patterns = PatternsManager()

    def update(dt):
        imgui.new_frame()

        imgui.begin('Patterns')

        if imgui.button('Add pattern'):
            imgui.open_popup("add-pattern")
        if imgui.begin_popup('add-pattern'):
            form = AddPatternForm.enter()
            if form is not None:
                imgui.close_current_popup()
                patterns.add_pattern_from_form(form)
            imgui.end_popup()

        patterns.list()

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

    def add_pattern_from_form(self, form):
        self.add_pattern(self.make_pattern_from_form(form))

    def make_pattern_from_form(self, form):
        name = form
        return Pattern(name=name)

    def add_pattern(self, pattern):
        self.patterns.append(pattern)

    def list(self):
        imgui.begin_child('patterns')
        for pattern in self.patterns:
            imgui.button(pattern.name)
        imgui.end_child()


class AddPatternForm:
    name = ''

    @classmethod
    def enter(cls):
        changed, cls.name = imgui.input_text('Enter pattern name', cls.name, 256)
        if imgui.button('Add pattern'):
            name = cls.name
            cls.name = ''
            return name
        return None

if __name__ == "__main__":
    main()
