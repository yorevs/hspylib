from hspylib.core.config.app_config import AppConfigs
from hspylib.core.crud.file.file_repository import FileRepository
from phonebook.entity.person import Person


class PersonRepository(FileRepository):

    def __init__(self):
        self.db_file = "{}/db/{}".format(
            AppConfigs.INSTANCE.resource_dir(),
            AppConfigs.INSTANCE.get("phonebook.persons.db.file")
        )
        super().__init__(self.db_file)

    def dict_to_entity(self, row: dict) -> Person:
        return Person(
            row['uuid'],
            row['name'],
            row['age'],
            row['phone'],
            row['email'],
            row['address'],
            row['complement'])
