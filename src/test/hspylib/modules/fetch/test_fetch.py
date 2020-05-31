import sys
import unittest

from main.hspylib.modules.fetch.fetch import get


class TestEventBus(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_get_from_example_com(self):
        resp = get('http://example.com')
        self.assertIsNotNone(resp)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEventBus)
    unittest\
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout)\
        .run(suite)
