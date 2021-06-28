import ast
import atexit
import os
import re
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QHeaderView

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.tools.commons import run_dir, now, now_ms, read_version
from hspylib.core.tools.text_tools import strip_escapes
from hspylib.modules.eventbus.event import Event
from hspylib.modules.eventbus.eventbus import EventBus
from hspylib.modules.qt.promotions.htablemodel import HTableModel
from hspylib.modules.qt.views.qt_view import QtView
from hspylib.modules.qt.stream_capturer import StreamCapturer
from kafman.src.main.core.constants import StatusColor
from kafman.src.main.core.kafka_consumer import KafkaConsumer
from kafman.src.main.core.kafka_producer import KafkaProducer
from kafman.src.main.core.message_row import MessageRow
from kafman.src.main.core.statistics import Statistics


class MainQtView(QtView):
    """
    For all kafka settings: https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    """
    VERSION = read_version(f"{run_dir()}/.version")
    UI_FILE = 'main_qt_view.ui'
    HISTORY_FILE = f"{run_dir()}/resources/kafman-history.txt"
    REQUIRED_SETTINGS = ['bootstrap.servers']

    class Tabs(Enumeration):
        """TODO"""
        PRODUCER = 0
        CONSUMER = 1
        CONSOLE = 2

    class Tools(Enumeration):
        """TODO"""
        SETTINGS = 0
        STRATEGY = 1
        STATISTICS = 2

    def __init__(self):
        # Must come after the initialization above
        super().__init__(self.UI_FILE)
        self.configs = AppConfigs.INSTANCE
        self._started = False
        self._consumer = KafkaConsumer()
        self._consumer.messageConsumed.connect(self._message_consumed)
        self._producer = KafkaProducer()
        self._producer.messageProduced.connect(self._message_produced)
        self._all_settings = None
        self._stats = Statistics()
        self._capturer = StreamCapturer()
        self._capturer.start()
        self._stats_bus = EventBus.get('kafka-statistics')
        self._stats_bus.subscribe('stats-report', self._update_stats)
        self._capturer.stderrCaptured.connect(self._console_print_err)
        self._capturer.stdoutCaptured.connect(self._console_print)
        self._display_text(f"Application started at {now()}<br/>{'-' * 45}<br/>")
        self.setup_ui()
        self._load_history()
        atexit.register(self._save_history)

    def setup_ui(self) -> None:
        """Connect signals and startup components"""
        self.set_default_font(QFont("DroidSansMono Nerd Font", 14))
        self.window.setWindowTitle(f"Kafman v{'.'.join(self.VERSION)}")
        self.window.resize(1024, 768)
        self.ui.splitter_pane.setSizes([350, 824])
        self.ui.tool_box.setCurrentIndex(self.Tools.SETTINGS.value)
        self.ui.tab_widget.currentChanged.connect(self._activate_tab)
        self.ui.lbl_status_text.setTextFormat(Qt.RichText)
        self.ui.btn_action.setAutoRepeat(False)
        self.ui.btn_action.clicked.connect(self._toggle_start)
        self.ui.cmb_topic.lineEdit().setPlaceholderText("Select or type comma (,) separated topics")
        self.ui.cmb_topic.setDuplicatesEnabled(False)
        # Producer controls
        self.ui.tbtn_prod_settings_add.clicked.connect(lambda: self.ui.lst_prod_settings.set_item('new.setting'))
        self.ui.tbtn_prod_settings_del.clicked.connect(self._del_setting)
        self.ui.lst_prod_settings.currentRowChanged.connect(self._get_setting)
        self.ui.lst_prod_settings.set_editable()
        self.ui.lst_prod_settings.itemChanged.connect(self._edit_setting)
        self.ui.le_prod_settings.editingFinished.connect(self._edit_setting)
        self.ui.tbtn_produce.clicked.connect(self._produce)
        # Consumer controls
        self.ui.tbtn_cons_settings_add.clicked.connect(lambda: self.ui.lst_cons_settings.set_item('new.setting'))
        self.ui.tbtn_cons_settings_del.clicked.connect(self._del_setting)
        self.ui.lst_cons_settings.currentRowChanged.connect(self._get_setting)
        self.ui.lst_cons_settings.set_editable()
        self.ui.lst_cons_settings.itemChanged.connect(self._edit_setting)
        self.ui.le_cons_settings.editingFinished.connect(self._edit_setting)
        self.ui.tbl_consumer.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        HTableModel(self.ui.tbl_consumer, MessageRow, MessageRow.headers())

    def _is_producer(self) -> bool:
        """Whether started as producer or consumer"""
        return self.ui.tab_widget.currentIndex() == self.Tabs.PRODUCER.value

    def _kafka_type(self) -> str:
        return 'producer' if self._is_producer() else 'consumer'

    def _topics(self) -> List[str]:
        """Return the selected topics"""
        current_text = self.ui.cmb_topic.currentText()
        return current_text.split(',') if current_text else []

    def _messages(self) -> List[str]:
        """Return the selected messages"""
        msgs = self.ui.txt_producer.toPlainText().split('\n')
        return list(filter(lambda m: m != '', msgs))

    def _settings(self) -> dict:
        """Return the configured settings"""
        return self._all_settings[self._kafka_type()]

    def _activate_tab(self, index: int = None) -> None:
        """Set the selected tab"""
        index = index if index is not None else self.ui.tab_widget.currentIndex()
        if not self._started:
            self.ui.btn_action.setText('Produce' if self._is_producer() else 'Consume')
        self.ui.tab_widget.setCurrentIndex(index)
        self.ui.stk_settings.setCurrentIndex(index)
        self.ui.stk_statistics.setCurrentIndex(index)

    def _get_setting(self) -> None:
        """Get a setting and display it on the proper line edit field"""
        lst = self.ui.lst_prod_settings if self._is_producer() else self.ui.lst_cons_settings
        edt = self.ui.le_prod_settings if self._is_producer() else self.ui.le_cons_settings
        ktype = self._kafka_type()
        item = lst.currentItem()
        if item and item.text():
            setting = item.text()
            if setting in self._all_settings[ktype]:
                edt.setText(str(self._all_settings[ktype][setting]))
            else:
                edt.setText('')
                self._all_settings[ktype][setting] = ''

    def _edit_setting(self) -> None:
        """Edit a setting from the proper line edit field"""
        lst = self.ui.lst_prod_settings if self._is_producer() else self.ui.lst_cons_settings
        edt = self.ui.le_prod_settings if self._is_producer() else self.ui.le_cons_settings
        ktype = self._kafka_type()
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

    def _del_setting(self) -> None:
        """Delete a setting specified by the proper line edit field"""
        lst = self.ui.lst_prod_settings if self._is_producer() else self.ui.lst_cons_settings
        ktype = self._kafka_type()
        item = lst.currentItem()
        if item:
            setting = item.text()
            if setting and setting not in self.REQUIRED_SETTINGS:
                lst.del_item(lst.currentRow())
                del self._all_settings[ktype][setting]
            else:
                self._display_error(f"Setting {setting} is required")

    def _add_topic(self, topic: str):
        """Add a topic to the combo box."""
        self.ui.cmb_topic.set_item(topic)

    def _toggle_start(self):
        """Start/Stop the consumer or producer (whatever is selected)."""
        if self._started:
            self._stop()
            self.ui.btn_action.setText('Produce' if self._is_producer() else 'Consume')
            self.ui.tool_box.setCurrentIndex(0)
        else:
            if self._start():
                self.ui.btn_action.setText('Stop')
                self.ui.tool_box.setCurrentIndex(2)

    def _start(self) -> bool:
        """Start consuming or producing (whatever is selected)."""
        settings = self._settings()
        topics = self._topics()
        if topics and all(s in settings for s in self.REQUIRED_SETTINGS):
            self._add_topic(self.ui.cmb_topic.currentText())
            if self._is_producer():
                self._producer.start(settings)
                self._display_text(f"Started producing to topics {topics}", StatusColor.green)
                self.ui.tbtn_produce.setEnabled(True)
            else:
                self._consumer.start(settings)
                self._consumer.consume(topics)
                self._display_text(f"Started consuming from topics {topics}", StatusColor.green)
            self.ui.cmb_topic.setEnabled(False)
        else:
            self._display_error('No topic selected')
            return False
        self._started = True

        return True

    def _stop(self) -> None:
        """Stop consuming or producing (what is selected)."""
        if self._is_producer():
            self._producer.stop()
            self._display_text(f"Production to topic {self._topics()} stopped", StatusColor.yellow)
        else:
            self._consumer.stop()
            self._display_text(f"Consumption from topic {self._topics()} stopped", StatusColor.yellow)
        self.ui.cmb_topic.setEnabled(True)
        self.ui.tbtn_produce.setEnabled(False)
        self._started = False

    def _produce(self) -> None:
        """TODO"""
        messages = self._messages()
        size = len(messages)
        if self._started and self._is_producer() and size > 0:
            topics = self._topics()
            self._producer.produce(topics, messages)
            self._display_text(f"Produced {size} messages to Kafka topics", StatusColor.blue, False)
        self.ui.txt_producer.clear()

    def _display_error(self, message: str, add_console: bool = False) -> None:
        """Display an error at the status bar (and console if required)"""
        self._display_text(message, StatusColor.red, add_console)

    def _display_text(self, message: str, color: QColor = None, add_console: bool = True) -> None:
        """Display a text at the status bar (and console if required)"""
        message = f"<font color='{color.name() if color else 'white'}'>{message}</font>"
        self.ui.lbl_status_text.setText(message)
        if add_console:
            self._console_print(f"-> {message}", color)

    def _update_stats(self, event: Event):
        """Update the consumer and producer statistics"""
        self.ui.lbl_stats_produced.setText(str(event['stats'][0]))
        self.ui.lbl_stats_produced_ps.setText(str(event['stats'][2]))
        self.ui.lbl_stats_consumed.setText(str(event['stats'][1]))
        self.ui.lbl_stats_consumed_ps.setText(str(event['stats'][3]))
        self.ui.lbl_stats_produced_avg.setText(str(event['stats'][4]))
        self.ui.lbl_stats_consumed_avg.setText(str(event['stats'][5]))

    def _message_produced(self, topic: str, message: str) -> None:
        """Callback when a kafka message has been produced."""
        text = f"-> Produced timestamp={now_ms()} topic={topic} message={message}"
        self._console_print(text, StatusColor.blue)
        self._stats.produced()

    def _message_consumed(self, topic: str, message: str) -> None:
        """Callback when a kafka message has been consumed."""
        text = f"-> Consumed timestamp={now_ms()} topic={topic} message={message}"
        self.ui.tbl_consumer.model().push_data([MessageRow(now_ms(), topic, message)])
        self._console_print(text, StatusColor.orange)
        self._stats.consumed()

    def _console_print(self, text: str, color: QColor = None) -> None:
        """Append a message to the console."""
        if isinstance(text, str):
            msg = text
        else:
            raise TypeError('Expecting string or Event objects')
        self.ui.txt_console.push_text(strip_escapes(msg), color)

    def _console_print_err(self, text: str) -> None:
        """Append an error message to the console."""
        self._console_print(f"-> {text}", StatusColor.red)

    def _save_history(self):
        """Save current app history."""
        with open(self.HISTORY_FILE, 'w') as fd_history:
            cmb = self.ui.cmb_topic
            fd_history.write(f"topics = {[cmb.itemText(i) for i in range(cmb.count())]}\n")
            fd_history.write(f"settings = {str(self._all_settings)}\n")
            fd_history.write(f"tab = {self.ui.tab_widget.currentIndex()}\n")

    def _load_history(self):
        """Load a previously saved app history."""
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
                                self._activate_tab(int(prop_value))
                            except ValueError:
                                self._activate_tab(self.Tabs.PRODUCER.value)

        else:
            # Defaults
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
            self._activate_tab()
