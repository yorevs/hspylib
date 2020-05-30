"""
  @package: main.modules.eventbus
  @purpose: Test Suite for EventBus module.
  @created: May 28, 2020
   @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
   @mailto: yorevs@hotmail.com
  @license: Please refer to <https://opensource.org/licenses/MIT>
"""

import unittest


class TestEventBus(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_case_1(self):
        pass


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEventBus)
    unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)
