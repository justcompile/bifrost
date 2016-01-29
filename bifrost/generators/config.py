from __future__ import (
    unicode_literals
)
from copy import deepcopy
import os
import yaml
from bifrost.version import get_version


class Config(object):
    """
    Config class contains a number of methods for interacting with the Bifrost
    configuration data
    """
    @staticmethod
    def load(name='bifrost.cfg'):
        """
        Loads in the configuration file for the current project. Can override
        the name of which file to load via the `name` parameter
        """
        with(open(name)) as file_pointer:
            return yaml.load(file_pointer.read())

    @staticmethod
    def load_from_template():
        """
        Loads the Bifrost configuration template
        """
        tmpl_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../_templates/config-yaml.tpl')

        with(open(tmpl_path)) as file_pointer:
            return yaml.load(file_pointer.read())

    @staticmethod
    def save(name='bifrost.cfg', application_type='undefined', connection=None,
             deployment=None, repository=None, roles=None):
        """
        Saves a given configuration data to a file in the current directory.
        """
        tmpl_data = deepcopy(Config.load_from_template())

        bifrost_info = tmpl_data.get('bifrost', {})
        bifrost_info['version'] = get_version('short')

        tmpl_data['bifrost'] = bifrost_info

        tmpl_data['connection'].update(connection or {})
        tmpl_data['deployment'].update(deployment or {})
        if repository:
            tmpl_data['repository'] = repository

        tmpl_data['roles'] = roles or {}
        tmpl_data['application']['type'] = application_type

        with(open(name, 'w')) as file_pointer:
            file_pointer.write(yaml.dump(tmpl_data))

    @staticmethod
    def _get_file_path():
        """
        Retrieves the path of the configuration template
        """
        return os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            '_templates/config-yaml.tpl')
