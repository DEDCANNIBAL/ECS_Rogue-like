from ecs import System


class DebugSystem(System):
    def process(self, dt):
        print(dt)
