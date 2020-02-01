from dataclasses import dataclass, field
from functools import partial
import typing

import imgui
import pyglet

from widgets.base import Widget
from widgets.button import ImageButton


@dataclass
class List(Widget):
    name: str = 'List'
    items: list = field(default_factory=list)
    allow_removing: bool = False
    on_remove: typing.Callable[[int], typing.Any] = lambda index: None
    remove_buttons: typing.List[ImageButton] = field(default_factory=list)

    def add_item(self, item):
        self.items.append(item)
        texture = pyglet.resource.texture('cancel.png')
        del pyglet.resource._default_loader._cached_textures['cancel.png']
        self.remove_buttons.append(ImageButton(
            texture,
            callback=partial(self._on_remove, item)
        ))

    def _on_remove(self, item):
        index = self.items.index(item)
        self.on_remove(index)
        self.remove_buttons.pop(index)
        self.items.remove(item)

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
