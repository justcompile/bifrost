from __future__ import (
    unicode_literals
)
import os


class Fabric(object):
    @staticmethod
    def load_from_template():
        tmpl_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                '../_templates/fabfile.tpl')

        with(open(tmpl_path)) as fp:
            return fp.read()

    @staticmethod
    def save(name='fabfile.py'):
        tmpl_data = Fabric.load_from_template()

        with(open(name, 'w')) as fp:
            fp.write(tmpl_data)
