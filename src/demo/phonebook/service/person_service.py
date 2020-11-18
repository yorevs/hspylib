from hspylib.core.crud.crud_service import CrudService
from hspylib.core.meta.singleton import Singleton
from phonebook.repository.person_repository import PersonRepository


class PersonService(CrudService, metaclass=Singleton):

    def __init__(self):
        self.repository = PersonRepository()
        super().__init__(self.repository)
