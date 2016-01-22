from __future__ import (
    print_function,
    unicode_literals
)
from datetime import datetime
import os
from fabric.api import run, sudo
from bifrost.aws_service import AWSService

def get_ssh_gateway(config):
    regions = config['connection'].get('regions')
    aws_profile = config['connection'].get('aws_profile')
    gateways = {}
    for region in regions:
        aws = AWSService(profile_name=aws_profile, regions=[region])
        ips = aws.get_instances(instance_attr='ip_address',
                                filter={'tag:role': 'nat'})

        assert len(ips) is 1, "You seem to have too many NAT boxes"
        gateways[region] = 'ec2-user@{}'.format(ips[0])

    return gateways


def generate_fabric_roles(config):
    """
    Using the configuration provided and the AWS EC2 API this method compiles
    a dict of connection details for a given list of roles for Fabric to utilise
    """
    assert 'roles' in config, "Config must contain a roles key"
    regions = config['connection'].get('regions')
    aws_profile = config['connection'].get('aws_profile')

    aws = AWSService(profile_name=aws_profile, regions=regions)

    roles = {}
    for role_name, filters in config['roles'].iteritems():
        ips = aws.get_instances(instance_attr='private_ip_address',
                                filter=filters)

        roles[role_name] = ['ubuntu@{}'.format(ip) for ip in ips]

    return roles


def list_files(directory):
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
    backup_dir = os.path.join('/var/backups', '{}-{}'.format(key, backup_name))

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
    result = run('hg update {}'.format(branch))

    return result

def convert_to_bool(val, default=False):
    import ast

    if isinstance(val, bool):
        return val

    if val in [0, 1, '0', '1']:
        return int(val) == 1

    try:
        return ast.literal_eval(val.title())
    except:
        return default

def copy_code(deployment_config, source_dir='src', **additional_files):
    """
    Removes the old code base before copying the new one across
    """
    deployment_dir = os.path.join(deployment_config['base_dir'],
                                  deployment_config['code_dir'])

    sudo('rm -rf %s/*' % deployment_dir, user=deployment_config['user'])

    sudo('cp -r {}/* {}'.format(source_dir, deployment_dir),
                                user=deployment_config['user'])

    for source, dest in additional_files.iteritems():
        if dest != '.':
            print('Attempting to copy {} to {}'.format(source, dest))
            raise NotImplementedError('Need to implement moving additional '
                                      'files somewhere other than the '
                                      'deployment directory')

        sudo('cp -r {} {}'.format(source, deployment_dir),
             user=deployment_config['user'])


def install_pkgs(deployment_config):
    pip_binary = os.path.join(deployment_config['base_dir'],
                              deployment_config['venv'], 'bin/pip')

    sudo('{} install -r requirements.txt'.format(pip_binary),
         user=deployment_config['user'])
