import os
from base_test_case import BaseTestCase
from bifrost.generators import Config


class ConfigGeneratorTestCase(BaseTestCase):
    file_name = 'test.cfg'

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_when_not_passing_any_overrides_default_file_is_generated(self):
        Config.save(self.file_name)

        saved_file = Config.load(self.file_name)
        template = Config.load_from_template()
        self.assertEqual(saved_file, template)


    def test_writes_connection_aws_profile_when_passed_in(self):
        connection_obj = dict(aws_profile='hello')
        Config.save(self.file_name, connection=connection_obj)

        saved_file = Config.load(self.file_name)
        self.assertEqual(saved_file['connection']['aws_profile'], 'hello')

    def test_writes_connection_gateway_when_passed_in(self):
        connection_obj = dict(gateway='user@10.0.0.1')
        Config.save(self.file_name, connection=connection_obj)

        saved_file = Config.load(self.file_name)
        self.assertEqual(saved_file['connection']['gateway'], 'user@10.0.0.1')

    def test_writes_connection_gateway_when_false_passed_in(self):
        connection_obj = dict(gateway=False)
        Config.save(self.file_name, connection=connection_obj)

        saved_file = Config.load(self.file_name)
        self.assertFalse(saved_file['connection']['gateway'])

    def test_writes_connection_instance_username_when_passed_in(self):
        connection_obj = dict(instance_username='david')
        Config.save(self.file_name, connection=connection_obj)

        saved_file = Config.load(self.file_name)
        self.assertEqual(saved_file['connection']['instance_username'], 'david')

    def test_writes_connection_ssh_key_when_passed_in(self):
        connection_obj = dict(ssh_key='~/.aws/conn.pem')
        Config.save(self.file_name, connection=connection_obj)

        saved_file = Config.load(self.file_name)
        self.assertEqual(saved_file['connection']['ssh_key'], '~/.aws/conn.pem')

    def test_write_deployment_base_dir_when_passed_in(self):
        deployment_obj = dict(base_dir='/path/to/something')
        Config.save(self.file_name, deployment=deployment_obj)

        saved_file = Config.load(self.file_name)
        self.assertEqual(saved_file['deployment']['base_dir'], '/path/to/something')

    def test_write_deployment_code_dir_when_passed_in(self):
        deployment_obj = dict(code_dir='relative')
        Config.save(self.file_name, deployment=deployment_obj)

        saved_file = Config.load(self.file_name)
        self.assertEqual(saved_file['deployment']['code_dir'], 'relative')

    def test_write_default_deployment_code_dir_when_not_passed_in(self):
        Config.save(self.file_name)
        saved_file = Config.load(self.file_name)
        self.assertEqual(saved_file['deployment']['code_dir'], 'code')

    def test_write_deployment_venv_when_passed_in(self):
        deployment_obj = dict(venv='env')
        Config.save(self.file_name, deployment=deployment_obj)
        saved_file = Config.load(self.file_name)
        self.assertEqual(saved_file['deployment']['venv'], 'env')

    def test_write_default_deployment_venv_when_not_passed_in(self):
        Config.save(self.file_name)
        saved_file = Config.load(self.file_name)
        self.assertEqual(saved_file['deployment']['venv'], 'venv')
