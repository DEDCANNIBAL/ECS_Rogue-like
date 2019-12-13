from dataclasses import dataclass, field
from typing import List

import imgui
import pyglet

from widgets.base import Widget
from widgets.button import ImageButton


@dataclass
class List(Widget):
    name: str = 'List'
    items: list = field(default_factory=list)
    remove_buttons: List[ImageButton] = field(default_factory=list)
    allow_removing: bool = False

    def add_item(self, item):
        self.items.append(item)
        self.remove_buttons.append(ImageButton(
            pyglet.resource.texture('cancel.png')
        ))

    def remove_item(self, item):
        self.items.remove(item)

    def gui(self):
        imgui.begin_child(self.name)
        for item, remove_button in zip(self.items, self.remove_buttons):
            if isinstance(item, Widget):
                item.gui()
            else:
                text = getattr(item, 'name', str(item))
                imgui.label_text(text, text)
            imgui.same_line()
            remove_button.gui()

        imgui.end_child()
