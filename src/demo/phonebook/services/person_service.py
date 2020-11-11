from uuid import UUID

from hspylib.core.meta.singleton import Singleton
from hspylib.core.model.entity import Entity
from phonebook.repositories.person_repository import PersonRepository


class PersonService(metaclass=Singleton):

    def __init__(self):
        self.person_repository = PersonRepository()

    def save(self, person: Entity) -> UUID:
        pass
