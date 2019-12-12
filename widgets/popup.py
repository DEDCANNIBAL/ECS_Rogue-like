from dataclasses import dataclass
from typing import Callable, Any

import imgui

from widgets.base import Widget
from widgets.form import Form


@dataclass
class Popup(Widget):
    callback: Callable[[], Any]

    def open(self):
        imgui.open_popup(self.name)

    def gui(self):
        if imgui.begin_popup(self.name):
            imgui.label_text(self.name, self.name)
            if imgui.button('Ok'):
                self.callback()
                imgui.close_current_popup()
                imgui.end_popup()


@dataclass
class FormPopup(Popup):
    form: Form
    callback: Callable[[dict], Any]

    def gui(self):
        if imgui.begin_popup(self.name):
            self.form.gui()
            if imgui.button(self.name):
                self.callback(self.form.context)
                imgui.close_current_popup()
                self.form.init()
            imgui.end_popup()
