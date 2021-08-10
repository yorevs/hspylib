#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   IP Message Sender. Sends TCP/UDP messages (multi-threaded).

   @project: HSPyLib
   @package: hspylib.main.hspylib.addons.widman.widgets
      @file: widget_send_msg.py
   @created: Thu, 26 Aug 2017
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
import argparse
import os
import signal
import socket
import threading
from time import sleep

from hspylib.addons.widman.widget import Widget
from hspylib.core.enums.exit_code import ExitCode
from hspylib.core.exception.exceptions import WidgetExecutionError
from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.icons.font_awesome.widget_icons import WidgetIcons
from hspylib.modules.cli.tui.extra.minput.input_validator import InputValidator
from hspylib.modules.cli.tui.extra.minput.minput import MenuInput, minput
from hspylib.modules.cli.tui.menu.menu_utils import MenuUtils


class WidgetSendMsg(Widget):
    """HSPyLib to send TCP/UDP messages (multi-threaded)"""
    WIDGET_ICON = WidgetIcons.NETWORK
    WIDGET_NAME = "SendMsg"
    TOOLTIP = "IP Message Sender. Sends TCP/UDP messages (multi-threaded)"
    VERSION = (0, 3, 0)
    MAX_THREADS = 1000
    NET_TYPE_UDP = 'UDP'
    NET_TYPE_TCP = 'TCP'

    # Help message to be displayed by the application.
    USAGE = """Usage: SendMsg [options]

  Options:
    -n, --net_type   <network_type>     : The network type to be used. Either UDP or TCP ( default is TCP ).
    -p, --port       <port_num>         : The port number [1-65535] ( default is 12345).
    -a, --address    <host_address>     : The address of the datagram receiver ( default is 127.0.0.1 ).
    -k, --packets    <num_packets>      : The number of max datagrams to be send. If zero is specified, then the app
                                          is going to send indefinitely ( default is 100 ).
    -i, --interval   <interval_MS>      : The interval in seconds between each datagram ( default is 1 Second ).
    -t, --threads    <threads_num>      : Number of threads [1-{}] to be opened to send simultaneously ( default is 1 ).
    -m, --message    <message/filename> : The message to be sent. If the message matches a filename, then the file
                                          contents sent instead.

    E.g:. send-msg.py -m "Hello" -p 12345 -a 0.0.0.0 -k 100 -i 500 -t 2
""".format(MAX_THREADS)

    def __init__(self):
        super().__init__(
            self.WIDGET_ICON,
            self.WIDGET_NAME,
            self.TOOLTIP,
            self.USAGE,
            self.VERSION)

        self.is_alive = True
        self.net_type = None
        self.host = None
        self.packets = None
        self.interval = None
        self.threads = None
        self.message = None
        self.args = None
        self.socket = None

    def execute(self, *args) -> ExitCode:
        ret_val = ExitCode.SUCCESS
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)

        if args and args[0] in ['-h', '--help']:
            sysout(self.usage())
            return ExitCode.SUCCESS
        if args and args[0] in ['-v', '--version']:
            sysout(self.version())
            return ExitCode.SUCCESS

        if not args:
            if not args and not self._read_args():
                return ExitCode.ERROR
        else:
            if not self._parse_args(*args):
                return ExitCode.ERROR

        self.net_type = self.args.net_type or self.NET_TYPE_TCP
        self.host = (self.args.address or '127.0.0.1', self.args.port or 12345)
        self.packets = self.args.packets or 100
        self.interval = self.args.interval or 1
        self.threads = self.args.threads or 1

        if self.args.message and os.path.isfile(self.args.message):
            file_size = os.stat(self.args.message).st_size
            sysout(f"Reading contents from file: {self.args.message} ({file_size}) [Bs] instead")
            with open(self.args.message, 'r') as f_msg:
                self.message = f_msg.read()
        else:
            self.message = self.args.message or f"This is a {self.args.net_type} test"

        self._start_send()

        MenuUtils.wait_enter()

        return ret_val

    def cleanup(self) -> None:
        sysout('Terminating threads%NC%')
        self.is_alive = False
        if self.net_type == self.NET_TYPE_TCP:
            sysout('Closing TCP connection')
            self.socket.close()

    def _read_args(self) -> bool:
        """When no input is provided (e.g:. when executed from dashboard). Prompt the user for the info. """
        # @formatter:off
        form_fields = MenuInput.builder() \
            .field() \
                .label('Net Type') \
                .itype('select') \
                .value(f"{self.NET_TYPE_TCP}|{self.NET_TYPE_UDP}") \
                .build() \
            .field() \
                .label('Address') \
                .validator(InputValidator.anything()) \
                .value('127.0.0.1') \
                .build() \
            .field() \
                .label('Port') \
                .validator(InputValidator.numbers()) \
                .min_max_length(2, 5) \
                .value(12345) \
                .build() \
            .field() \
                .label('Packets') \
                .validator(InputValidator.numbers()) \
                .min_max_length(1, 4) \
                .value(100) \
                .build() \
            .field() \
                .label('Interval') \
                .validator(InputValidator.numbers()) \
                .min_max_length(1, 4) \
                .value(1) \
                .build() \
            .field() \
                .label('Threads') \
                .validator(InputValidator.numbers()) \
                .min_max_length(1, 4) \
                .value(1) \
                .build() \
            .field() \
                .label('Message') \
                .validator(InputValidator.anything()) \
                .min_max_length(1, 40) \
                .value('This is a test') \
                .build() \
            .build()
        # @formatter:on
        self.args = minput(form_fields)

        return len(self.args.__dict__) > 1

    def _parse_args(self, *args):
        """When arguments are passed from the command line, parse them"""
        parser = argparse.ArgumentParser(description='Sends TCP/UDP messages (multi-threaded)')
        parser.add_argument(
            '--net-type', action='store', type=str, required=False,
            help='The network type to be used. Either UDP or TCP ( default is TCP )')
        parser.add_argument(
            '--address', action='store', type=str, required=False,
            help='The address of the datagram receiver ( default is 127.0.0.1 )')
        parser.add_argument(
            '--port', action='store', type=int, required=False,
            help='The port number [1-65535] ( default is 12345)')
        parser.add_argument(
            '--packets', action='store', type=int, required=False,
            help='The number of max datagrams to be send. If zero is specified, then the app '
                 'is going to send indefinitely ( default is 100 ).')
        parser.add_argument(
            '--interval', action='store', type=float, required=False,
            help='The interval in seconds between each datagram ( default is 1 Second )')
        parser.add_argument(
            '--threads', action='store', type=int, required=False,
            help=f'Number of threads [1-{self.MAX_THREADS}] to be opened to send simultaneously ( default is 1 )')
        parser.add_argument(
            '--message', action='store', type=str, required=False,
            help='The message to be sent. If the message matches a filename, then the file contents sent instead')
        self.args = parser.parse_args(args)

        return bool(self.args)

    def _init_sockets(self) -> None:
        """Initialize sockets"""
        if self.net_type == self.NET_TYPE_UDP:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.socket.connect(self.host)
                sysout(f"Successfully connected to {self.host}")
            except socket.error as err:
                raise WidgetExecutionError('Unable to initialize sockets') from err

    def _start_send(self) -> None:
        """Start sending packets"""
        thread_relief = 0.25
        self._init_sockets()
        sysout(f"\n%ORANGE%Start sending {self.packets} "
               f"{self.net_type.upper()} packet(s) "
               f"every {self.interval} second(s) to {self.host} using {self.threads} thread(s)")
        threads_num = threading.active_count()

        for thread_num in range(1, int(self.threads) + 1):
            tr = threading.Thread(target=self._send_packet, args=(thread_num,))
            tr.setDaemon(True)
            tr.start()
            sleep(thread_relief)

        while self.is_alive and threading.active_count() > threads_num:
            sleep(2 * thread_relief)

    def _send_packet(self, thread_num: int) -> None:
        """Send a packet"""
        counter = 1
        length = len(self.message)

        while self.is_alive and self.packets <= 0 or counter <= self.packets:
            sysout(f"%BLUE%[Thread-{thread_num:d}] "
                   f"%GREEN%Sending \"{self.message:s}\" ({length:d}) bytes, "
                   f"Pkt = {counter:>d}/{self.packets:>d} %NC%...")
            if self.net_type == self.NET_TYPE_UDP:
                self.socket.sendto(self.message.encode(), self.host)
            else:
                try:
                    self.socket.sendall((self.message + '\n').encode())
                except socket.error as err:
                    raise WidgetExecutionError('Unable to send packet') from err
            counter += 1
            sleep(self.interval)
