from uuid import UUID

from phonebook.entity.contact import Contact


class Person(Contact):
    def __init__(
            self,
            uuid: UUID = None,
            name: str = None,
            age: int = None,
            phone: str = None,
            email: str = None,
            address: str = None,
            complement: str = None):
        super().__init__(uuid, name, phone, address, complement)
        self.age = age
        self.email = email
