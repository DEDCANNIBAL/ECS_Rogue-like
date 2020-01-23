from components import Position, Goal, GoalType, Action, ActionType
from systems import MakeActionSystem
from .base import TestSystem


class TestMakeActionSystem(TestSystem):
    system = MakeActionSystem

    def test_vertical_move(self):
        self.check_delta(
            current_position=Position(0, 0),
            goal_position=Position(2, 0),
            expected_delta=Position(1, 0),
        )

    def test_horizontal_move(self):
        self.check_delta(
            current_position=Position(1, 0),
            goal_position=Position(-1, 0),
            expected_delta=Position(-1, 0),
        )

    def test_none_move(self):
        entity = self.make_entity(
            current_position=Position(0, 0),
            goal_position=Position(0, 0),
        )
        self.system.process()
        self.assertIsNone(self.registry.get(entity, Action))

    def check_delta(self, current_position, goal_position, expected_delta):
        entity = self.make_entity(current_position, goal_position)
        self.system.process()
        action = self.registry.get(entity, Action)
        self.assertEqual(action.delta, expected_delta)
        self.assertEqual(action.type, ActionType.MOVE)

    def make_entity(self, current_position, goal_position):
        entity = self.registry.create(
            Goal(GoalType.MOVE, position=goal_position),
            current_position,
        )
        return entity

