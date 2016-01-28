from __future__ import (
    unicode_literals
)
from copy import deepcopy
import os
import yaml
from bifrost.version import get_version


class Config(object):
    @staticmethod
    def load(name='bifrost.cfg'):
        with(open(name)) as fp:
            return yaml.load(fp.read())

    @staticmethod
    def load_from_template():
        tmpl_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                '../_templates/config-yaml.tpl')

        with(open(tmpl_path)) as fp:
            return yaml.load(fp.read())

    @staticmethod
    def save(name='bifrost.cfg', application_type='undefined', connection={},
             deployment={}, repository=None, roles={}, **kwargs):
        tmpl_data = deepcopy(Config.load_from_template())

        bifrost_info = tmpl_data.get('bifrost', {})
        bifrost_info['version'] = get_version('short')

        tmpl_data['bifrost'] = bifrost_info

        tmpl_data['connection'].update(connection)
        tmpl_data['deployment'].update(deployment)
        if repository:
            tmpl_data['repository'] = repository

        tmpl_data['roles'] = roles
        tmpl_data['application']['type'] = application_type

        with(open(name, 'w')) as fp:
            fp.write(yaml.dump(tmpl_data))

    @staticmethod
    def _get_file_path():
        return os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            '_templates/config-yaml.tpl')
