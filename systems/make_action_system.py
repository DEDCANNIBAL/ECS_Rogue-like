from typing import Deque

from components import Position, GoalType, Action, ActionType, Goal, PathInformation, Obstacle
from ecs import System
from settings import STEPS_TO_UPDATE_PATH
from utils import PathFinder
from utils.getters import get_field_size


class MakeActionSystem(System):
    def init(self):
        self.path_finder = PathFinder(get_field_size())

    def process(self, dt=0):
        for entity, pos, goal in self.registry.view(Position, Goal):
            if goal.type == GoalType.MOVE:
                self.make_move_action(entity, pos, goal)

    def make_move_action(self, entity, pos: Position, goal: Goal):
        path_information = self.registry.get(entity, PathInformation)
        if path_information.steps_from_last_update == STEPS_TO_UPDATE_PATH \
                or not path_information.path:
            path = self.find_path(pos, goal.position)
            if not path:
                self.registry.assign(entity, Action, ActionType.MOVE, delta=Position(0, 0))
                return
            path_information.path = path
        next_pos = path_information.path.pop()
        path_information.steps_from_last_update += 1
        delta = next_pos - pos
        self.registry.assign(entity, Action, ActionType.MOVE, delta=delta)

    def find_path(self, start: Position, finish: Position) -> Deque[Position]:
        obstacles = {pos for *_, pos in self.registry.view(Obstacle, Position)}
        return self.path_finder.find_path(start, finish, obstacles)
