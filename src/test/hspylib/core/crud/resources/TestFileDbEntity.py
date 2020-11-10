from uuid import UUID

from hspylib.core.model.entity import Entity


class TestFileDbEntity(Entity):
    def __init__(self, entity_id: UUID = None, comment: str = None, lucky_number: int = 0, is_working: bool = False):
        super().__init__(entity_id)
        self.comment = comment
        self.lucky_number = lucky_number
        self.is_working = is_working

    def __str__(self):
        return 'uuid={} comment={} lucky_number={}'.format(self.uuid, self.comment, self.lucky_number)
