import re
from typing import Any

from hspylib.core.tools.text_helper import camelcase
from hspylib.modules.cli.menu.extra.minput.input_field import InputField


class FieldBuilder:

    modes = ['input', 'password', 'checkbox', 'select']
    kinds = ['letter', 'number', 'word', 'token', 'any']
    access_types = ['read-only', 'read-write']

    def __init__(self, parent: Any):
        self.parent = parent
        self.field = InputField()

    def label(self, label: str) -> Any:
        self.field.label = label
        return self

    def mode(self, mode: str) -> Any:
        assert mode in self.modes, \
            f"Not a valid mode: {mode}. Valid modes are: {str(self.modes)}"
        self.field.mode = mode
        return self

    def kind(self, kind: str) -> Any:
        assert kind in self.kinds, \
            f"Not a valid kind: {kind}. Valid kinds are: {str(self.kinds)}"
        self.field.kind = kind
        return self

    def min_max_length(self, min_length: int, max_length: int) -> Any:
        assert max_length >= min_length, f"Not a valid field length: ({min_length}-{max_length})"
        assert max_length > 0 and min_length > 0, f"Not a valid field length: ({min_length}-{max_length})"
        self.field.min_length = min_length
        self.field.max_length = max_length
        return self

    def access_type(self, access_type: str) -> Any:
        assert access_type in self.access_types, \
            f"Not a valid access type {access_type}. Valid access types are: {str(self.access_types)}"
        self.field.access_type = access_type
        return self

    def value(self, value: Any) -> Any:
        re_valid = self.field.val_regex(0, len(str(value)))
        if value:
            assert re.match(re_valid, value), f"Not a valid value: \"{value}\". Valid regex is \"{re_valid}\""
        self.field.value = value
        return self

    def build(self) -> Any:
        if self.field.mode == "checkbox":
            self.field.value = self.field.value if self.field.value in ['0', '1'] else 0
            self.field.min_length = self.field.max_length = 1
        elif self.field.mode == "select":
            self.field.min_length = self.field.max_length = 1
        self.field.label = camelcase(self.field.label) or 'Field'
        self.field.access_type = self.field.access_type or 'read-write'
        self.field.min_length = self.field.min_length or 1
        self.field.max_length = self.field.max_length or 30
        self.field.kind = self.field.kind or 'any'
        self.field.kind = self.field.kind or 'input'
        self.field.value = self.field.value or ''
        self.parent.fields.append(self.field)
        return self.parent
