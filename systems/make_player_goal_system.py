from components import Goal, GoalType
from ecs import System
from systems.mixins import PlayerMixin
from utils import last


class MakePlayerGoalSystem(System, PlayerMixin):
    def process(self, dt=0):
        self.make_move_goals()

    def make_move_goals(self):
        order = last(self.pubsub.move_orders)
        if order is None:
            return
        player = self.get_player_entity()
        self.registry.assign(player, Goal, GoalType.MOVE, position=order)
