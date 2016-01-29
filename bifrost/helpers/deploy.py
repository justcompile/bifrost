"""
Contains a number of methods to used during the deployment process
"""
from __future__ import (
    print_function,
    unicode_literals
)
from datetime import datetime
import os
from fabric.api import run, sudo
from fabric.context_managers import cd
from bifrost.aws import EC2Service
from bifrost.generators import Config


def load_config(file_name=None):
    """
    Loads Bifrost configuration file for project
    """
    return Config.load(file_name)

def get_ssh_gateway(config):
    """
    Returns the SSH gateway for a project based on the AWS Region
    """
    region = config['connection'].get('region')
    aws_profile = config['connection'].get('aws_profile')

    aws = EC2Service(profile_name=aws_profile, region=region)
    ips = aws.get_instances(instance_attr='public_ip_address',
                            filter={'tag:role': 'nat'})

    assert len(ips) is 1, "You seem to have too many NAT boxes"
    return 'ec2-user@{0}'.format(ips[0])


def generate_fabric_roles(config):
    """
    Using the configuration provided and the AWS EC2 API this method compiles
    a dict of connection details for a given list of roles for Fabric to utilise
    """
    assert 'roles' in config, "Config must contain a roles key"
    region = config['connection'].get('region')
    aws_profile = config['connection'].get('aws_profile')

    aws = EC2Service(profile_name=aws_profile, region=region)

    roles = {}
    for role_name, filters in config['roles'].iteritems():
        ips = aws.get_instances(instance_attr='private_ip_address',
                                filter=filters)

        roles[role_name] = ['ubuntu@{0}'.format(ip) for ip in ips]

    return roles


def list_files(directory):
    """
    Generates a list of filenames for a given directory
    """
    string_ = run("for i in %s/*; do echo $i; done" % directory)
    files = string_.replace("\r", "").split("\n")
    if len(files) == 1 and files[0].endswith('/*'):
        return []
    return files


def backup(key, deployment_config):
    """
    Runs backup of existing code base
    """
    backup_name = deployment_config['base_dir'].replace('/', '_')
    backup_dir = os.path.join('/var/backups', '{0}-{1}'.format(key, backup_name))

    deployment_dir = os.path.join(deployment_config['base_dir'],
                                  deployment_config['code_dir'])

    # Ensure this dir actually exists
    sudo('mkdir -p %s' % backup_dir)

    all_backup_files = list_files(backup_dir + '/')
    for backup_file in all_backup_files[:5]:
        sudo('rm ' + backup_file)

    backup_tar_name = '%s.tar.gz' % datetime.now().strftime('%Y%m%d%H%M%S')

    sudo('tar -czf %s %s' % (os.path.join(backup_dir, backup_tar_name),
                             deployment_dir))


def checkout_code(branch):
    """
    Checks out code base from BitBucket
    """

    run('hg pull -u')
    result = run('hg update {0}'.format(branch))

    return result

def convert_to_bool(val, default=False):
    """
    Converts a value to it's boolean representation, used for parsing
    command line arguements
    """
    import ast

    if isinstance(val, bool):
        return val

    if val in [0, 1, '0', '1']:
        return int(val) == 1

    try:
        return ast.literal_eval(val.title())
    except ValueError:
        return default

def copy_code(deployment_config, source_dir='src', delete_dest_contents=True,
              **additional_files):
    """
    Removes the old code base before copying the new one across
    """
    deployment_dir = os.path.join(deployment_config['base_dir'],
                                  deployment_config['code_dir'].strip())

    if delete_dest_contents:
        sudo('rm -rf %s/*' % deployment_dir, user=deployment_config['user'])
    sudo('cp -r {0}/* {1}'.format(source_dir, deployment_dir),
         user=deployment_config['user'])

    for source, dest in additional_files.iteritems():
        if dest != '.':
            print('Attempting to copy {0} to {1}'.format(source, dest))
            raise NotImplementedError('Need to implement moving additional '
                                      'files somewhere other than the '
                                      'deployment directory')

        sudo('cp -r {0} {1}'.format(source, deployment_dir))

    sudo('chown {0} -R {1}'.format(deployment_config['user'],
                                   deployment_dir))


def install_pkgs(config, **kwargs):
    """
    Installs the Project's packages
    """
    deployment_config = config['deployment']
    app_type = config['application']['type']
    if app_type == 'python':
        _install_python_packages(deployment_config, **kwargs)
    elif app_type == 'javascript':
        _install_node_packages(deployment_config, **kwargs)
    else:
        raise Exception('{0} is not a supported application type'.format(app_type))


def _install_python_packages(deployment_config,
                             requirements_file='requirements.txt',
                             **kwargs):
    """
    Will install python requirements using `pip`.
    """
    pip_binary = os.path.join(deployment_config['base_dir'],
                              deployment_config['venv'], 'bin/pip')

    sudo('{0} install -r {1}'.format(pip_binary, requirements_file),
         user=deployment_config['user'])


def _install_node_packages(deployment_config, **kwargs):
    """
    Installs Node.js packages via `npm`
    """
    code_dir = os.path.join(deployment_config['base_dir'],
                            deployment_config['code_dir'].strip())

    command = 'npm install'
    if 'home_env' in kwargs:
        command = 'HOME={0} {1}'.format(kwargs['home_env'], command)

    with cd(code_dir):
        sudo(command, user=deployment_config['user'])
