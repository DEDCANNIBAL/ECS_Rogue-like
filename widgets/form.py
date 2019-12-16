import inspect
from dataclasses import dataclass
from enum import Enum
from functools import partial
from operator import attrgetter
from typing import List, Union, Any, Callable

import imgui

from widgets.base import Widget


class ForeignKey:
    def __init__(self, choices: list, name_func: Callable[[Any], str]=str):
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


class EnumKey(ForeignKey):
    def __init__(self, enum):
        members = [value for _, value in enum.__members__.items()]
        super().__init__(members, name_func=attrgetter('name'))


@dataclass
class FormField:
    key: str
    type: Union[type, ForeignKey]
    description: str = ''
    default: Any = None


class Form(Widget):
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
            if self.name:
                description = self.name + '.' + description
            self.fields[field.key] = [default, input_func, description]

    def get_input_func(self, field: FormField):
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
        elif field.type.__base__ is Enum:
            return EnumKey(field.type).input
        else:
            subform = ObjectForm(field.type, name=self.name + '.' + field.key)
            return subform.input

    def gui(self):
        if self.name:
            imgui.text(self.name)
            imgui.indent(20)
        for key, (current, input_func, description) in self.fields.items():
            changed, current = input_func(description, current)
            self.fields[key][0] = current
        if self.name:
            imgui.unindent(20)

    def input(self, label, value):
        self.gui()
        return False, None

    @property
    def context(self):
        return {key: value for key, (value, _, _) in self.fields.items()}


class ObjectForm(Form):
    def __init__(self, cls, name: str = ''):
        fields = [FormField(key, type(default), default=default)
                  for key, default in inspect.getmembers(cls()) if not key.startswith('__')]
        if not name:
            name = cls.__name__
        super().__init__(fields, name)
