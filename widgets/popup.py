from dataclasses import dataclass
from typing import Callable, Any

import imgui

from widgets.base import Widget


@dataclass
class Popup(Widget):
    name: str
    callback: Callable[[], Any] = lambda: None

    def __init__(self):
        imgui.open_popup(self.name)

    def gui(self):
        if imgui.begin_popup(self.name):
            imgui.label_text(self.name, self.name)
            if imgui.button('Ok'):
                self.callback()
                imgui.close_current_popup()
                imgui.end_popup()
