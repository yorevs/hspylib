from hspylib.core.namespace import Namespace
from hspylib.modules.cli.tui.minput.input_validator import InputValidator
from hspylib.modules.cli.tui.minput.minput import MenuInput, minput


class ContactForms:

    @staticmethod
    def person_form(
        name: str = '',
        age: int = 0,
        phone: str = '',
        email: str = '',
        address: str = '',
        cpl: str = '') -> Namespace:
        # fmt: off
        form_fields = MenuInput.builder() \
            .field() \
                .label("Name") \
                .validator(InputValidator.letters()) \
                .value(name) \
                .build() \
            .field() \
                .label("Age") \
                .validator(InputValidator.numbers()) \
                .value(age) \
                .build() \
            .field() \
                .label("Phone") \
                .validator(InputValidator.anything()) \
                .value(phone) \
                .build() \
            .field() \
                .label("Email") \
                .validator(InputValidator.anything()) \
                .value(email) \
                .build() \
            .field() \
                .label("Address") \
                .validator(InputValidator.anything()) \
                .value(address) \
                .build() \
            .field() \
                .label("Complement") \
                .validator(InputValidator.numbers()) \
                .value(cpl) \
                .build() \
            .build()
        # fmt: on
        return minput(form_fields, 'Please fill the person form below')

    @staticmethod
    def company_form(
        name: str = '',
        cnpj: str = '',
        phone: str = '',
        website: str = '',
        address: str = '',
        cpl: str = '') -> Namespace:
        # fmt: off
        form_fields = MenuInput.builder() \
            .field() \
                .label("Name") \
                .validator(InputValidator.letters()) \
                .value(name) \
                .build() \
                .field() \
            .label("CNPJ") \
                .validator(InputValidator.anything()) \
                .value(cnpj) \
                .build() \
                .field() \
            .label("Phone") \
                .validator(InputValidator.anything()) \
                .value(phone) \
                .build() \
                .field() \
            .label("WebSite") \
                .validator(InputValidator.anything()) \
                .value(website) \
                .build() \
                .field() \
            .label("Address") \
                .validator(InputValidator.anything()) \
                .value(address) \
                .build() \
                .field() \
            .label("Complement") \
                .validator(InputValidator.numbers()) \
                .value(cpl) \
                .build() \
            .build()
        # fmt: on
        return minput(form_fields, 'Please fill the person form below')