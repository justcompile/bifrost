from fabric.api import roles, execute, abort, env, sudo
from fabric.context_managers import cd
from fabric.contrib.console import confirm
from fabric.decorators import runs_once
from fabric.operations import local, run
from bifrost.deploy import helpers


# connection: contains connection information for Fabric and AWS details
# deployment: The location of where the codebase will reside on the server
# repository: The location of where the repository has been checked out to on the server in question]
# roles: Any number of roles using the role name; such as "web" and then any boto ec2 filter queries to determine which instances to retreive
CONFIG = {
    'connection': {
        'gateway': 'user@ipaddress', # OMIT if not required
        'regions': ['eu-west-1'],
        'aws_profile': 'reservoir', # The AWS credentials profile to use, omit to use default
        'instance_username': 'ubuntu',
        'ssh_key':  '~/.aws/live.pem'
    },
    'deployment': {
        'base_dir': '/srv/mgr',
        'code_dir': 'code',
        'venv': 'venv'
    },
    'repository': '',
    'roles': {
        'web': {
            'tag-key': 'my-web-tag'
        },
        'worker': {
            'tag-key': 'my-worker-tag'
        }
    }
}

def setup():
    if CONFIG['connection'].get('gateway'):
        env.gateway = CONFIG['connection'].get('gateway')

    env.roledefs = helpers.generate_fabric_roles(CONFIG)
    env.key_filename = CONFIG['connection']['ssh_key']


@roles('role1')
def deploy_role1(branch, install_pkgs=False):
    pass

@roles('role2')
def deploy_role2(branch, install_pkgs=False):
    pass

def deploy(branch, install_pkgs=False):
    execute(deploy_role1, branch, install_pkgs=install_pkgs)
    execute(deploy_role2, branch, install_pkgs=install_pkgs)
