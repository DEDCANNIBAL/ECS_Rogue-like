import ecs

from tests.ecs_tests.components import Health, Point

N = 10000


def create(registry):
    for i in range(N):
        entity = registry.create()
        registry.assign(entity, Point(3, 4))
        registry.assign(entity, Health)

    for i in range(N):
        entity = registry.create()
        registry.assign(entity, Point(3, 4))

    for i in range(N * 4):
        registry.create(Health)

    for i in range(N):
        registry.create(Point(3, 4), Health)


def view(registry):
    for entity, pos in registry.view(Point):
        pass

    for entity, pos, hp in registry.view(Point, Health):
        pass


def get(registry):
    for i in range(1, N * 2):
        entity = registry.create(Health)
        registry.get(entity, Health)
        entity = registry.create(Health, Point)
        registry.get(entity, Health, Point)


def make_world():
    return ecs.Registry()