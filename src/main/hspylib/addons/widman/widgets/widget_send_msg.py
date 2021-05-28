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
import signal
import socket
import threading
from time import sleep

from hspylib.addons.widman.widget import Widget
from hspylib.core.enums.exit_code import ExitCode
from hspylib.core.exception.exceptions import WidgetExecutionError
from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.icons.font_awesome.widget_icons import WidgetIcons
from hspylib.modules.cli.menu.menu_utils import MenuUtils


class WidgetSendMsg(Widget):

    WIDGET_ICON  = WidgetIcons.NETWORK
    WIDGET_NAME = "SendMsg"
    TOOLTIP = "IP Message Sender. Sends TCP/UDP messages (multi-threaded)"
    VERSION = (0, 3, 0)
    MAX_THREADS = 1000
    NET_TYPE_UDP = 'UDP'
    NET_TYPE_TCP = 'TCP'
    MAX_DISP_LEN = 500

    # Help message to be displayed by the application.
    USAGE = """
IP Message Sender v{}

Usage: SendMsg [options]

  Options:
    -m, --message    <message/filename> : The message to be sent. If the message matches a filename, then the
                                          file is read and the content sent instead.
    -p, --port       <port_num>         : The port number [1-65535] ( default is 12345).
    -a, --address    <host_address>     : The address of the datagram receiver ( default is 127.0.0.1 ).
    -k, --packets    <num_packets>      : The number of max datagrams to be send. If zero is specified, then the app
                                          is going to send indefinitely ( default is 100 ).
    -i, --interval   <interval_MS>      : The interval between each datagram ( default is 1 Second ).
    -t, --threads    <threads_num>      : Number of threads [1-{}] to be opened to send simultaneously ( default is 1 ).
    -n, --net_type    <network_type>     : The network type to be used. Either UDP or TCP ( default is TCP ).

    E.g:. send-msg.py -m "Hello" -p 12345 -a 0.0.0.0 -k 100 -i 500 -t 2
""".format(str(VERSION), MAX_THREADS)


    def __init__(self):
        super().__init__(
            self.WIDGET_ICON,
            self.WIDGET_NAME,
            self.TOOLTIP,
            self.USAGE,
            self.VERSION)

        self.is_alive = True
        self.net_type = self.NET_TYPE_TCP
        self.host = ('127.0.0.1', 12345)
        self.packets = 100
        self.interval = 1.0
        self.threads = 1
        self.message = '{} SendMsg SELF TEST'.format(self.net_type)
        self.args = None

        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)
        self._init_sockets()


    def execute(self, *args) -> ExitCode:

        ret_val = ExitCode.SUCCESS

        if (not args or len(args) < 3) and not any(a in args for a in ['-h', '--help']):
            if not self._read_args():
                return ExitCode.ERROR
        elif args[0] in ['-h', '--help']:
            sysout(self.usage())
            return ExitCode.SUCCESS

        if not self.args:
            self.args = args

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
        return True

    def _init_sockets(self) -> None:
        if self.net_type == self.NET_TYPE_UDP:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.socket.connect(self.host)
            except socket.error as err:
                raise WidgetExecutionError('Unable to initialize sockets') from err

    def _start_send(self) -> None:

        sysout('\n%ORANGE%Start sending {} packets every {} seconds: max. of[{}] to {}. Threads = {}%NC%'.format(
            self.net_type, self.interval, self.packets, self.host, self.threads))
        threads_num = threading.active_count()

        for i in range(1, self.threads + 1):
            tr = threading.Thread(target=self._send_packet, args=(i,))
            tr.setDaemon(True)
            tr.start()
            sleep(0.011)

        while self.is_alive and threading.active_count() > threads_num:
            sleep(0.50)

    def _send_packet(self, i) -> None:

        counter = 1
        length = len(self.message)

        while self.is_alive and self.packets <= 0 or counter <= self.packets:
            sysout(f"%BLUE%[Thread-{i:02d}] "
                   f"%GREEN%Sending [{length:d}] bytes, "
                   f"Pkt = {counter:d}/{self.packets:d} %NC%...")
            if self.net_type == self.NET_TYPE_UDP:
                self.socket.sendto(self.message.encode(), self.host)
            else:
                try:
                    self.socket.sendall((self.message + '\n').encode())
                except socket.error as err:
                    raise WidgetExecutionError('Unable to send packet') from err
            counter += 1
            sleep(self.interval)
