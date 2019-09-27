import pyglet
from pyglet import gl
import imgui
from imgui.integrations.pyglet import PygletRenderer

from ecs import SystemManager, Registry, PubSub
from systems.debug_system import DebugSystem


def main():
    window = pyglet.window.Window(width=1280, height=720, resizable=True)

    gl.glClearColor(1, 1, 1, 1)
    imgui.create_context()
    impl = PygletRenderer(window)

    ui_clock = pyglet.clock.Clock()

    registry = Registry()
    pubsub = PubSub()
    system_manager = make_system_manager(pubsub=pubsub, registry=registry)
    pyglet.clock.schedule_interval(system_manager.process, 0.016)

    def update_ui(dt):
        imgui.new_frame()

    @window.event
    def on_draw():
        update_ui(ui_clock.update_time())

        window.clear()
        imgui.render()
        impl.render(imgui.get_draw_data())

    pyglet.app.run()
    impl.shutdown()


def make_system_manager(pubsub, registry):
    system_manager = SystemManager(pubsub=pubsub, registry=registry)
    system_manager.add_system(DebugSystem)
    return system_manager


if __name__ == "__main__":
    main()
