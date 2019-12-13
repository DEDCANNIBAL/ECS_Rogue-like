import pyglet
import glooey


def main():
    window = pyglet.window.Window()
    batch = pyglet.graphics.Batch()
    group = pyglet.graphics.Group()
    gui = glooey.Gui(window, batch=batch, group=group)

    hbox = glooey.HBox()
    patterns_placeholder = glooey.Placeholder()
    hbox.add(patterns_placeholder)
    gui.add(hbox)

    button = glooey.Button("Click here!")
    button.push_handlers(on_click=lambda w: print(f"{w} clicked!"))
    patterns_placeholder.add(button)

    pyglet.app.run()


if __name__ == "__main__":
    main()
