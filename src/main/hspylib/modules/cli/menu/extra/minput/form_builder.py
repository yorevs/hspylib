from typing import Any

from hspylib.modules.cli.menu.extra.minput.field_builder import FieldBuilder


class FormBuilder:
    def __init__(self):
        self.fields = []

    def field(self) -> Any:
        return FieldBuilder(self)

    def build(self) -> list:
        return self.fields
