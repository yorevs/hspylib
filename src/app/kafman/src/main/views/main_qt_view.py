from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from hspylib.core.config.app_config import AppConfigs
from hspylib.modules.qt.views.qt_view import QtView
from kafman.src.main.core.kafman_consumer import KafmanConsumer
from kafman.src.main.core.kafman_producer import KafmanProducer


class MainQtView(QtView):
    """
    For all kafka settings: https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    """
    UI_FILE = 'main_qt_view.ui'

    REQUIRED_SETTINGS = ['bootstrap.servers']

    def __init__(self):
        # Must come after the initialization above
        super().__init__(self.UI_FILE)
        self.configs = AppConfigs.INSTANCE
        self._consumer = KafmanConsumer()
        self._producer = KafmanProducer()
        self._all_settings = {
            'producer': {
                'bootstrap.servers': 'localhost:9092',
            },
            'consumer': {
                'bootstrap.servers': 'localhost:9092',
                'group.id': 'kafka_test_group',
                'client.id': 'client-1',
                'enable.auto.commit': 'False',
                'session.timeout.ms': '6000',
                'default.topic.config': {
                    'auto.offset.reset': 'smallest'
                }
            }
        }
        self.setup_ui()

    def setup_ui(self) -> None:
        """Connect signals and startup components"""
        self.ui.main_dialog = self.window.findChild(QDialog, 'main_dialog')
        self._set_current_tab(0)
        self.ui.tool_box.setCurrentIndex(0)
        self.ui.splitter_pane.setSizes([300, 824])
        self.ui.tab_widget.currentChanged.connect(self._set_current_tab)
        self.ui.lbl_status_text.setTextFormat(Qt.RichText)
        self.ui.btn_start.clicked.connect(self._start)
        self.ui.btn_stop.clicked.connect(self._stop)
        self.ui.cmb_topic.lineEdit().setPlaceholderText("Select or type comma (,) separated topics")
        # Producer controls
        self.ui.tbtn_prod_settings_add.clicked.connect(lambda: self.ui.lst_prod_settings.set_item('new.setting'))
        self.ui.tbtn_prod_settings_del.clicked.connect(self._del_item)
        self.ui.lst_prod_settings.currentRowChanged.connect(self._get_setting)
        self.ui.lst_prod_settings.set_editable()
        self.ui.le_prod_settings.editingFinished.connect(self._edit_setting)
        self.ui.lst_prod_settings.itemChanged.connect(self._edit_setting)
        # Consumer controls
        self.ui.tbtn_cons_settings_add.clicked.connect(lambda: self.ui.lst_cons_settings.set_item('new.setting'))
        self.ui.tbtn_cons_settings_del.clicked.connect(self._del_item)
        self.ui.lst_cons_settings.currentRowChanged.connect(self._get_setting)
        self.ui.lst_cons_settings.set_editable()
        self.ui.le_cons_settings.editingFinished.connect(self._edit_setting)
        self.ui.lst_cons_settings.itemChanged.connect(self._edit_setting)

    def _topics(self) -> List[str]:
        """TODO"""
        current_text = self.ui.cmb_topic.currentText()
        return current_text.split(',') if current_text else []

    def _message(self) -> str:
        """TODO"""
        return self.ui.txt_producer.toPlainText()

    def _settings(self) -> dict:
        """TODO"""
        return self._all_settings['producer' if self._is_producer() else 'consumer']

    def _is_producer(self) -> bool:
        """TODO"""
        return self.ui.btn_start.text() == 'Produce'

    def _set_current_tab(self, index: int) -> None:
        """TODO"""
        index = index or self.ui.tab_widget.currentIndex()
        self.ui.btn_start.setText('Produce' if index == 0 else 'Consume')
        self.ui.tab_widget.setCurrentIndex(index)
        self.ui.stk_settings.setCurrentIndex(index)
        self.ui.stk_strategy.setCurrentIndex(index)
        self.ui.stk_statistics.setCurrentIndex(index)

    def _get_setting(self) -> None:
        """TODO"""
        lst = self.ui.lst_prod_settings if self._is_producer() else self.ui.lst_cons_settings
        edt = self.ui.le_prod_settings if self._is_producer() else self.ui.le_cons_settings
        ktype = self.ui.btn_start.text().lower() + 'r'
        item = lst.currentItem()
        if item and item.text():
            setting = item.text()
            if setting in self._all_settings[ktype]:
                edt.setText(self._all_settings[ktype][setting])
            else:
                edt.setText('')
                self._all_settings[ktype][setting] = ''

    def _edit_setting(self) -> None:
        """TODO"""
        lst = self.ui.lst_prod_settings if self._is_producer() else self.ui.lst_cons_settings
        edt = self.ui.le_prod_settings if self._is_producer() else self.ui.le_cons_settings
        ktype = self.ui.btn_start.text().lower() + 'r'
        item = lst.currentItem()
        if item:
            setting = item.text()
            old_setting = next((s for i, s in enumerate(self._all_settings[ktype]) if i == lst.currentRow()), '')
            if setting:
                if setting not in self._all_settings[ktype]:
                    del self._all_settings[ktype][old_setting]
                if edt.text():
                    self._all_settings[ktype][setting] = edt.text()
                    self._display_text(f"{ktype.capitalize()} setting {setting} saved")
                else:
                    edt.setText(self._all_settings[ktype][setting])
            else:
                setting = old_setting
                edt.setText(self._all_settings[ktype][setting])
                item.setText(setting)
                if setting:
                    self._display_error(f"Setting {setting} is required")

    def _del_item(self) -> None:
        """TODO"""
        lst = self.ui.lst_prod_settings if self._is_producer() else self.ui.lst_cons_settings
        ktype = self.ui.btn_start.text().lower() + 'r'
        item = lst.currentItem()
        if item:
            setting = item.text()
            if setting and setting not in self.REQUIRED_SETTINGS:
                lst.del_item(lst.currentRow())
                del self._all_settings[ktype][setting]
            else:
                self._display_error(f"Setting {setting} is required")

    def _start(self) -> None:
        """TODO"""
        settings = self._settings()
        topics = self._topics()
        if topics and all(s in settings for s in self.REQUIRED_SETTINGS):
            self.ui.cmb_topic.addItem(','.join(topics))
            if self._is_producer():
                if self._message():
                    self._producer.start(settings)
                    self._display_text(f"Started producing to topics {topics}", '#00FF00')
                else:
                    self._display_error('No message defined')
                    return
            else:
                self._consumer.start(settings)
                self._display_text(f"Started consuming from topics {topics}", '#00FF00')
            self.ui.btn_stop.setEnabled(True)
            self.ui.btn_start.setEnabled(False)
            self.ui.tab_widget.setEnabled(False)
            self.ui.cmb_topic.setEnabled(False)
        else:
            self._display_error('No topic selected')

    def _stop(self):
        """TODO"""
        if self._is_producer():
            self._producer.stop()
            self._display_text(f"Production to topic {self._topics()} stopped", '#FFFF00')
        else:
            self._consumer.stop()
            self._display_text(f"Consumption from topic {self._topics()} stopped", '#FFFF00')
        self.ui.btn_stop.setEnabled(False)
        self.ui.btn_start.setEnabled(True)
        self.ui.tab_widget.setEnabled(True)
        self.ui.cmb_topic.setEnabled(True)

    def _display_error(self, message: str) -> None:
        """TODO"""
        self.ui.lbl_status_text.setText(f"<font color='#FF0000'>{message}</font>")

    def _display_text(self, message: str, rgb: str = None) -> None:
        """TODO"""
        if rgb:
            self.ui.lbl_status_text.setText(f"<font color='{rgb}'>{message}</font>")
        else:
            self.ui.lbl_status_text.setText(message)
