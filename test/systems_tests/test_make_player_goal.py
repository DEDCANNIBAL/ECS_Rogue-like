from components import Position, Goal, GoalType, Player
from systems import MakePlayerGoalSystem
from .base import TestSystem


class TestMakePlayerGoalSystem(TestSystem):
    system = MakePlayerGoalSystem

    def test_procces_makes_move_goal(self):
        pos = Position(2, 1)
        self.pubsub_view.move_orders.append(pos)

        player = self.registry.create(Player)
        self.system.process()

        self.assertEqual(
            self.registry.get(player, Goal),
            Goal(GoalType.MOVE, position=pos)
        )
