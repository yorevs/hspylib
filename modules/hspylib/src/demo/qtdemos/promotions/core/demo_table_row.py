class DemoTableRow:
    """TODO"""

    def __init__(self):
        self.color: str = ''
        self.text: str = ''
        self.desc: str = ''
        self.lst_items: list = []

    def __str__(self):
        return f'Color: {self.color}  Text: {self.text}  Desc: {self.desc}  Items: {",".join(self.lst_items)}'
