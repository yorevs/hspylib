class MenuOption:
    def __init__(self, parent, option_index: int, option_text: str):
        self.parent = parent
        self.option_index = option_index
        self.option_text = option_text
        self.action_trigger = lambda s: print(f"Option: {self.option_index}-{self.option_text} selected!")

    def on_trigger(self, action_trigger):
        self.action_trigger = action_trigger
        return self.parent

    def __str__(self):
        return "\033[0;32m[{}]\033[0;0;0m {}".format(self.option_index, self.option_text)
