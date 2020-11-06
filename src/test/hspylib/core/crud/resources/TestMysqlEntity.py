from uuid import UUID

from hspylib.core.model.entity import Entity


class TestMysqlEntity(Entity):
    def __init__(self, entity_id: UUID = None, comment: str = None):
        super().__init__(entity_id)
        self.comment = comment

    def __str__(self):
        return 'uuid={} comment={}'.format(self.uuid, self.comment)
