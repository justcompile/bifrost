import os
import unittest
from bifrost.main import generate_fab_file


class GeneratorTestCase(unittest.TestCase):
    file_name = 'test.fab'

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_can_generate_placeholder_fab_file(self):
        generate_fab_file(self.file_name)
        self.assertTrue(os.path.exists(self.file_name))

    def test_can_generate_fab_file_with_deploy_task(self):
        generate_fab_file(self.file_name)

        signature = "def deploy(branch, install_pkgs=False):"

        self.assertIn(signature, self.__read_file())

    def test_can_generate_fab_file_with_deploy_role1_task(self):
        generate_fab_file(self.file_name)

        signature = "@roles('role1')\ndef deploy_role1(branch, install_pkgs=False):"

        self.assertIn(signature, self.__read_file())

    def test_can_generate_fab_file_with_deploy_role2_task(self):
        generate_fab_file(self.file_name)

        signature = "@roles('role2')\ndef deploy_role2(branch, install_pkgs=False):"

        self.assertIn(signature, self.__read_file())

    def __read_file(self):
        with open(self.file_name, 'r') as fp:
            return fp.read()
