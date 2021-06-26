import ast
import atexit
import os
import re
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QDialog, QHeaderView

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.tools.commons import run_dir, now, now_ms
from hspylib.modules.qt.promotions.entity_table_model import EntityTableModel
from hspylib.modules.qt.views.qt_view import QtView
from kafman.src.main.core.kafman_consumer import KafmanConsumer
from kafman.src.main.core.kafman_producer import KafmanProducer
from kafman.src.main.entity.message_row import MessageRow


class MainQtView(QtView):
    """
    For all kafka settings: https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    """
    UI_FILE = 'main_qt_view.ui'
    HISTORY_FILE = f"{run_dir()}/resources/kafman-history.txt"

    REQUIRED_SETTINGS = ['bootstrap.servers']

    def __init__(self):
        # Must come after the initialization above
        super().__init__(self.UI_FILE)
        self.configs = AppConfigs.INSTANCE
        self._consumer = KafmanConsumer()
        self._consumer.messageConsumed.connect(self._message_consumed_event)
        self._producer = KafmanProducer()
        self._producer.messageProduced.connect(self._message_produced_event)
        self._all_settings = None
        self._display_text(f"Application started at {now()}<br/>{'-' * 45}<br/>")
        self.setup_ui()
        self._load_history()
        atexit.register(self._save_history)

    def setup_ui(self) -> None:
        """Connect signals and startup components"""
        default_font = QFont("Courier New", 13)
        self.ui.main_dialog = self.window.findChild(QDialog, 'main_dialog')
        self.ui.tool_box.setCurrentIndex(0)
        self.ui.splitter_pane.setSizes([300, 824])
        self.ui.tab_widget.currentChanged.connect(self._set_current_tab)
        self.ui.lbl_status_text.setTextFormat(Qt.RichText)
        self.ui.btn_start.clicked.connect(self._start)
        self.ui.btn_stop.clicked.connect(self._stop)
        self.ui.lbl_status_text.setFont(default_font)
        self.ui.cmb_topic.lineEdit().setPlaceholderText("Select or type comma (,) separated topics")
        self.ui.cmb_topic.setDuplicatesEnabled(False)
        # Producer controls
        self.ui.tbtn_prod_settings_add.clicked.connect(lambda: self.ui.lst_prod_settings.set_item('new.setting'))
        self.ui.tbtn_prod_settings_del.clicked.connect(self._del_item)
        self.ui.lst_prod_settings.currentRowChanged.connect(self._get_setting)
        self.ui.lst_prod_settings.set_editable()
        self.ui.lst_prod_settings.setFont(default_font)
        self.ui.le_prod_settings.editingFinished.connect(self._edit_setting)
        self.ui.lst_prod_settings.itemChanged.connect(self._edit_setting)
        self.ui.txt_producer.setFont(default_font)
        # Consumer controls
        self.ui.tbtn_cons_settings_add.clicked.connect(lambda: self.ui.lst_cons_settings.set_item('new.setting'))
        self.ui.tbtn_cons_settings_del.clicked.connect(self._del_item)
        self.ui.lst_cons_settings.currentRowChanged.connect(self._get_setting)
        self.ui.lst_cons_settings.set_editable()
        self.ui.lst_cons_settings.setFont(default_font)
        self.ui.le_cons_settings.editingFinished.connect(self._edit_setting)
        self.ui.lst_cons_settings.itemChanged.connect(self._edit_setting)
        self.ui.tbl_consumer.setFont(default_font)
        self.ui.tbl_consumer.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tbl_consumer.setModel(EntityTableModel(
            self.ui.tbl_consumer, MessageRow, ['Timestamp', 'Topic', 'Message']
        ))

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

    def _set_current_tab(self, index: int = 0) -> None:
        """TODO"""
        index = index if index is not None else self.ui.tab_widget.currentIndex()
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
                edt.setText(str(self._all_settings[ktype][setting]))
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
                    self._display_text(f"{ktype.capitalize()} setting '{setting}' saved")
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

    def _add_topic(self, topic: str):
        """TODO"""
        self.ui.cmb_topic.set_item(topic)

    def _start(self) -> None:
        """TODO"""
        settings = self._settings()
        topics = self._topics()
        if topics and all(s in settings for s in self.REQUIRED_SETTINGS):
            self._add_topic(self.ui.cmb_topic.currentText())
            if self._is_producer():
                if self._message():
                    self._set_current_tab(2)
                    self._producer.start(settings)
                    self._producer.produce(topics, self._message().split('\n'))
                    self._display_text(f"Started producing to topics {topics}", QColor('#00FF00'))
                else:
                    self._display_error('No message defined')
                    return
            else:
                self._set_current_tab(1)
                self._consumer.start(settings)
                self._consumer.consume(topics)
                self._display_text(f"Started consuming from topics {topics}", QColor('#00FF00'))
            self.ui.btn_stop.setEnabled(True)
            self.ui.btn_start.setEnabled(False)
            self.ui.cmb_topic.setEnabled(False)
        else:
            self._display_error('No topic selected')

    def _stop(self):
        """TODO"""
        if self._is_producer():
            self._producer.stop()
            self._display_text(f"Production to topic {self._topics()} stopped", QColor('#FFFF00'))
        else:
            self._consumer.stop()
            self._display_text(f"Consumption from topic {self._topics()} stopped", QColor('#FFFF00'))
        self.ui.btn_stop.setEnabled(False)
        self.ui.btn_start.setEnabled(True)
        self.ui.cmb_topic.setEnabled(True)

    def _display_error(self, message: str, add_console: bool = False) -> None:
        """TODO"""
        red = QColor('#FF0000')
        self._display_text(message, red)
        if add_console:
            self._console_print(f"-> {message}", red)

    def _display_text(self, message: str, color: QColor = None) -> None:
        """TODO"""
        message = f"<font color='{color.name() if color else 'white'}'>{message}</font>"
        self.ui.lbl_status_text.setText(message)
        self._console_print(f"-> {message}", color)

    def _message_produced_event(self, topic: str, event: str) -> None:
        """TODO"""
        text = f"{now()} [Produced] {event}"
        self._console_print(text, QColor('#2380FA'))

    def _message_consumed_event(self, topic: str, event: str) -> None:
        """TODO"""
        text = f"{now()} [Consumed] {event}"
        self.ui.tbl_consumer.model().append_data([MessageRow(now_ms(), topic, event)])
        self._console_print(text, QColor('#FF8C36'))

    def _console_print(self, text: str, color: QColor = None) -> None:
        """TODO"""
        if isinstance(text, str):
            msg = text
        else:
            raise TypeError('Expecting string or Event objects')
        self.ui.txt_console.push_text(msg, color)

    def _save_history(self):
        """TODO"""
        with open(self.HISTORY_FILE, 'w') as fd_history:
            cmb = self.ui.cmb_topic
            fd_history.write(f"topics = {[cmb.itemText(i) for i in range(cmb.count())]}\n")
            fd_history.write(f"settings = {str(self._all_settings)}\n")
            fd_history.write(f"tab = {self.ui.tab_widget.currentIndex()}\n")

    def _load_history(self):
        """TODO"""
        if os.path.exists(self.HISTORY_FILE) and os.stat(self.HISTORY_FILE).st_size > 250:
            self._display_text('History recovered')
            with open(self.HISTORY_FILE, 'r') as fd_history:
                lines = fd_history.readlines()
                for line in lines:
                    mat = re.search(r'(.*) ?= ?(.*)', line)
                    if mat:
                        prop_name = mat.group(1).strip()
                        prop_value = mat.group(2).strip()
                        if prop_name == 'topics':
                            list(map(self._add_topic, ast.literal_eval(prop_value)))
                        elif prop_name == 'settings':
                            self._all_settings = ast.literal_eval(prop_value)
                        elif prop_name == 'tab':
                            try:
                                self._set_current_tab(int(prop_value))
                            except ValueError:
                                self._set_current_tab()

        else:
            self._display_text('History discarded')
            self.ui.cmb_topic.addItem('foobar')
            self._all_settings = {
                'producer': {
                    'bootstrap.servers': 'localhost:9092',
                },
                'consumer': {
                    'bootstrap.servers': 'localhost:9092',
                    'group.id': 'kafka_test_group',
                    'client.id': 'client-1',
                    'enable.auto.commit': True,
                    'session.timeout.ms': 6000,
                    'default.topic.config': {
                        'auto.offset.reset': 'smallest'
                    }
                }
            }
            self._set_current_tab()
