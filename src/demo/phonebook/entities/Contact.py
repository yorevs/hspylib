from uuid import UUID

from hspylib.core.model.entity import Entity


class Contact(Entity):
    def __init__(
            self,
            uuid: UUID = None,
            name: str = None,
            phone: str = None,
            address: str = None,
            complement: str = None):

        super().__init__(uuid)
        self.name = name
        self.phone = phone
        self.address = address
        self.complement = complement
