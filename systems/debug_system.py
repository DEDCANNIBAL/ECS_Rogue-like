from components import Position
from ecs import System
from systems.mixins import PlayerMixin


class DebugSystem(System, PlayerMixin):
    def process(self, dt):
        player = self.get_player_entity()
        print(self.registry.get(player, Position))
