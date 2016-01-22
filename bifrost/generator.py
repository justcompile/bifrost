"""
This module contains Bifrost's generation class which is used to create the
fabric files used to create
"""
from __future__ import (
    print_function,
    unicode_literals
)
import os

__all__ = ['Generator']

TEMPLATES = {
    'fabric': open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '_templates/fabfile.py'), 'r').read()
}

class Generator(object):
    @staticmethod
    def fabric(file_name):
        with open(file_name, 'w') as fp:
            fp.write(TEMPLATES['fabric'])
