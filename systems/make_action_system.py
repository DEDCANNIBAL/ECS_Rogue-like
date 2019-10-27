from components import Position, GoalType, Action, ActionType, Goal
from ecs import System
from utils import sign


class MakeActionSystem(System):
    def process(self, dt=0):
        for entity, pos, goal in self.registry.view(Position, Goal):
            if goal.type == GoalType.MOVE:
                self.make_move_action(entity, pos, goal)

    def make_move_action(self, entity, pos, goal):
        delta = goal.position - pos
        if delta.x:
            delta = Position(sign(delta.x), 0)
        elif delta.y:
            delta = Position(0, sign(delta.y))
        else:
            return
        self.registry.assign(entity, Action, ActionType.MOVE, delta=delta)
