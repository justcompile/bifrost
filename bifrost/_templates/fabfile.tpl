from fabric.api import roles, execute, abort, env, sudo
from fabric.context_managers import cd
from fabric.contrib.console import confirm
from fabric.decorators import runs_once
from fabric.operations import local, run
from bifrost.deploy import helpers


def setup():
    env.config = helpers.load_config()

    if env.config['connection'].get('gateway'):
        env.gateway = helpers.get_ssh_gateway(env.config)['eu-west-1']

    env.roledefs = helpers.generate_fabric_roles(env.config)
    env.key_filename = env.config['connection']['ssh_key']


{% for role in roles %}
@roles('{{role}}')
def deploy_{{role}}(branch, install_pkgs=False):
    pass
{% endfor %}

def deploy(branch, install_pkgs=False):
    {% for role in roles %}
    execute(deploy_{{role}}, branch, install_pkgs=install_pkgs)
    {% endfor %}
