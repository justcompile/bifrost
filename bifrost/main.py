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
import aaargh
import argparse
from generator import Generator

app = aaargh.App(description="Bifrost is a simple, Pythonic tool for deployment and verifying Docker images.")

@app.cmd(alias=['gen'])
@app.cmd_arg('-n', '--name', default='fabfile.py', help='Name of the file to generate')
def generate_fab_file(name):
    print(name)
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


@app.cmd(name="hi", help="Say hi")  # override subcommand name
@app.cmd_arg('-r', '--repeat', type=int, default=1, help="How many times?")
def say_hi(name, repeat):  # both application and subcommand args
    for i in range(repeat):
        print("Hi, %s!" % name)


@app.cmd
@app.cmd_defaults(name="my friend")  # overrides "visitor" for this command only
def greetings(name):
    print("Greetings, %s." % name)


def main():
    """
    Main command-line execution loop.
    """
    app.run()

if __name__ == '__main__':
    main()
