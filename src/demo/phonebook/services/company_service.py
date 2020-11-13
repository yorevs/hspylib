from typing import Optional, List
from uuid import UUID

from hspylib.core.meta.singleton import Singleton
from phonebook.entity.Company import Company
from phonebook.entity.Company import Company
from phonebook.exception.NotFoundError import NotFoundError
from phonebook.repository.company_repository import CompanyRepository


class CompanyService(metaclass=Singleton):

    def __init__(self):
        self.company_repository = CompanyRepository()

    def find_one(self, uuid: UUID) -> Optional[Company]:
        return self.company_repository.find_by_id(uuid)

    def find_all(self, filters: str = None) -> List[Company]:
        return self.company_repository.find_all(filters)

    def save(self, company: Company):
        if not self.find_one(company.uuid):
            self.company_repository.insert(company)
        else:
            self.company_repository.update(company)

    def delete(self, company: Company):
        if not self.find_one(company.uuid):
            raise NotFoundError("Company was not found: {}".format(company))
        else:
            self.company_repository.delete(company)
