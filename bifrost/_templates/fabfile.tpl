from fabric.api import roles, execute, abort, env, sudo
from fabric.context_managers import cd, settings
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from fabric.decorators import runs_once
from fabric.operations import local, run
from bifrost.helpers import deploy as deploy_helpers


def setup(config=None):
    env.config = deploy_helpers.load_config(config)

    if env.config['connection'].get('gateway'):
        env.gateway = deploy_helpers.get_ssh_gateway(env.config)

    env.roledefs = deploy_helpers.generate_fabric_roles(env.config)
    env.key_filename = env.config['connection']['ssh_key']


{% for role in roles %}
@roles('{{role}}')
def deploy_{{role}}(branch, install_pkgs=False):
    """ Deploys from `branch` to {{role}}
    """
    # Stop services here...
    sudo('service myservice stop')

    with cd(env.config['repository']):
        res = deploy_helpers.checkout_code(branch=branch, dvsc_type=env.config['dvsc']))
        if not res:
            abort('Unable to download code')

    deploy_helpers.backup('{{role}}', env.config['deployment'])

    with cd(env.config['repository']):
        additional_files = {
            'requirements.txt': '.'
        }

        deploy_helpers.copy_code(env.config['deployment'],
                          source_dir='src',
                          **additional_files)

    if deploy_helpers.convert_to_bool(install_pkgs):
        with cd(env.config['repository']):
            deploy_helpers.install_pkgs(env.config)

    sudo('service myservice start')
{% endfor %}

def deploy(branch, install_pkgs=False):
    """ Deploys from `branch` to all roles
    """
    {% for role in roles %}
    execute(deploy_{{role}}, branch, install_pkgs=install_pkgs)
    {% endfor %}
