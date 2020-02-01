import inspect
from contextlib import nullcontext
from copy import copy
from dataclasses import dataclass
from enum import Enum
from functools import partial
from operator import attrgetter
from typing import List, Union, Any, Callable, Dict, Tuple

import imgui

from widgets.base import Widget
from widgets.utils import indent


class ForeignKey:
    def __init__(self, choices: list, name_func: Callable[[Any], str] = str):
        self.choices = choices
        self.names: List[str] = []
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
    def __init__(self,
                 fields: List[FormField],
                 name: str = '',
                 on_change=lambda key, value: None):
        self.name = name
        self.form_fields = fields
        self.fields: Dict[str, Tuple[Any, Callable, str]] = {}
        self.on_change = on_change
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
            self.on_change(field.key, default)

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
            subform = ObjectForm(
                field.type,
                name=self.name + '.' + field.key,
            )
            return subform.input

    def gui(self):
        if self.name:
            imgui.text(self.name)
            context = indent(20)
        else:
            context = nullcontext()
        with context:
            any_changed = False
            for key, (current, input_func, description) in self.fields.items():
                changed, current = input_func(description, current)
                if changed:
                    any_changed = True
                    self.on_change(key, current)
                self.fields[key][0] = current
            return any_changed

    @property
    def context(self):
        return {key: value for key, (value, _, _) in self.fields.items()}


class ObjectForm(Form):
    def __init__(self, cls, name: str = '', defaults=None, *args, **kwargs):
        fields = self.extract_fields(cls, defaults)
        if not isinstance(cls, type):
            cls = type(cls)
        if not name:
            name = cls.__name__
        self.cls = cls
        super().__init__(fields, name, *args, **kwargs)

    @staticmethod
    def extract_fields(cls, defaults):
        fields: List[FormField] = getattr(cls, '__form_fields__', None)
        if fields is not None:
            if defaults is None:
                return fields
            fields = copy(fields)
            for field in fields:
                field.default = defaults.get(field.key, field.default)
            return fields

        obj = cls() if isinstance(cls, type) else cls
        fields = [FormField(key, type(default), default=defaults.get(key, default))
                  for key, default in inspect.getmembers(obj)
                  if not key.startswith('__')]

        return fields

    @property
    def object(self):
        return self.cls(**self.context)

    def input(self, label, value):
        changed = self.gui()
        return changed, self.object
