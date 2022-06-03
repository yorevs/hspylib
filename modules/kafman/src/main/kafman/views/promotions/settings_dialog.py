import os
from pathlib import Path

from hspylib.core.config.properties import Properties
from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.tools.commons import run_dir
from hspylib.modules.qt.promotions.hlistwidget import HListWidget
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialogButtonBox, QWidget


class SettingsDialog:
    """TODO"""

    DIALOG_FORM = str(Path(run_dir()) / "resources/forms/settings_dlg.ui")

    class SettingsType(Enumeration):
        """TODO"""

        PRODUCER_SETTINGS = (Path(run_dir()) / "resources/producer-settings.properties").read_text()

        CONSUMER_SETTINGS = (Path(run_dir()) / "resources/consumer-settings.properties").read_text()

        # @formatter:off
        PRODUCER = 'PRODUCER', PRODUCER_SETTINGS
        CONSUMER = 'CONSUMER', CONSUMER_SETTINGS
        # @formatter:on

        def settings(self) -> str:
            return self.value[1]

    def __init__(
        self, parent: QWidget, settings_type: 'SettingsType', current_settings: dict, settings_widget: HListWidget):

        ui_class, base_class = uic.loadUiType(self.DIALOG_FORM)
        assert ui_class is not None and base_class is not None
        self.dialog, self.ui = base_class(parent), ui_class()
        self.ui.setupUi(self.dialog)
        self._settings = {}
        self._settings_type = settings_type
        self._current_settings = current_settings
        self._settings_widget = settings_widget
        self._setup_controls()

    def _setup_controls(self) -> None:
        """TODO"""
        self._fill_settings()
        self.dialog.resize(360, 180)
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.setModal(True)
        self.ui.cmb_settings.currentTextChanged.connect(self.change_setting)
        self.ui.btn_box.clicked.connect(self._button_clicked)

    def _fill_settings(self):
        all_settings = self._settings_type.settings().split(os.linesep)
        self._settings.update(Properties.read_properties(all_settings))
        self.ui.cmb_settings.addItems({
            k: v for (k, v) in self._settings.items() if k not in self._current_settings
        })

    def set_window_title(self, param):
        self.dialog.setWindowTitle(param)

    def show(self):
        self.dialog.exec()

    def _button_clicked(self, button) -> None:
        role = self.ui.btn_box.buttonRole(button)
        if role == QDialogButtonBox.ApplyRole:
            self.add_setting()

    def change_setting(self, setting_name: str) -> None:
        self.ui.le_value.setText(self._settings[setting_name])

    def add_setting(self) -> None:
        setting_name = self.ui.cmb_settings.currentText()
        setting_value = self.ui.le_value.text()
        self._settings_widget.set_item(self.ui.cmb_settings.currentText())
        self.ui.cmb_settings.removeItem(self.ui.cmb_settings.currentIndex())
        self._current_settings.update({setting_name: setting_value})
