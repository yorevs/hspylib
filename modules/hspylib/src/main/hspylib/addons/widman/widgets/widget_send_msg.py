#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.addons.widman.widgets
      @file: widget_send_msg.py
   @created: Thu, 26 Aug 2017
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import os
import socket
import threading
from textwrap import dedent
from time import sleep
from typing import List

from hspylib.addons.widman.widget import Widget
from hspylib.core.exception.exceptions import WidgetExecutionError
from hspylib.core.tools.commons import hook_exit_signals, sysout
from hspylib.modules.application.argparse.argument_parser import HSArgumentParser
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.application.version import Version
from hspylib.modules.cli.icons.font_awesome.widget_icons import WidgetIcons
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.tui.minput.input_validator import InputValidator
from hspylib.modules.cli.tui.minput.minput import MenuInput, minput


class WidgetSendMsg(Widget):
    """HSPyLib Widget to send TCP/UDP messages (multi-threaded)"""

    # fmt: off
    MAX_THREADS     = 1000
    NET_TYPE_UDP    = "UDP"
    NET_TYPE_TCP    = "TCP"

    WIDGET_ICON     = WidgetIcons.NETWORK
    WIDGET_NAME     = "SendMsg"
    VERSION         = Version(0, 3, 0)
    TOOLTIP         = "Multi-Threaded IP Message Sender. Sends TCP/UDP messages"
    USAGE           = dedent(f"""Usage: SendMsg [options]

      Options:
        +n, ++net_type   <network_type>     : The network type to be used. Either udp or tcp ( default is tcp ).
        +p, ++port       <port_num>         : The port number [1-65535] ( default is 12345).
        +a, ++address    <host_address>     : The address of the datagram receiver ( default is 127.0.0.1 ).
        +k, ++packets    <num_packets>      : The number of max datagrams to be send. If zero is specified, then the app
                                              is going to send indefinitely ( default is 100 ).
        +i, ++interval   <interval_MS>      : The interval in seconds between each datagram ( default is 1 Second ).
        +t, ++threads    <threads_num>      : Number of threads [1-{MAX_THREADS}] to be opened to send simultaneously
                                              ( default is 1 ).
        +m, ++message    <message/filename> : The message to be sent. If the message matches a filename, then the file
                                              contents sent instead.

        E.g:. send-msg.py +n tcp +m "Hello" +p 12345 +a 0.0.0.0 +k 100 +i 500 +t 2
    """)
    # fmt: on

    def __init__(self) -> None:
        super().__init__(self.WIDGET_ICON, self.WIDGET_NAME, self.TOOLTIP, self.USAGE, self.VERSION)
        self.is_alive = True
        self.net_type = None
        self.host = None
        self.packets = None
        self.interval = None
        self.threads = None
        self.message = None
        self._args = None
        self.socket = None
        self.counter = 1

    def execute(self, args: List[str] = None) -> ExitStatus:
        hook_exit_signals(self.cleanup)
        if args and args[0] in ["-h", "--help"]:
            sysout(self.usage())
            return ExitStatus.SUCCESS
        if args and args[0] in ["-v", "--version"]:
            sysout(self.version())
            return ExitStatus.SUCCESS
        if args and not self._parse_args(args):
            return ExitStatus.ERROR
        if not args and not self._prompt():
            return ExitStatus.ERROR
        if not args and not self._args:
            return ExitStatus.ERROR

        self.net_type = self._args.net_type or self.NET_TYPE_TCP
        self.host = (self._args.address or "127.0.0.1", self._args.port or 12345)
        self.packets = self._args.packets or 100
        self.interval = self._args.interval or 1
        self.threads = self._args.threads or 1

        if self._args.message and os.path.isfile(self._args.message):
            file_size = os.stat(self._args.message).st_size
            sysout(f"Reading contents from file: {self._args.message} ({file_size}) [Bs] instead")
            with open(self._args.message, "r", encoding="utf-8") as f_msg:
                self.message = f_msg.read()
        else:
            self.message = self._args.message or f"This is a {self._args.net_type} test %(count)"

        self._start_send()

        Keyboard.wait_keystroke()

        return ExitStatus.SUCCESS

    def cleanup(self) -> None:
        """Stops workers and close socket connection."""
        sysout("Terminating threads%NC%")
        self.is_alive = False
        if self.net_type == self.NET_TYPE_TCP:
            sysout("Closing TCP connection")
            self.socket.close()

    def _prompt(self) -> bool:
        """When no input is provided (e.g:. when executed from dashboard). Prompt the user for the info."""
        # fmt: off
        form_fields = MenuInput.builder() \
            .field() \
                .label('Net Type') \
                .itype('select') \
                .value(f"{self.NET_TYPE_TCP}|{self.NET_TYPE_UDP}") \
                .build() \
            .field() \
                .label('Address') \
                .validator(InputValidator.custom(r"^([0-9]{0,3}){0,1}(\.[0-9]{0,3}){0,3}$")) \
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
        # fmt: on
        self._args = minput(form_fields)
        sysout("%HOM%%ED2%%MOD(0)%", end="")

        return len(self._args) > 1 if self._args else False

    def _parse_args(self, args: List[str]):
        """When arguments are passed from the command line, parse them"""
        parser = HSArgumentParser(
            prog="sendmsg", prefix_chars="+", description="Sends TCP/UDP messages (multi-threaded)"
        )
        # fmt: off
        parser.add_argument(
            "+n", "++net-type", action="store", choices=["udp", "tcp"],
            type=str, default="tcp", required=False,
            help="The network type to be used. Either udp or tcp ( default is tcp )",
        )
        parser.add_argument(
            "+a", "++address", action="store",
            type=str, default="127.0.0.1", required=False,
            help="The address of the datagram receiver ( default is 127.0.0.1 )",
        )
        parser.add_argument(
            "+p", "++port", action="store",
            type=int, default=12345, required=False,
            help="The port number [1-65535] ( default is 12345)",
        )
        parser.add_argument(
            "+k", "++packets", action="store",
            type=int, default=100, required=False,
            help="The number of max datagrams to be send. If zero is specified, then the app "
                 "is going to send indefinitely ( default is 100 ).",
        )
        parser.add_argument(
            "+i", "++interval", action="store",
            type=float, default=1, required=False,
            help="The interval in seconds between each datagram ( default is 1 Second )",
        )
        parser.add_argument(
            "+t", "++threads", action="store",
            type=int, default=1, required=False,
            help=f"Number of threads [1-{self.MAX_THREADS}] to be opened to send simultaneously ( default is 1 )",
        )
        parser.add_argument(
            "+m", "++message", action="store",
            type=str, required=False,
            help="The message to be sent. If the message matches a filename, then the file contents sent instead",
        )
        # fmt: on
        self._args = parser.parse_args(args)

        return bool(self._args)

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
                raise WidgetExecutionError("Unable to initialize sockets") from err

    def _start_send(self) -> None:
        """Start sending packets"""
        thread_relief = 0.05
        self._init_sockets()
        sysout(
            f"\n%ORANGE%Start sending {self.packets} "
            f"{self.net_type.upper()} packet(s) "
            f"every {self.interval} second(s) to {self.host} using {self.threads} thread(s)"
        )
        threads_num = threading.active_count()

        for thread_num in range(1, int(self.threads) + 1):
            tr = threading.Thread(target=self._send_packet, args=(thread_num,))
            tr.daemon = True
            tr.start()
            sleep(thread_relief)

        while self.is_alive and threading.active_count() > threads_num:
            sleep(2 * thread_relief)

    def _send_packet(self, thread_num: int) -> None:
        """Send a packet"""
        lock = threading.Lock()

        while self.is_alive and self.packets <= 0 or self.counter <= self.packets:
            message = self.message.replace("%(count)", str(self.counter))
            length = len(message)
            sysout(
                f"%BLUE%[Thread-{thread_num:d}] "
                f'%GREEN%Sending "{message:s}" ({length:d}) bytes, '
                f"Pkt = {self.counter:>d}/{self.packets:>d} %NC%..."
            )
            if self.net_type == self.NET_TYPE_UDP:
                self.socket.sendto(message.encode(), self.host)
            else:
                try:
                    self.socket.sendall((message + "\n").encode())
                    with lock:
                        self.counter += 1
                except socket.error as err:
                    raise WidgetExecutionError("Unable to send packet") from err
            sleep(self.interval)
