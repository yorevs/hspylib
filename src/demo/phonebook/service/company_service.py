from hspylib.core.crud.crud_service import CrudService
from hspylib.core.meta.singleton import Singleton
from phonebook.repository.company_repository import CompanyRepository


class CompanyService(CrudService, metaclass=Singleton):

    def __init__(self):
        self.repository = CompanyRepository()
        super().__init__(self.repository)
