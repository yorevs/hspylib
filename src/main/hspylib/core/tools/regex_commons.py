from abc import ABC


class RegexCommons(ABC):
    UUID = '^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
    PHONE_NUMBER = '((\\d{2})?\\s)?(\\d{4,5}\\-\\d{4})'
    COMMON_3_30_NAME = '[a-zA-Z]\\w{2,30}'
    EMAIL_W3C = '^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$'
    URL = '^(?:http(s)?:\\/\\/)?[\\w.-]+(?:\\.[\\w\\.-]+)+[\\w\\-\\._~:/?#[\\]@!\\$&\'\\(\\)\\*\\+,;=.]+$'
