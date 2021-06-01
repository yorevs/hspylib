#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.test.hspylib.modules.eventbus
      @file: test_eventbus.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import sys
import unittest
from unittest.mock import MagicMock

from hspylib.modules.eventbus.eventbus import EventBus


class TestEventBus(unittest.TestCase):

    def test_should_return_the_same_instance(self):
        bus1 = EventBus.get('test-bus')
        self.assertIsNotNone(bus1)
        bus2 = EventBus.get('test-bus')
        self.assertIsNotNone(bus2)
        self.assertIs(bus1, bus2)

    def test_should_not_return_the_same_instance(self):
        bus1 = EventBus.get('test-bus1')
        self.assertIsNotNone(bus1)
        bus2 = EventBus.get('test-bus2')
        self.assertIsNotNone(bus2)
        self.assertIsNot(bus1, bus2)

    def test_should_invoke_all_callbacks_from_subscribed_events(self):
        bus1 = EventBus.get('test-bus1')
        self.assertIsNotNone(bus1)
        method1 = MagicMock()
        method2 = MagicMock()
        bus1.subscribe('test-event', method1)
        bus1.subscribe('test-event', method2)
        bus1.emit('test-event', age=41, name='hugo')
        method1.assert_called_with({'age': 41, 'name': 'hugo'})
        method2.assert_called_with({'age': 41, 'name': 'hugo'})
        bus1.emit('test-event', age=25, name='jose')
        method1.assert_called_with({'age': 25, 'name': 'jose'})
        method2.assert_called_with({'age': 25, 'name': 'jose'})

    def test_should_not_invoke_callbacks_from_unsubscribed_events(self):
        bus1 = EventBus.get('test-bus1')
        self.assertIsNotNone(bus1)
        method1 = MagicMock()
        method2 = MagicMock()
        bus1.subscribe('test-event-Z', method1)
        bus1.subscribe('test-event-Z', method2)
        bus1.emit('test-event', age=41, name='hugo')
        assert not method1.called
        assert not method2.called


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEventBus)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
