import settings
from components import Position
from ecs import System


class MakeOrderSystem(System):
    def process(self, dt=0):
        for click_position in self.pubsub.mouse_clicks:
            self.pubsub.move_orders.append(tile_from_click(click_position))


def tile_from_click(click: Position):
    return click // settings.TILE_SIZE
