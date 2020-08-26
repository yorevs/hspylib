from abc import ABC, abstractmethod
from typing import Any


class Menu(ABC):
    @abstractmethod
    def execute(self) -> Any:
        """
        Execute the current menu actions.
        :return: The next menu action to proceed after processing.
        """
        pass

    @abstractmethod
    def trigger_menu_item(self) -> Any:
        """
        Trigger the option action selected by the user.
        :return: The next menu action to trigger.
        """
        pass

    @abstractmethod
    def is_valid_option(self) -> bool:
        """
        Checks if the selected option is within the available options.
        :return: whether the option is valid or not.
        """
        pass
