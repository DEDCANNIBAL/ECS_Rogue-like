from functools import partial, singledispatchmethod  # type: ignore
from typing import List

import widgets
from patterns import EntityPattern, ComponentPattern


class ComponentsManager:
    def __init__(self, entity_pattern: EntityPattern):
        self.entity_pattern = entity_pattern
        self.components = entity_pattern.component_patterns
        self.forms: List[widgets.Form] = []
        self.widget = widgets.List(
            items=self.forms,
            on_remove=self.delete_component,
        )
        self.load()
        self.save()

    def load(self):
        for component in self.entity_pattern.component_patterns:
            self.add_button_for_component(component)

    def gui(self):
        self.widget.gui()

    def add_component_from_form(self, form):
        self.add_component(self.make_component_from_form(form))

    def make_component_from_form(self, form):
        component = form['component']
        return ComponentPattern(component)

    def add_component(self, pattern: ComponentPattern):
        self.entity_pattern.component_patterns.append(pattern)
        self.add_button_for_component(pattern)
        self.save()

    def add_button_for_component(self, pattern: ComponentPattern):
        self.widget.add_item(widgets.ObjectForm(
            pattern.component,
            defaults=pattern.kwargs,
            on_change=partial(self.update_component_field, pattern),
        ))

    @singledispatchmethod
    def delete_component(self, pattern: ComponentPattern):
        self.entity_pattern.component_patterns.remove(pattern)
        self.save()

    @delete_component.register
    def _(self, index: int):
        self.delete_component(self.components[index])

    def update_component_field(self, pattern, key, value):
        pattern.kwargs[key] = value
        self.save()

    def save(self):
        self.entity_pattern.save()
