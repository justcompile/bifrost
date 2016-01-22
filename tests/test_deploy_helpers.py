import unittest
from bifrost.deploy import helpers


class DeployHelpersTestCase(unittest.TestCase):
    def test_raises_error_when_config_has_no_roles_key(self):
        self.assertRaises(AssertionError, helpers.generate_fabric_roles, {})
