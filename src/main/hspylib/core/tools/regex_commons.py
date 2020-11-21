class RegexCommons:
    PHONE_NUMBER = '((\\d{2})?\\s)?(\\d{4,5}\\-\\d{4})'
    COMMON_3_30_NAME = '[a-zA-Z]\\w{2,30}'
    EMAIL_W3C = '^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$'
    URL = '^(?:http(s)?:\\/\\/)?[\\w.-]+(?:\\.[\\w\\.-]+)+[\\w\\-\\._~:/?#[\\]@!\\$&\'\\(\\)\\*\\+,;=.]+$'
