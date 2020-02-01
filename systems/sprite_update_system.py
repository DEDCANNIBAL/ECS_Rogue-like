from components import Position, Sprite
from ecs import System
from settings import TILE_SIZE


class UpdateSpriteSystem(System):
    def process(self, dt=0):
        for entity, pos, sprite in self.registry.view(Position, Sprite):
            sprite.x = pos.x * TILE_SIZE
            sprite.y = pos.y * TILE_SIZE
