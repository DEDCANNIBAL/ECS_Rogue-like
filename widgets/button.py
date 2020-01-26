from dataclasses import dataclass
from typing import Callable

import imgui
import pyglet

from widgets.base import Widget
from widgets.popup import Popup


@dataclass
class Button(Widget):
    name: str = 'Button'
    callback: Callable = lambda: None

    def gui(self):
        if imgui.button(self.name):
            self.callback()


@dataclass
class ButtonWithPopup(Widget):
    popup: Popup
    callback: Callable = lambda: None

    def gui(self):
        if imgui.button(self.name):
            self.callback()
            self.popup.open()
        self.popup.gui()


class ImageButton(Button):
    def __init__(self, texture: pyglet.image.Texture, callback=lambda: None, width=15, height=15):
        self.callback = callback
        self.width = width
        self.height = height
        self.texture = texture

    def gui(self):
        if imgui.image_button(self.texture.id, self.width, self.height):
            self.callback()
