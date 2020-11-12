from typing import Optional, List
from uuid import UUID

from hspylib.core.meta.singleton import Singleton
from phonebook.entity.Person import Person
from phonebook.exception.NotFoundError import NotFoundError
from phonebook.repository.person_repository import PersonRepository


class PersonService(metaclass=Singleton):

    def __init__(self):
        self.person_repository = PersonRepository()

    def find_one(self, uuid: UUID) -> Optional[Person]:
        return self.person_repository.find_by_id(uuid)

    def find_all(self, filters: str = None) -> List[Person]:
        return self.person_repository.find_all(filters)

    def save(self, person: Person):
        if not self.find_one(person.uuid):
            self.person_repository.insert(person)
        else:
            self.person_repository.update(person)

    def delete(self, person: Person):
        if not self.find_one(person.uuid):
            raise NotFoundError("Person was not found: {}".format(person))
        else:
            self.person_repository.delete(person)
