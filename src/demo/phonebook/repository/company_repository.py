from hspylib.core.config.app_config import AppConfigs
from hspylib.core.crud.file.file_repository import FileRepository
from phonebook.entity.Company import Company


class CompanyRepository(FileRepository):

    def __init__(self):
        self.db_file = "{}/db/{}".format(
            AppConfigs.INSTANCE.resource_dir(),
            AppConfigs.INSTANCE.get("phonebook.companies.db.file")
        )
        super().__init__(self.db_file)

    def insert(self, company: Company):
        super(CompanyRepository, self).insert(company)

    def update(self, company: Company):
        super(CompanyRepository, self).update(company)

    def delete(self, company: Company):
        super(CompanyRepository, self).delete(company)

    def dict_to_entity(self, row: dict) -> Company:
        return Company(
            row['uuid'],
            row['name'],
            row['phone'],
            row['website'],
            row['address'],
            row['complement'])
