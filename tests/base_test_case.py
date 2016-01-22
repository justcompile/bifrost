import unittest


class BaseTestCase(unittest.TestCase):
    def assertIn(self, member, container, msg=None):
        if hasattr(unittest.TestCase, 'assertIn') and callable(getattr(unittest.TestCase, 'assertIn', None)):
            super(BaseTestCase, self).assertIn(member, container, msg)
        else:
            self.assertTrue(member in container,
                            msg="{item} not found in {iterable}"
                                 .format(item=member,
                                         iterable=container))
