import settings
from components import Position
from systems import MakeOrderSystem
from .base import TestSystem


class TestMakeOrderSystem(TestSystem):
    system = MakeOrderSystem

    def test_procces_makes_order(self):
        self.pubsub.mouse_clicks.append(Position(settings.TILE_SIZE * 2, settings.TILE_SIZE + 1))
        self.system.process()
        self.assertEqual(next(self.pubsub_view.move_orders), Position(2, 1))
