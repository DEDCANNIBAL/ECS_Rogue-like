from dataclasses import dataclass, field

import imgui

from widgets.base import Widget


@dataclass
class List(Widget):
    name: str = 'List'
    items: list = field(default_factory=list)
    allow_removing: bool = False

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def gui(self):
        imgui.begin_child(self.name)
        for pattern in self.patterns:
            if isinstance(pattern, Widget):
                pattern.gui()
            else:
                imgui.label_text(str(pattern))
            #imgui.same_line()
        imgui.end_child()