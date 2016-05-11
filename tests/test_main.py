"""
Tests for Bifrost main module
"""
import fudge
from base_test_case import BaseTestCase
from bifrost.main import deploy


class MainTestCase(BaseTestCase):
    @fudge.patch('bifrost.main.query_yes_no',
                 'bifrost.main.subprocess',
                 'bifrost.main.load_config')
    def test_deploy_aborts_when_no_supplied(self, fake_yes_no, fake_subprocess, mock_config):
        mock_config.expects_call().returns(dict(dvcs='hg'))
        fake_yes_no.expects_call().returns(False)
        fake_subprocess.provides('call').returns(False)

        deploy('test', False, False, None)

    @fudge.patch('bifrost.main.query_yes_no',
                 'bifrost.main.subprocess',
                 'bifrost.main.load_config')
    def test_deploy_requests_user_confirmation_before_continuing_by_default(self, fake_yes_no, fake_subprocess, mock_config):
        mock_config.expects_call().returns(dict(dvcs='hg'))
        fake_yes_no.expects_call().returns(True)
        fake_subprocess.expects('call').returns(True)

        deploy('test', False, False, None)

    @fudge.patch('bifrost.main.subprocess', 'bifrost.main.load_config')
    def test_deploy_skips_user_confirmation_when_no_input_supplied(self, fake_subprocess, mock_config):
        mock_config.expects_call().returns(dict(dvcs='hg'))
        fake_subprocess.expects('call').returns(True)

        deploy('test', False, True, None)

    @fudge.patch('bifrost.main.subprocess', 'bifrost.main.load_config')
    def test_picks_up_default_branch_for_git_dvcs(self, fake_subprocess, mock_config):
        mock_config.expects_call().returns(dict(dvcs='git'))
        cmd = [u'fab', u'setup:config=test', u'deploy:branch=master']
        fake_subprocess.expects('call').with_args(cmd).returns(False)
        deploy('test', False, True, None)


    @fudge.patch('bifrost.main.subprocess', 'bifrost.main.load_config')
    def test_picks_up_default_branch_for_mercurial_dvcs(self, fake_subprocess, mock_config):
        mock_config.expects_call().returns(dict(dvcs='hg'))
        cmd = [u'fab', u'setup:config=test', u'deploy:branch=default']
        fake_subprocess.expects('call').with_args(cmd).returns(False)
        deploy('test', False, True, None)
