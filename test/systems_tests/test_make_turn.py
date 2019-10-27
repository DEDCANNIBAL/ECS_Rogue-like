from unittest.mock import MagicMock

from components import Actable
from systems import MakeTurnSystem
from .base import TestSystem


class TestMakeTurnSystem(TestSystem):
    system = MakeTurnSystem

    def test_one_turn_without_player(self):
        self.system.non_player_turn = MagicMock()
        entity1 = self.registry.create(Actable)
        entity2 = self.registry.create(Actable)
        self.system.process(1)
        self.assertFalse(self.registry.get(entity1, Actable).acted)
        self.assertFalse(self.registry.get(entity2, Actable).acted)

    def test_one_turn_with_player(self):
        self.system.non_player_turn = MagicMock()
        for player_acted in False, True:
            self.system.player_turn = MagicMock(return_value=player_acted)
            entity1 = self.registry.create(Actable)
            player = self.registry.create(Actable(is_player=True))
            entity2 = self.registry.create(Actable)
            self.system.process(1)
            self.assertIs(self.registry.get(entity1, Actable).acted, not player_acted)
            self.assertFalse(self.registry.get(player, Actable).acted)
            self.assertFalse(self.registry.get(entity2, Actable).acted)

    def test_event_appending(self):
        self.system.non_player_turn = MagicMock()
        entity = self.registry.create(Actable)
        turn_number = self.system.turn_number
        self.system.process(1)
        self.assertEqual(next(self.pubsub_view.unit_acted), entity)
        self.assertEqual(next(self.pubsub_view.turns), turn_number)
        self.assertEqual(self.system.turn_number, turn_number + 1)


