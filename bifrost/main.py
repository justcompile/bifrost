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
from bifrost.aws import ConfigService
from bifrost.generator import Generator
from bifrost.version import __version__

app = aaargh.App(description="Bifrost is a simple, Pythonic tool for deployment and verifying Docker images.")
app.arg('-v', '--version', action='version',
        version='%(prog)s {version}'.format(version=__version__))


@app.cmd
@app.cmd_arg('-n', '--name', default='fabfile.py', help='Name of the file to generate')
def init(name):
    if os.path.exists(name):
        print('File already exists, exiting...')
        sys.exit(1)

    profile_name = raw_input('AWS Profile to use')
    profile_exists = ConfigService.profile_exists(profile_name)

    should_create_profile = raw_input('Do you want to create this profile? [y/n]')
    if not should_create_profile.lower() in ['y', 'yes']:
        sys.exit(1)

    access_key_id = raw_input('AWS Access Key Id:')
    access_secret_key = raw_input('AWS Secret Access Key:')

    ConfigService.save_profile(profile_name, access_key_id, access_secret_key)


@app.cmd(alias=['gen'])
@app.cmd_arg('-n', '--name', default='fabfile.py', help='Name of the file to generate')
def generate_fab_file(name):
    Generator.fabric(name)


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
