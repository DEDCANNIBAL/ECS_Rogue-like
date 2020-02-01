import patterns
from ecs import System


class ManagePlayerSystem(System):
    def init(self):
        player_pattern = patterns.load('player')
        self.player_entity = player_pattern.spawn(self.registry)
