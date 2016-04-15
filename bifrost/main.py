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
import subprocess

from bifrost.aws import AWSProfile
from bifrost.generators import Config, Fabric
from bifrost.helpers import fab
from bifrost.helpers.console import print_header, ConfigBuilder, query_yes_no, query_options
from bifrost.version import __version__

FABRIC_FILE_NAME = 'fabfile.py'

app = aaargh.App(description="Bifrost is a simple, Pythonic tool for deployment and verifying Docker images.")
app.arg('-v', '--version', action='version',
        version='%(prog)s {version}'.format(version=__version__))


@app.cmd
@app.cmd_arg('-n', '--name', default='bifrost.cfg', help='Name of the config file to generate')
def init(name):
    print_header()
    if os.path.exists(name):
        print('File already exists, exiting...')
        sys.exit(1)

    app_type = query_options('Type of application', 'python', 'javascript')
    dvsc = query_options('Source Control version', 'git', 'hg')

    profile_name = raw_input('AWS Profile to use: ')
    profile_exists = AWSProfile.exists(profile_name)

    if not profile_exists:
        should_create_profile = query_yes_no('Do you want to create this profile?: ')
        if not should_create_profile:
            sys.exit(1)

        access_key_id = raw_input('AWS Access Key Id: ')
        access_secret_key = raw_input('AWS Secret Access Key: ')

        AWSProfile.save(profile_name, access_key_id, access_secret_key)

    config_values = {}
    config_template = Config.load_from_template()

    for key, components in config_template.iteritems():
        if key in ['bifrost', 'application', 'dvsc']:
            continue
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
            elif key == 'deployment':
                builder.change_question('base_dir', required=True)
            elif key == 'repository':
                builder.change_question('repository', required=True)

            config_values[key] = builder.prompt_user()
            if key == 'repository':
                config_values[key] = config_values[key][key]

    if config_values:
        Config.save(name=name, application_type=app_type, dvsc=dvsc, **config_values)
        if not os.path.exists(FABRIC_FILE_NAME):
            Fabric.save(FABRIC_FILE_NAME,
                        roles=list(config_values['roles'].iterkeys()))
    else:
        print('No configuration loaded')


@app.cmd
@app.cmd_arg('-n', '--name', default='bifrost.cfg', help='Name of the config file load')
@app.cmd_arg('-t', '--tasks', action='store_true', help='List the available tasks')
@app.cmd_arg('args', nargs=argparse.REMAINDER)
def deploy(name, tasks, args):
    print_header()
    if tasks:
        fab.display_fabric_tasks()
        sys.exit(0)
    else:
        print("Generating fab deploy command...")
        cmd = ['fab']
        cmd.append('setup:config={0}'.format(name))

        if args:
            cmd.extend(args)
        else:
            cmd.append('deploy:branch=default')

        print('Executing: {0}'.format(' '.join(cmd)))
        if query_yes_no("Do you want to continue?", default="no"):
            subprocess.call(cmd)


def main():
    """
    Main command-line execution loop.
    """
    app.run()

if __name__ == '__main__':
    main()
