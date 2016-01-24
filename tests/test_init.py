import os
import fudge
from base_test_case import BaseTestCase
from bifrost.main import init


class InitTestCase(BaseTestCase):
    file_name = 'test.fab'

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    @fudge.patch('os.path.exists')
    def test_if_file_exists_exit(self, fake_exists):
        fake_exists.expects_call().returns(True)
        self.assertRaises(SystemExit, init, self.file_name)

    @fudge.patch('__builtin__.raw_input',
                'os.path.exists',
                'bifrost.aws.AWSProfile.exists',
                'bifrost.generators.Config.load_from_template')
    def test_will_skip_aws_creds_if_profile_exists(self,
                                                    fake_input,
                                                    fake_exists,
                                                    FakeSession,
                                                    fake_load_from_tmpl):
        profile_name = '<profile_name>'
        fake_exists.expects_call().returns(False)
        fake_input.expects_call().returns(profile_name)
        FakeSession.expects_call().with_args(profile_name).returns(True)
        fake_load_from_tmpl.expects_call().returns({})

        init(self.file_name)


    @fudge.patch('__builtin__.raw_input',
                'os.path.exists',
                'bifrost.aws.AWSProfile.exists')
    def test_will_exit_if_profile_doesnt_exist_but_user_enters_no(self,
                                                            fake_input,
                                                            fake_exists,
                                                            FakeSession):
        profile_name = '<profile_name>'
        fake_exists.expects_call().returns(False)
        fake_input.expects_call().returns(profile_name)
        FakeSession.expects_call().with_args(profile_name).returns(False)
        fake_input.next_call().returns('n')

        self.assertRaises(SystemExit, init, self.file_name)

    @fudge.patch('__builtin__.raw_input',
                'os.path.exists',
                'bifrost.aws.AWSProfile.exists',
                'bifrost.generators.Config.load_from_template')
    def test_will_request_aws_creds_if_profile_doesnt_exist(self,
                                                            fake_input,
                                                            fake_exists,
                                                            FakeSession,
                                                            fake_load_tmpl):
        profile_name = '<profile_name>'
        key = '<key>'
        secret = '<secret>'

        fake_exists.expects_call().returns(False)
        fake_input.expects_call().returns(profile_name)
        FakeSession.expects_call().with_args(profile_name).returns(False)
        fake_input.next_call().returns('y')
        fake_input.next_call().returns(key)
        fake_input.next_call().returns(secret)
        fake_load_tmpl.expects_call().returns({})

        init(self.file_name)


    @fudge.patch('__builtin__.raw_input',
                'os.path.exists',
                'bifrost.aws.AWSProfile.exists',
                'bifrost.aws.AWSProfile._get_file_path',
                'bifrost.generators.Config.load_from_template')
    def test_will_request_aws_creds_if_profile_doesnt_exist_save_to_file(self,
                                                                        fake_input,
                                                                        fake_exists,
                                                                        fake_profile_exists,
                                                                        fake_get_file_path,
                                                                        fake_load_from_tmpl):
        profile_name = '<profile_name>'
        key = '<key>'
        secret = '<secret>'

        fake_exists.expects_call().returns(False)
        fake_input.expects_call().returns(profile_name)
        fake_profile_exists.expects_call().with_args(profile_name).returns(False)
        fake_input.next_call().returns('y')
        fake_input.next_call().returns(key)
        fake_input.next_call().returns(secret)
        fake_get_file_path.expects_call().returns('my_creds')
        fake_load_from_tmpl.expects_call().returns({})

        init(self.file_name)

        with(open('my_creds')) as fp:
            lines = fp.readlines()

        self.assertEqual(len(lines), 4)
        self.assertEqual(lines[0], '[{}]\n'.format(profile_name))
        self.assertEqual(lines[1], 'aws_access_key_id = {}\n'.format(key))
        self.assertEqual(lines[2], 'aws_secret_access_key = {}\n'.format(secret))

        os.remove('my_creds')
