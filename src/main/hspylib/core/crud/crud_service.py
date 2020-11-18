from typing import Optional, List
from typing import TypeVar, Generic
from uuid import UUID

from hspylib.core.crud.repository import Repository
from hspylib.core.exception.NotFoundError import NotFoundError
from hspylib.core.model.entity import Entity

T = TypeVar('T')


class CrudService(Generic[T]):

    def __init__(self, repository: Repository):
        self.repository = repository

    def save(self, entity: Entity):
        if not self.get(entity.uuid):
            self.repository.insert(entity)
        else:
            self.repository.update(entity)

    def remove(self, entity: Entity):
        if not self.get(entity.uuid):
            raise NotFoundError(
                "{} was not found: {}".format(entity.__class__, entity))
        else:
            self.repository.delete(entity)

    def list(self, filters: str = None) -> List[Entity]:
        ret_val = self.repository.find_all(filters)
        return ret_val if ret_val else []

    def get(self, uuid: UUID) -> Optional[Entity]:
        return self.repository.find_by_id(str(uuid))
