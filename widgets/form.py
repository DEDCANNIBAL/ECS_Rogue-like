from dataclasses import dataclass
from functools import partial
from typing import List, Union, Any

import imgui

from widgets.base import Widget


@dataclass
class ForeignKey:
    def __init__(self, choices: list, name_func=str):
        self.choices = choices
        self.names = []
        self.name_func = name_func
        self.update_names()

    def update_names(self):
        if len(self.names) != len(self.choices):
            self.names = [self.name_func(choice) for choice in self.choices]

    def __call__(self, *args, **kwargs):
        return self.choices[0]

    def input(self, description, current):
        index = self.choices.index(current)
        changed, index = imgui.listbox(description, index, self.names)
        return changed, self.choices[index]


@dataclass
class FormField:
    key: str
    type: Union[type, ForeignKey]
    description: str = ''
    default: Any = None


@dataclass
class Form(Widget):
    name: str = ''

    def __init__(self, fields: List[FormField], name: str = ''):
        self.name = name
        self.form_fields = fields
        self.fields = {}
        self.init()

    def init(self):
        self.fields = {}
        for field in self.form_fields:
            default = field.type() if field.default is None else field.default
            input_func = self.get_input_func(field)
            description = field.description or field.key
            self.fields[field.key] = [default, input_func, description]

    @staticmethod
    def get_input_func(field: FormField):
        if field.type is str:
            return partial(imgui.input_text, buffer_length=256)
        elif field.type is int:
            return imgui.input_int
        elif field.type is float:
            return imgui.input_float
        elif field.type is bool:
            return imgui.checkbox
        elif isinstance(field.type, ForeignKey):
            return field.type.input
        else:
            raise NotImplementedError

    def gui(self):
        if self.name:
            imgui.text(self.name)
        for key, (current, input_func, description) in self.fields.items():
            changed, current = input_func(description, current)
            self.fields[key][0] = current

    @property
    def context(self):
        return {key: value for key, (value, _, _) in self.fields.items()}
