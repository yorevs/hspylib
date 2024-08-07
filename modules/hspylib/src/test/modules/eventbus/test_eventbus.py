#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   test.modules.eventbus
      @file: test_eventbus.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""

from hspylib.modules.eventbus.event import Event
from hspylib.modules.eventbus.eventbus import emit, EventBus, subscribe
from unittest.mock import MagicMock

import sys
import unittest


class TestEventBus(unittest.TestCase):
    def test_should_return_the_same_instance(self) -> None:
        bus1 = EventBus.get("test-bus")
        self.assertIsNotNone(bus1)
        bus2 = EventBus.get("test-bus")
        self.assertIsNotNone(bus2)
        self.assertIs(bus1, bus2)

    def test_should_not_return_the_same_instance(self) -> None:
        bus1 = EventBus.get("test-bus1")
        self.assertIsNotNone(bus1)
        bus2 = EventBus.get("test-bus2")
        self.assertIsNotNone(bus2)
        self.assertIsNot(bus1, bus2)

    def test_should_invoke_all_callbacks_from_subscribed_events(self) -> None:
        expected_ev1 = Event("test-event", age=41, name="hugo")
        expected_ev2 = Event("test-event", age=25, name="jose")
        bus1 = EventBus.get("test-bus1")
        self.assertIsNotNone(bus1)
        method1 = MagicMock()
        method2 = MagicMock()
        bus1.subscribe("test-event", method1)
        bus1.subscribe("test-event", method2)
        bus1.emit("test-event", age=41, name="hugo")
        method1.assert_called_with(expected_ev1)
        method2.assert_called_with(expected_ev1)
        bus1.emit("test-event", age=25, name="jose")
        method1.assert_called_with(expected_ev2)
        method2.assert_called_with(expected_ev2)

    def test_should_not_invoke_callbacks_from_unsubscribed_events(self) -> None:
        bus1 = EventBus.get("test-bus1")
        self.assertIsNotNone(bus1)
        method1 = MagicMock()
        method2 = MagicMock()
        bus1.subscribe("test-event-Z", method1)
        bus1.subscribe("test-event-Z", method2)
        bus1.emit("test-event", age=41, name="hugo")
        self.assertFalse(method1.called, "Callback was invoked and should not")
        self.assertFalse(method2.called, "Callback was invoked and should not")

    def test_should_subscribe_and_invoke_callback_using_decorator(self) -> None:
        method1 = MagicMock()
        method2 = MagicMock()

        @subscribe(bus="test-bus1", events="test-event-Z")
        def method_1(ev) -> None:
            self.assertEqual("test", ev.args.name)
            self.assertEqual(1, ev.args.status)
            method1()

        @subscribe(bus="test-bus1", events="test-event-Z")
        def method_2(ev) -> None:
            self.assertEqual("test", ev.args.name)
            self.assertEqual(1, ev.args.status)
            method2()

        emit("test-bus1", "test-event-Z", name="test", status=1)
        self.assertTrue(method1.called, "Callback 'method1' was not invoked")
        self.assertTrue(method2.called, "Callback 'method2' was not invoked")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEventBus)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
