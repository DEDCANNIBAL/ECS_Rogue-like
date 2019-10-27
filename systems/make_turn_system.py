from operator import itemgetter

from components import Actable, Action, Position
from ecs import System


class MakeTurnSystem(System):
    def init(self):
        self.turn_number = 0

    def process(self, dt):
        actable_components = []
        for entity, actable in sorted(self.registry.view(Actable), key=itemgetter(0)):
            if actable.acted:
                continue
            if actable.is_player:
                if not self.player_turn(entity):
                    return
            else:
                self.non_player_turn(entity)
                actable.acted = True
            actable_components.append(actable)
            self.pubsub.unit_acted.append(entity)
        self.pubsub.turns.append(self.turn_number)
        for component in actable_components:
            component.acted = False
        self.turn_number += 1

    def non_player_turn(self, entity: int):
        action = self.registry.get(entity, Action)
        if action is None:
            return False
        position = self.registry.get(entity, Position)
        position += action.delta
        self.registry.remove(entity, Action)
        return True

    def player_turn(self, entity: int):
        return self.non_player_turn(entity)
