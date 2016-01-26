from __future__ import (
    unicode_literals
)
from copy import deepcopy
import os
import yaml


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
    def save(name='bifrost.cfg', connection={}, deployment={},
                                    repository=None, roles={}, **kwargs):
        tmpl_data = deepcopy(Config.load_from_template())

        tmpl_data['connection'].update(connection)
        tmpl_data['deployment'].update(deployment)
        if repository:
            tmpl_data['repository'] = repository

        tmpl_data['roles'].update(roles)

        with(open(name, 'w')) as fp:
            fp.write(yaml.dump(tmpl_data))

    @staticmethod
    def _get_file_path():
        return os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            '_templates/config-yaml.tpl')


class ConfigBuilder(object):
    def __init__(self, key, data):
        self.values = {}
        self.key = key

        self._questions = {}
        if isinstance(data, basestring):
            data = {key: data}

        for k, v in data.iteritems():
            self._questions[k] = {
                'key': k,
                'default': v,
                'required': False,
                'is_bool': v in ['True', 'False', True, False],
                'is_array': isinstance(v, list)
            }

    def change_question(self, question, **kwargs):
        q = self._questions[question]
        q.update(kwargs)

    def prompt_user(self):
        print 'Please answer the following questions relating to {0}...'.format(self.key)
        for key, question in self._questions.iteritems():
            if question.get('skip'):
                self.values[key] = question['default']
            else:
                self.values[key] = self._get_answer_for_question(question)

        return self.values

    def _get_answer_for_question(self, question, indent=2):
        if question['is_bool']:
            suffix = ' [y/n]'
        elif question['is_array']:
            suffix = ' (comma seperated)'
        else:
            suffix = ''

        question_string = '{indent}{component}{suffix} [default: {default}]: '.format(
            indent=' '*indent,
            component=question['key'],
            suffix=suffix,
            default=question['default']
         )
        answer = raw_input(question_string).strip()

        if question['required'] and not answer:
            while not answer:
                print 'Sorry, {0} is a required value'.format(question['key'])
                answer = raw_input(question_string).strip()

        if answer and question['is_array']:
            answer = answer.split(',')

        if answer and question['is_bool']:
            if not isinstance(answer, bool):
                answer = answer.lower() in ['y', 'yes']            

        return answer or question['default']
