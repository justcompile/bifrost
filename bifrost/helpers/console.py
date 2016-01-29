from __future__ import (
    print_function,
    unicode_literals
)
import sys

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
        print('Please answer the following questions relating to {0}...'.format(self.key))
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
                print('Sorry, {0} is a required value'.format(question['key']))
                answer = raw_input(question_string).strip()

        if answer and question['is_array']:
            answer = answer.split(',')

        if answer and question['is_bool']:
            if not isinstance(answer, bool):
                answer = answer.lower() in ['y', 'yes']

        return answer or question['default']

def query_options(question, *options):
    """Ask a question via raw_input() which requies the user to answer one of a choice of answers and return their answer.
    "question" is a string that is presented to the user.
    "options" is the choices the user must pick one of.
    """

    def parse_options(*args):
        return [unicode(arg).lower() for arg in args]

    options = parse_options(*options)

    prompt = " ({0})".format('|'.join(options))

    while True:
        sys.stdout.write('{0}{1}: '.format(question, prompt))
        choice = raw_input().lower()
        if choice not in options:
            sys.stdout.write("Please respond with one of the following: {0}".format('|'.join(options)))
        else:
            return choice


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
