from components import Actable, Position, Player
from systems import ManagePlayerSystem
from .base import TestSystem


class TestManagePlayerSystem(TestSystem):
    system = ManagePlayerSystem

    def test_init_creates_player(self):
        player = self.registry.get(self.system.player_entity, Player)
        self.assertIsNotNone(player)

        actable = self.registry.get(self.system.player_entity, Actable)
        self.assertTrue(actable.is_player)

        position = self.registry.get(self.system.player_entity, Position)
        self.assertIsNotNone(position)
