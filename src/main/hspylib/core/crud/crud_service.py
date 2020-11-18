from typing import Optional, List, TypeVar, Generic
from uuid import UUID

from hspylib.core.exception.NotFoundError import NotFoundError

ET = TypeVar('ET')
RT = TypeVar('RT')


class CrudService(Generic[ET, RT]):

    def __init__(self, repository: RT):
        self.repository = repository

    def save(self, entity: ET):
        if not self.get(entity.uuid):
            self.repository.insert(entity)
        else:
            self.repository.update(entity)

    def remove(self, entity: ET):
        if not self.get(entity.uuid):
            raise NotFoundError(
                "{} was not found: {}".format(entity.__class__, entity))
        else:
            self.repository.delete(entity)

    def list(self, filters: str = None) -> List[ET]:
        ret_val = self.repository.find_all(filters)
        return ret_val if ret_val else []

    def get(self, uuid: UUID) -> Optional[ET]:
        return self.repository.find_by_id(str(uuid))
