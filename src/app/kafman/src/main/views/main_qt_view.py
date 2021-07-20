#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: main_qt_view.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import ast
import atexit
import json
import os
import re
from collections import defaultdict
from typing import List, Optional, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QFileDialog

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.tools.commons import run_dir, now, now_ms, read_version, dirname
from hspylib.core.tools.text_tools import strip_escapes
from hspylib.modules.cli.icons.font_awesome.dashboard_icons import DashboardIcons
from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from hspylib.modules.fetch.fetch import is_reachable
from hspylib.modules.qt.kafka.consumer_config import ConsumerConfig
from hspylib.modules.qt.kafka.kafka_consumer import KafkaConsumer
from hspylib.modules.qt.kafka.kafka_message import KafkaMessage
from hspylib.modules.qt.kafka.kafka_producer import KafkaProducer
from hspylib.modules.qt.kafka.kafka_statistics import KafkaStatistics
from hspylib.modules.qt.kafka.producer_config import ProducerConfig
from hspylib.modules.qt.kafka.schemas.kafka_avro_schema import KafkaAvroSchema
from hspylib.modules.qt.kafka.schemas.kafka_json_schema import KafkaJsonSchema
from hspylib.modules.qt.kafka.schemas.kafka_plain_schema import KafkaPlainSchema
from hspylib.modules.qt.kafka.schemas.kafka_schema import KafkaSchema
from hspylib.modules.qt.promotions.htablemodel import HTableModel
from hspylib.modules.qt.stream_capturer import StreamCapturer
from hspylib.modules.qt.views.qt_view import QtView
from kafman.src.main.core.constants import StatusColor, MAX_HISTORY_SIZE_BYTES


