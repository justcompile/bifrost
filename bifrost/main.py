"""
This module contains Bifrost's `main` method plus related subroutines.
`main` is executed as the command line ``bifrost`` program and takes care of
parsing options and commands, loading the user settings file, loading a
bifile, and executing the commands given.
"""
from __future__ import (
    print_function,
    unicode_literals
)
import os
import sys
import aaargh
import argparse
from bifrost.aws import AWSProfile
from bifrost.generators import Config, Fabric
from bifrost.generators.config import ConfigBuilder
from bifrost.version import __version__

FABRIC_FILE_NAME = 'fabfile.py'

app = aaargh.App(description="Bifrost is a simple, Pythonic tool for deployment and verifying Docker images.")
app.arg('-v', '--version', action='version',
        version='%(prog)s {version}'.format(version=__version__))


@app.cmd
@app.cmd_arg('-n', '--name', default='bifrost.cfg', help='Name of the config file to generate')
def init(name):
    if os.path.exists(name):
        print('File already exists, exiting...')
        sys.exit(1)

    profile_name = raw_input('AWS Profile to use: ')
    profile_exists = AWSProfile.exists(profile_name)

    if not profile_exists:
        should_create_profile = raw_input('Do you want to create this profile? [y/n]: ')
        if not should_create_profile.lower() in ['y', 'yes']:
            sys.exit(1)

        access_key_id = raw_input('AWS Access Key Id: ')
        access_secret_key = raw_input('AWS Secret Access Key: ')

        AWSProfile.save(profile_name, access_key_id, access_secret_key)

    config_values = {}
    config_template = Config.load_from_template()

    for key, components in config_template.iteritems():
        if key == 'roles':
            print('Roles...')
            config_values['roles'] = {}
            number_of_roles = raw_input('Number required: ')
            for i in range(0, int(number_of_roles)):
                builder = ConfigBuilder('role {0}'.format(i), {'name': '', 'tag-key': 'my-role'})

                values = builder.prompt_user()
                role_name = values.pop('name')
                config_values['roles'][role_name] = values
        else:
            builder = ConfigBuilder(key, components)
            if key == 'connection':
                builder.change_question('aws_profile', skip=True)
                builder.change_question('regions', required=False)
            elif key == 'deployment':
                builder.change_question('code_dir',required=False)
                builder.change_question('venv',required=False)

            config_values[key] = builder.prompt_user()
            if key == 'repository':
                config_values[key] = config_values[key][key]

    if (config_values):
        Config.save(name=name, **config_values)
        if not os.path.exists(FABRIC_FILE_NAME):
            Fabric.save(FABRIC_FILE_NAME,
                        roles=list(config_values['roles'].iterkeys()))
    else:
        print('No configuration loaded')


@app.cmd
@app.cmd_arg('-n', '--name', default='fabfile.py', help='Name of the file to pull from')
@app.cmd_arg('args', nargs=argparse.REMAINDER)
def deploy(name, args):
    print("Generating fab deploy command...")
    cmd = ['fab']
    if name is not 'fabfile.py':
        cmd.extend(['-f', name])

    cmd.append('setup')
    cmd.extend(args)

    print(' '.join(cmd))


def main():
    """
    Main command-line execution loop.
    """
    app.run()

if __name__ == '__main__':
    main()
