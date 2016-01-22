import unittest


class BaseTestCase(unittest.TestCase):
    def assertIn(self, member, container, msg=None):
        print "OMG DO SOMETHING"
        if hasattr(unittest.TestCase, 'assertIn') and callable(getattr(unittest.TestCase, 'assertIn', None)):
            print 'Calling super'
            super(BaseTestCase, self).assertIn(member, container, msg)
        else:
            print 'meh'
            self.assertTrue(member in container,
                            msg="{item} not found in {iterable}"
                                 .format(item=member,
                                         iterable=container))
