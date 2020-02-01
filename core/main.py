import imgui
import pyglet
from imgui.integrations.pyglet import PygletRenderer
from pyglet import gl

import systems
from components import Position
from components.sprite import batch
from ecs import SystemManager, Registry, PubSub


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

    def clear_pubsub(dt):
        pubsub.clear()
    pyglet.clock.schedule_interval(clear_pubsub, 0.033)

    def update_ui(dt):
        imgui.new_frame()

    @window.event
    def on_draw():
        update_ui(ui_clock.update_time())

        window.clear()
        imgui.render()
        batch.draw()
        impl.render(imgui.get_draw_data())

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        pubsub.mouse_clicks.append(Position(x, y))

    pyglet.app.run()
    impl.shutdown()


def make_system_manager(pubsub, registry):
    system_manager = SystemManager(pubsub=pubsub, registry=registry)
    for system in (
        systems.ManagePlayerSystem,
        systems.MakeOrderSystem,
        systems.MakePlayerGoalSystem,
        systems.MakeActionSystem,
        systems.MakeTurnSystem,
        systems.DebugSystem,
        systems.FieldGenerationSystem,
        systems.UpdateSpriteSystem,
    ):
        system_manager.add_system(system)

    return system_manager


if __name__ == "__main__":
    main()
