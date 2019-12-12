from dataclasses import dataclass
from functools import partial
from typing import Callable, Any, List

import imgui

from widgets.base import Widget


@dataclass
class FormField:
    key: str
    type: type
    description: str = ''
    default = None


@dataclass
class Form(Widget):
    name: str = ''

    def __init__(self, fields: List[FormField], name: str = ''):
        self.name = name
        self.fields = {}
        for field in fields:
            default = field.type() if field.default is None else field.default
            input_func = self.get_input_func(field)
            description = field.description or field.key
            self.fields[field.key] = (default, input_func, description)

    @staticmethod
    def get_input_func(field: FormField):
        if isinstance(field.type, str):
            return partial(imgui.input_text, buffer_length=256)
        elif isinstance(field.type, int):
            return imgui.input_int
        elif isinstance(field.type, float):
            return imgui.input_float
        elif isinstance(field.type, ForeignKey):
            return partial(imgui.listbox, fitems=field.type.choices)

    def gui(self):
        for key, (current, input_func, description) in self.fields.items():
            current, changed = input_func(description, current)
            self.fields[key] = current

    @property
    def context(self):
        return {key: value for key, (value, _, _) in self.fields.items()}


@dataclass
class ForeignKey:
    choices: list

    def __call__(self, *args, **kwargs):
        return 0
