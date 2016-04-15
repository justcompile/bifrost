#!/usr/bin/env python
#pylint: disable-all

from __future__ import with_statement

from setuptools import setup, find_packages

from bifrost.version import get_version


with open('README.md') as f:
    readme = f.read()

long_description = """
To find out what's new in this version of Bifrost, please see `the changelog`_.
----
%s
----
For more information, please see the Bifrost website or execute ``fab --help``.
""" % readme


with open('requirements.txt') as f:
    install_requires = []
    for line in f.read().splitlines():
        install_requires.append(line)


setup(
    name='Bifrost',
    version=get_version('short'),
    description='Bifrost is a simple, Pythonic tool for deployment and verifying Docker images.',
    long_description=long_description,
    author='Richard Hayes',
    author_email='rich@justcompile.it',
    url='http://justcompile.it',
    packages=find_packages(),
    package_data={'bifrost': ['_templates/*.tpl']},
    test_suite='nose.collector',
    tests_require=['nose', 'fudge<1.0', 'jinja2'],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'bifrost = bifrost.main:main',
        ]
    },
    classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Clustering',
          'Topic :: System :: Software Distribution',
          'Topic :: System :: Systems Administration',
    ],
)
