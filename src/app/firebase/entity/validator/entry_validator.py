from typing import Tuple, List

from firebase.entity.firebase_entry import FirebaseEntry
from hspylib.core.tools.validator import Validator


class EntryValidator(Validator):

    def __call__(self, *entries: FirebaseEntry, **kwargs) -> Tuple[bool, List[dict]]:
        errors = []
        assert len(entries) == 1, "Exactly one entry can be validated at a time. Given: {}".format(len(entries))
        assert isinstance(entries[0], FirebaseEntry), "Only firebase entries can be validated"
        self.assert_valid(errors, self.validate_payload(entries[0].data))

        return len(errors) == 0, errors

    @staticmethod
    def validate_payload(payload: str) -> Tuple[bool, str]:
        return False, "TODO"
