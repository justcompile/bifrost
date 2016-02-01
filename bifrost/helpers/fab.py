from __future__ import (unicode_literals, print_function)

from fabric import state
from fabric.main import find_fabfile, load_fabfile, list_commands


def display_fabric_tasks():
    paths = find_fabfile()
    docstring, callables, default = load_fabfile(paths)
    callables.pop('setup', None)
    state.commands.update(callables)

    commands = list_commands(docstring, 'normal')
    print("\n".join(commands))
