import unittest
from bifrost.helpers import deploy


class DeployHelpersTestCase(unittest.TestCase):
    def test_raises_error_when_config_has_no_roles_key(self):
        self.assertRaises(AssertionError, deploy.generate_fabric_roles, {})
