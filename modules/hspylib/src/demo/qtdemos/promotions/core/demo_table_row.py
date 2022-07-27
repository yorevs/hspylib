class DemoTableRow:
    """TODO"""

    def __init__(self):
        self.color: str = ''
        self.text: str = ''
        self.desc: str = ''
        self.lst_items: list = []

    def __str__(self):
        return f'' \
               f'{"Color: " + self.color if self.color else " "}' \
               f'{"  Text: " + self.text if self.text else " "}' \
               f'{"  Desc: " + self.desc if self.desc else " "}' \
               f'{"  Items: " + ",".join(self.lst_items) if self.lst_items else " "}'
