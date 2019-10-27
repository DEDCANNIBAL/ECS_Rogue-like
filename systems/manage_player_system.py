from components import Actable, Position, Player
from ecs import System


class ManagePlayerSystem(System):
    def init(self):
        self.player_entity = self.registry.create(
            Actable(is_player=True),
            Player,
            Position(0, 0),
        )
