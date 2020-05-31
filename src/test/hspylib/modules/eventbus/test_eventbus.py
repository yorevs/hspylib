"""
  @package: main.modules.eventbus
  @purpose: Test Suite for EventBus module.
  @created: May 28, 2020
   @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
   @mailto: yorevs@hotmail.com
  @license: Please refer to <https://opensource.org/licenses/MIT>
"""
import sys
import unittest
from unittest.mock import MagicMock

from main.hspylib.modules.eventbus.eventbus import EventBus


class TestEventBus(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

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
        self.method1 = MagicMock()
        self.method2 = MagicMock()
        bus1.subscribe('test-event', self.method1)
        bus1.subscribe('test-event', self.method2)
        bus1.emit('test-event', age=41, name='hugo')
        self.method1.assert_called_with({'age': 41, 'name': 'hugo'})
        self.method2.assert_called_with({'age': 41, 'name': 'hugo'})
        bus1.emit('test-event', age=25, name='jose')
        self.method1.assert_called_with({'age': 25, 'name': 'jose'})
        self.method2.assert_called_with({'age': 25, 'name': 'jose'})

    def test_should_not_invoke_callbacks_from_unsubscribed_events(self):
        bus1 = EventBus.get('test-bus1')
        self.assertIsNotNone(bus1)
        self.method1 = MagicMock()
        self.method2 = MagicMock()
        bus1.subscribe('test-event-Z', self.method1)
        bus1.subscribe('test-event-Z', self.method2)
        bus1.emit('test-event', age=41, name='hugo')
        assert not self.method1.called
        assert not self.method2.called


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEventBus)
    unittest\
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout)\
        .run(suite)
