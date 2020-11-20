from datetime import datetime
from typing import Tuple, List

from hspylib.core.tools.validator import Validator
from vault.entity.vault_entry import VaultEntry


class EntryValidator(Validator):

    def __call__(self, *entries: VaultEntry, **kwargs) -> Tuple[bool, List[dict]]:
        errors = []
        assert len(entries) == 1, "Exactly one entry can be validated at a time. Given: {}".format(len(entries))
        assert isinstance(entries[0], VaultEntry), "Only vault entries can be validated"
        self.assert_valid(errors, self.validate_key(entries[0].key))
        self.assert_valid(errors, self.validate_name(entries[0].name))
        self.assert_valid(errors, self.validate_password(entries[0].password))
        self.assert_valid(errors, self.validate_hint(entries[0].hint))
        self.assert_valid(errors, self.validate_modified(entries[0].modified))

        return len(errors) == 0, errors

    @staticmethod
    def validate_key(key: str) -> Tuple[bool, str]:
        return Validator \
            .matches(key, Validator.RegexCommons.COMMON_3_30_NAME), "Invalid key"

    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        return Validator \
            .matches(name, Validator.RegexCommons.COMMON_3_30_NAME), "Invalid name"

    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        return Validator.is_not_blank(password, 3), "Invalid password"

    @staticmethod
    def validate_hint(hint: str) -> Tuple[bool, str]:
        return hint is not None, 'Invalid hint'

    @staticmethod
    def validate_modified(modified: datetime) -> Tuple[bool, str]:
        return modified is not None, 'Invalid modified date'
