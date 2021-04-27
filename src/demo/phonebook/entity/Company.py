from uuid import UUID

from phonebook.entity.Contact import Contact


class Company(Contact):
    def __init__(
            self,
            uuid: UUID = None,
            name: str = None,
            phone: str = None,
            website: str = None,
            address: str = None,
            complement: str = None):
        super().__init__(uuid, name, phone, address, complement)
        self.website = website
