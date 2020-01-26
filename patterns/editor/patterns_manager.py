from functools import partial
from typing import List, Optional

import widgets
from patterns import EntityPattern, PATH_TO_PATTERNS, load
from patterns.editor.components_manager import ComponentsManager


class PatternsManager:
    def __init__(self):
        self.patterns = []
        self.buttons: List[widgets.Button] = []
        self.widget = widgets.List(
            items=self.buttons,
            on_remove=lambda index: self.delete_pattern(self.patterns[index])
        )
        self.components_managers: List[ComponentsManager] = []
        self.current_components_manager: Optional[ComponentsManager] = None
        self.load()

    def add_pattern_from_form(self, form):
        self.add_pattern(self.make_pattern_from_form(form))

    def make_pattern_from_form(self, form):
        name = form['name']
        return EntityPattern(name=name)

    def add_pattern(self, pattern):
        self.patterns.append(pattern)
        components_manager = ComponentsManager(pattern)
        self.set_current_components_manager(components_manager)
        self.components_managers.append(components_manager)
        self.widget.add_item(widgets.Button(
            pattern.name,
            callback=partial(
                self.set_current_components_manager,
                components_manager
            )
        ))

    def load(self):
        for pattern_path in PATH_TO_PATTERNS.iterdir():
            pattern = load(pattern_path.name)
            self.add_pattern(pattern)

    def set_current_components_manager(self, components_manager):
        self.current_components_manager = components_manager

    def delete_pattern(self, pattern: EntityPattern):
        current_components_manager = self.current_components_manager
        if current_components_manager is not None and current_components_manager.entity_pattern is pattern:
            self.current_components_manager = None
        self.patterns.remove(pattern)
        pattern.delete()

    def gui(self):
        self.widget.gui()