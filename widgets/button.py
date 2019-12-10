from dataclasses import dataclass
from typing import Callable

import imgui

from widgets import Widget


@dataclass
class Button(Widget):
    name: str = 'Button'
    callback: Callable = lambda: None

    def gui(self):
        if imgui.button(self.name):
            self.callback()