class MainQtView(QtView):
    """TODO"""
    VERSION = read_version(f"{run_dir()}/.version")
    HISTORY_FILE = f"{run_dir()}/resources/kafman-history.txt"
    REQUIRED_SETTINGS = ['bootstrap.servers']

    class Tabs(Enumeration):
        """TODO"""
        PRODUCER = 0
        CONSUMER = 1
        CONSOLE = 2

    class StkTools(Enumeration):
        """TODO"""
        SETTINGS = 0
        SCHEMAS = 1
        STATISTICS = 2

    class StkProducerEdit(Enumeration):
        """TODO"""
        TEXT = 0
        FORM = 1

    @staticmethod
    def supported_schemas() -> str:
        """TODO"""
        schemas = []
        schemas.extend(KafkaAvroSchema.extensions())
        schemas.extend(KafkaJsonSchema.extensions())
        return ' '.join(schemas)

    def __init__(self):
        # Must come after the initialization above
        super().__init__()
        self.configs = AppConfigs.INSTANCE
        self._started = False
        self._consumer = KafkaConsumer()
        self._consumer.messageConsumed.connect(self._message_consumed)
        self._consumer.messageFailed.connect(self._display_error)
        self._producer = KafkaProducer()
        self._producer.messageProduced.connect(self._message_produced)
        self._producer.messageFailed.connect(self._display_error)
        self._all_settings = {}
        self._last_dir = './src/main/resources/schemas'
        self._all_schemas = defaultdict(None, {})
        self._stats = KafkaStatistics()
        self._stats.statisticsReported.connect(self._update_stats)
        self._stats.start()
        self._capturer = StreamCapturer()
        self._capturer.stderrCaptured.connect(self._console_print_err)
        self._capturer.stdoutCaptured.connect(self._console_print)
        self._display_text(f"Application started at {now()}<br/>{'-' * 45}<br/>")
        self.setup_ui()
        self._load_history()
        list(map(self.ui.lst_cons_settings.set_item, self._all_settings['consumer']))
        list(map(self.ui.lst_prod_settings.set_item, self._all_settings['producer']))
        atexit.register(self._save_history)
        atexit.register(self._capturer.quit)
        self._capturer.start()

    def setup_ui(self) -> None:
        """Connect signals and startup components"""
        self.set_default_font(QFont("DroidSansMono Nerd Font", 14))
        self.window.setWindowTitle(f"Kafman v{'.'.join(self.VERSION)}")
        self.window.resize(1024, 768)
        # General controls
        self.ui.splitter_pane.setSizes([350, 824])
        self.ui.tool_box.setCurrentIndex(self.StkTools.SETTINGS.value)
        self.ui.tab_widget.currentChanged.connect(self._activate_tab)
        self.ui.lbl_status_text.setTextFormat(Qt.RichText)
        self.ui.lbl_status_text.set_elidable(True)
        self.ui.tbtn_test_registry_url.setText(FormIcons.CHECK_CIRCLE.value)
        self.ui.tbtn_test_registry_url.clicked.connect(self._test_registry_url)
        self.ui.cmb_registry_url.lineEdit().editingFinished \
            .connect(lambda: self.ui.tbtn_test_registry_url.setStyleSheet(''))
        self.ui.tbtn_sel_schema.setText(DashboardIcons.FOLDER_OPEN.value)
        self.ui.tbtn_sel_schema.clicked.connect(self._add_schema)
        self.ui.tbtn_desel_schema.setText(FormIcons.CLEAR.value)
        self.ui.tbtn_desel_schema.clicked.connect(self._deselect_schema)
        self.ui.tbtn_del_schema.setText(FormIcons.MINUS.value)
        self.ui.tbtn_del_schema.released.connect(self.ui.cmb_sel_schema.del_item)
        self.ui.cmb_sel_schema.currentTextChanged.connect(self._change_schema)
        self.ui.cmb_registry_url.lineEdit().setPlaceholderText("Type the registry url")
        self.ui.stk_producer_edit.setCurrentIndex(self.StkProducerEdit.TEXT.value)
        self.ui.txt_sel_schema.set_clearable(False)
        # Producer controls
        self.ui.cmb_prod_topics.lineEdit().setPlaceholderText("Select or type comma (,) separated topics")
        self.ui.tbtn_prod_settings_add.clicked.connect(lambda: self.ui.lst_prod_settings.set_item('new.setting'))
        self.ui.tbtn_prod_settings_add.setText(FormIcons.PLUS.value)
        self.ui.tbtn_prod_settings_del.clicked.connect(self._del_setting)
        self.ui.tbtn_prod_settings_del.setText(FormIcons.MINUS.value)
        self.ui.tbtn_prod_connect.clicked.connect(self._toggle_start_producer)
        self.ui.tbtn_prod_connect.setText(DashboardIcons.PLUG_IN.value)
        self.ui.tbtn_prod_connect.setStyleSheet('QToolButton {color: #2380FA;}')
        self.ui.tbtn_produce.clicked.connect(self._produce)
        self.ui.tbtn_produce.setText(DashboardIcons.SEND.value)
        self.ui.tbtn_prod_clear_topics.setText(FormIcons.DELETE.value)
        self.ui.tbtn_prod_add_topics.setText(FormIcons.PLUS.value)
        self.ui.tbtn_prod_add_topics.clicked.connect(self._add_topic)
        self.ui.tbtn_prod_del_topics.setText(FormIcons.MINUS.value)
        self.ui.tbtn_prod_del_topics.clicked.connect(self._del_topic)
        self.ui.lst_prod_settings.currentRowChanged.connect(self._get_setting)
        self.ui.lst_prod_settings.set_editable()
        self.ui.lst_prod_settings.itemChanged.connect(self._edit_setting)
        self.ui.le_prod_settings.editingFinished.connect(self._edit_setting)
        # Consumer controls
        self.ui.cmb_cons_topics.lineEdit().setPlaceholderText("Select or type a new kafka topic")
        self.ui.tbtn_cons_settings_add.clicked.connect(lambda: self.ui.lst_cons_settings.set_item('new.setting'))
        self.ui.tbtn_cons_settings_add.setText(FormIcons.PLUS.value)
        self.ui.tbtn_cons_settings_del.clicked.connect(self._del_setting)
        self.ui.tbtn_cons_settings_del.setText(FormIcons.MINUS.value)
        self.ui.tbtn_cons_connect.clicked.connect(self._toggle_start_consumer)
        self.ui.tbtn_cons_connect.setText(DashboardIcons.PLUG_IN.value)
        self.ui.tbtn_cons_connect.setStyleSheet('QToolButton {color: #2380FA;}')
        self.ui.tbtn_cons_clear_topics.setText(FormIcons.DELETE.value)
        self.ui.tbtn_cons_add_topics.setText(FormIcons.PLUS.value)
        self.ui.tbtn_cons_add_topics.clicked.connect(lambda: self._add_topic(is_producer=False))
        self.ui.tbtn_cons_del_topics.setText(FormIcons.MINUS.value)
        self.ui.tbtn_cons_del_topics.clicked.connect(lambda: self._del_topic(is_producer=False))
        self.ui.lst_cons_settings.currentRowChanged.connect(self._get_setting)
        self.ui.lst_cons_settings.set_editable()
        self.ui.lst_cons_settings.itemChanged.connect(self._edit_setting)
        self.ui.le_cons_settings.editingFinished.connect(self._edit_setting)

    def _is_producer(self) -> bool:
        """Whether started as producer or consumer"""
        return self.ui.tab_widget.currentIndex() == self.Tabs.PRODUCER.value

    def _kafka_type(self) -> str:
        return 'producer' if self._is_producer() else 'consumer'

    def _topics(self, is_producer: bool) -> Optional[List[str]]:
        """Return the selected topics"""
        if is_producer:
            topics = [self.ui.cmb_prod_topics.itemText(i) for i in range(self.ui.cmb_prod_topics.count())]
        else:
            topics = [self.ui.cmb_cons_topics.itemText(i) for i in range(self.ui.cmb_cons_topics.count())]

        return topics if len(topics) > 0 else None

    def _settings(self) -> Optional[dict]:
        """Return the configured settings"""
        settings = self._all_settings[self._kafka_type()]
        return settings if all(s in settings for s in self.REQUIRED_SETTINGS) else None

    def _messages(self) -> List[str]:
        """Return the selected messages"""
        msgs = self.ui.txt_producer.toPlainText().split('\n')
        return list(filter(lambda m: m != '', msgs))

    def _schema(self) -> KafkaSchema:
        """Return the selected AVRO schema"""
        sel_schema = self.ui.cmb_sel_schema.currentText()
        return self._all_schemas[sel_schema] if sel_schema in self._all_schemas else KafkaPlainSchema()

    def _activate_tab(self, index: int = None) -> None:
        """Set the selected tab"""
        index = index if index is not None else self.ui.tab_widget.currentIndex()
        self.ui.tab_widget.setCurrentIndex(index)
        self.ui.stk_settings.setCurrentIndex(index)
        self.ui.stk_statistics.setCurrentIndex(index)

    def _add_schema(self, file_tuple: Tuple[str, str] = None) -> None:
        """Select an AVRO schema from the file picker dialog or from specified file"""
        if not file_tuple:
            file_tuple = QFileDialog.getOpenFileName(
                self.ui.splitter_pane,
                'Open schema', self._last_dir or '.', f"Schema files ({self.supported_schemas()})")
        if file_tuple and file_tuple[0]:
            f_name, f_ext = os.path.splitext(file_tuple[0])
            if KafkaAvroSchema.supports(f_ext):
                avro_schema = KafkaAvroSchema(file_tuple[0])
                self._all_schemas[avro_schema.get_name()] = avro_schema
                self.ui.cmb_sel_schema.set_item(avro_schema.get_name())
                self.ui.cmb_sel_schema.setCurrentText(avro_schema.get_name())
                self._display_text(f"AVRO schema added \"{str(avro_schema)}\"")
            elif KafkaJsonSchema.supports(f_ext):
                json_schema = KafkaJsonSchema(file_tuple[0])
                self._all_schemas[json_schema.get_title()] = json_schema
                self.ui.cmb_sel_schema.set_item(json_schema.get_title())
                self.ui.cmb_sel_schema.setCurrentText(json_schema.get_title())
                self._display_text(f"JSON schema added \"{str(json_schema)}\"")
            else:
                self._display_error(f"Unsupported schema extension \"{f_ext}\"")
            self._last_dir = dirname(file_tuple[0])

    def _deselect_schema(self):
        """Deselect current selected AVRO schema"""
        self.ui.cmb_sel_schema.setCurrentIndex(-1)
        self.ui.stk_producer_edit.setCurrentIndex(self.StkProducerEdit.TEXT.value)

    def _change_schema(self, schema_name: str):
        """Change the current AVRO schema text content"""
        if schema_name:
            content = self._all_schemas[schema_name].get_content()
            self.ui.txt_sel_schema.setText(json.dumps(content, indent=2, sort_keys=False))
            self.ui.stk_producer_edit.setCurrentIndex(self.StkProducerEdit.FORM.value)
            self.ui.tool_box.setCurrentIndex(self.StkTools.SCHEMAS.value)
        else:
            self.ui.txt_sel_schema.setText('')
            self.ui.cmb_sel_schema.setCurrentIndex(-1)
            self.ui.stk_producer_edit.setCurrentIndex(self.StkProducerEdit.TEXT.value)

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
                    self._all_settings[ktype][setting] = ''
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

    def _add_topic(self, topic: str = None, is_producer: bool = True) -> None:
        """Add a topic to the combo box."""
        if is_producer:
            new_topic = self.ui.cmb_prod_topics.currentText()
            if topic or new_topic:
                self.ui.cmb_prod_topics.set_item(topic or new_topic)
                self.ui.cmb_prod_topics.setEditText('')
        else:
            new_topic = self.ui.cmb_cons_topics.currentText()
            if topic or new_topic:
                self.ui.cmb_cons_topics.set_item(topic or new_topic)
                self.ui.cmb_cons_topics.setEditText('')

    def _del_topic(self, is_producer: bool = True) -> None:
        """Delete a topic to the combo box."""
        if is_producer:
            current_text = self.ui.cmb_prod_topics.currentText()
            if current_text:
                self._display_text(f"Topic {current_text} removed from producer")
                self.ui.cmb_prod_topics.removeItem(self.ui.cmb_prod_topics.currentIndex())
        else:
            current_text = self.ui.cmb_cons_topics.currentText()
            if current_text:
                self._display_text(f"Topic {current_text} removed from consumer")
                self.ui.cmb_cons_topics.removeItem(self.ui.cmb_cons_topics.currentIndex())

    def _test_registry_url(self) -> None:
        url = self.ui.cmb_registry_url.currentText()
        if url:
            if is_reachable(url):
                self.ui.tbtn_test_registry_url.setText(FormIcons.CHECK_CIRCLE.value)
                self.ui.tbtn_test_registry_url.setStyleSheet("QToolButton {color: #28C941;}")
                self._display_text(f"Host {url} succeeded", StatusColor.green)
            else:
                self.ui.tbtn_test_registry_url.setText(FormIcons.ERROR.value)
                self.ui.tbtn_test_registry_url.setStyleSheet("QToolButton {color: #FF554D;}")
                self._display_error(f"Host {url} is unreachable")
        else:
            self.ui.tbtn_test_registry_url.setText(FormIcons.UNCHECK_CIRCLE.value)
            self.ui.tbtn_test_registry_url.setStyleSheet("QToolButton {color: #FF554D;}")

    def _toggle_start_producer(self) -> None:
        """Start/Stop the producer."""
        started = self._producer.is_started()
        settings = self._settings()
        if started:  # Stop
            self.ui.tool_box.setCurrentIndex(self.StkTools.SETTINGS.value)
            self._producer.stop_producer()
            self._display_text("Production to kafka topics stopped", StatusColor.yellow)
        else:  # Start
            self._add_topic()
            topics = self._topics(True)
            if topics:
                schema_name = f" using schema \"{str(self._schema())}\"" if self._schema() else ''
                self.ui.tool_box.setCurrentIndex(self.StkTools.STATISTICS.value)
                self._producer.start_producer(settings, self._schema())
                self._display_text(f"Started producing to topics {topics}{schema_name}", StatusColor.green)
            else:
                self._display_error('Must subscribe to at least one topic')
                return
        self.ui.tbtn_produce.setEnabled(not started)
        self.ui.txt_producer.setEnabled(not started)
        self.ui.cmb_prod_topics.setEnabled(started)
        self.ui.tbtn_prod_add_topics.setEnabled(started)
        self.ui.tbtn_prod_del_topics.setEnabled(started)
        self.ui.tbtn_prod_clear_topics.setEnabled(started)
        self.ui.tbtn_prod_connect.setText(DashboardIcons.PLUG_IN.value if started else DashboardIcons.PLUG_OUT.value)
        self.ui.tbtn_prod_connect.setStyleSheet(
            'QToolButton {color: ' + ('#FF554D' if not started else '#2380FA') + ';}')

    def _toggle_start_consumer(self) -> None:
        """Start/Stop the consumer."""
        started = self._consumer.is_started()
        settings = self._settings()
        if started:  # Stop
            self.ui.tool_box.setCurrentIndex(self.StkTools.STATISTICS.value)
            self._consumer.stop_consumer()
            self._display_text("Consumption from kafka topics stopped", StatusColor.yellow)
        else:  # Start
            self._add_topic(is_producer=False)
            topics = self._topics(False)
            if topics:
                schema_name = f" using schema \"{str(self._schema())}\"" if self._schema() else ''
                self.ui.tool_box.setCurrentIndex(self.StkTools.SCHEMAS.value)
                self._consumer.start_consumer(settings, self._schema())
                self._consumer.consume(topics)
                self._display_text(f"Started consuming from topics {topics}{schema_name}", StatusColor.green)
            else:
                self._display_error('Must subscribe to at least one topic')
                return
        self.ui.cmb_cons_topics.setEnabled(started)
        self.ui.tbtn_cons_add_topics.setEnabled(started)
        self.ui.tbtn_cons_del_topics.setEnabled(started)
        self.ui.tbtn_cons_clear_topics.setEnabled(started)
        self.ui.tbtn_cons_connect.setText('O' if started else '-')
        self.ui.tbtn_cons_connect.setText(DashboardIcons.PLUG_IN.value if started else DashboardIcons.PLUG_OUT.value)
        self.ui.tbtn_cons_connect.setStyleSheet(
            'QToolButton {color: ' + ('#FF554D' if not started else '#2380FA') + ';}')

    def _produce(self) -> None:
        """Produce messages to selected kafka topics"""
        messages = self._messages()
        if self._producer.is_started() and len(messages) > 0:
            topics = self._topics(True)
            self._producer.produce(topics, messages)
            self.ui.txt_producer.clear()

    def _display_error(self, message: str, add_console: bool = True) -> None:
        """Display an error at the status bar (and console if required)"""
        self._display_text(message, StatusColor.red, add_console)

    def _display_text(self, message: str, color: QColor = None, add_console: bool = True) -> None:
        """Display a text at the status bar (and console if required)"""
        message = f"<font color='{color.name() if color else 'white'}'>{message}</font>"
        self.ui.lbl_status_text.setText(message)
        if add_console:
            self._console_print(f"-> {message}", color)

    def _update_stats(
        self,
        produced_total: int,
        consumed_total: int,
        produced_in_a_tick: int,
        consumed_in_a_tick: int,
        average_produced: int,
        average_consumed: int) -> None:
        """Update the consumer and producer statistics"""

        self.ui.lbl_stats_produced.setText(str(produced_total))
        self.ui.lbl_stats_produced_ps.setText(str(produced_in_a_tick))
        self.ui.lbl_stats_produced_avg.setText(str(average_produced))
        self.ui.lbl_stats_consumed.setText(str(consumed_total))
        self.ui.lbl_stats_consumed_ps.setText(str(consumed_in_a_tick))
        self.ui.lbl_stats_consumed_avg.setText(str(average_consumed))

    def _message_produced(self, topic: str, partition: int, offset: int, value: str) -> None:
        """Callback when a kafka message has been produced."""
        row = KafkaMessage(now_ms(), topic, partition, offset, value)
        text = f"-> Produced {row}"
        self._console_print(text, StatusColor.blue)
        self._stats.report_produced()
        self._display_text(f"Produced {self._stats.get_in_a_tick()[0]} messages to Kafka", StatusColor.blue, False)

    def _message_consumed(self, topic: str, partition: int, offset: int, value: str) -> None:
        """Callback when a kafka message has been consumed."""
        if not self.ui.tbl_consumer.model():
            HTableModel(self.ui.tbl_consumer, KafkaMessage)
        row = KafkaMessage(now_ms(), topic, partition, offset, value)
        text = f"-> Consumed {row}"
        self.ui.tbl_consumer.model().push_data([row])
        self._console_print(text, StatusColor.orange)
        self._stats.report_consumed()

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
            prod_topics = [self.ui.cmb_prod_topics.itemText(i) for i in range(self.ui.cmb_prod_topics.count())]
            cons_topics = [self.ui.cmb_cons_topics.itemText(i) for i in range(self.ui.cmb_cons_topics.count())]
            schemas = [
                self._all_schemas[self.ui.cmb_sel_schema.itemText(i)].get_filepath()
                for i in range(self.ui.cmb_sel_schema.count())
            ]
            w_size = self.window.width(), self.window.height()
            s_size = self.ui.splitter_pane.sizes()[0], self.ui.splitter_pane.sizes()[1]
            fd_history.write(f"splitter_sizes = {str(s_size)}\n")
            fd_history.write(f"window_size = {str(w_size)}\n")
            fd_history.write(f"prod_topics = {prod_topics}\n")
            fd_history.write(f"cons_topics = {cons_topics}\n")
            fd_history.write(f"settings = {str(self._all_settings)}\n")
            fd_history.write(f"selected_tab = {self.ui.tab_widget.currentIndex()}\n")
            fd_history.write(f"last_dir = {self._last_dir}\n")
            fd_history.write(f"schemas = {schemas}\n")
            fd_history.write(f"last_schema = {self.ui.cmb_sel_schema.currentText()}\n")

    def _load_history(self):
        """Load a previously saved app history."""
        if os.path.exists(self.HISTORY_FILE) and os.stat(self.HISTORY_FILE).st_size > MAX_HISTORY_SIZE_BYTES:
            self._display_text('History recovered')
            with open(self.HISTORY_FILE, 'r') as fd_history:
                lines = fd_history.readlines()
                for line in lines:
                    mat = re.search(r'(.*) ?= ?(.*)', line)
                    if mat:
                        prop_name = mat.group(1).strip()
                        prop_value = mat.group(2).strip()
                        if prop_name == 'prod_topics':
                            list(map(self._add_topic, ast.literal_eval(prop_value)))
                        elif prop_name == 'cons_topics':
                            list(map(lambda p: self._add_topic(p, False), ast.literal_eval(prop_value)))
                        elif prop_name == 'settings':
                            self._all_settings = ast.literal_eval(prop_value)
                        elif prop_name == 'window_size':
                            size = ast.literal_eval(prop_value)
                            self.window.resize(int(size[0]), int(size[1]))
                        elif prop_name == 'splitter_sizes':
                            size = ast.literal_eval(prop_value)
                            self.ui.splitter_pane.setSizes([int(size[0]), int(size[1])])
                        elif prop_name == 'selected_tab':
                            try:
                                self._activate_tab(int(prop_value))
                            except ValueError:
                                self._activate_tab(self.Tabs.PRODUCER.value)
                        elif prop_name == 'last_dir':
                            self._last_dir = prop_value
                        elif prop_name == 'schemas':
                            list(map(lambda s: self._add_schema((s, '')) , ast.literal_eval(prop_value)))
                            self._deselect_schema()
                        elif prop_name == 'last_schema':
                            self.ui.cmb_sel_schema.setCurrentText(prop_value)

        else:
            # Defaults
            self._display_text('History discarded')
            self._add_topic('foobar')
            self._add_topic('foobar', False)
            self._all_settings = {
                'producer': {
                    ProducerConfig.BOOTSTRAP_SERVERS: 'localhost:29092',
                },
                'consumer': {
                    ConsumerConfig.BOOTSTRAP_SERVERS: 'localhost:29092',
                    ConsumerConfig.GROUP_ID: 'kafka_test_group',
                    ConsumerConfig.CLIENT_ID: 'client-1',
                    ConsumerConfig.ENABLE_AUTO_COMMIT: True,
                    ConsumerConfig.SESSION_TIMEOUT_MS: 6000,
                    ConsumerConfig.AUTO_OFFSET_RESET: 'earliest'
                }
            }
            self._activate_tab()
