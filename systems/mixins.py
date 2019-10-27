from components import Player


class PlayerMixin:
    def get_player_entity(self):
        player_entity, _ = next(self.registry.view(Player))
        return player_entity
