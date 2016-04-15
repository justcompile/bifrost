from fabric.api import run


class Mercurial(object):
    @staticmethod
    def update_to_branch(branch_name):
        run('hg pull -u')
        return run('hg update {0}'.format(branch_name))


class Git(object):
    @staticmethod
    def update_to_branch(branch_name):
        run('git pull')
        return run('git checkout {0}'.format(branch_name))


def cls_for_dvsc(dvsc_type):
    if dvsc_type.lower() == 'git':
        return Git
    elif dvsc_type.lower() == 'hg':
        return Mercurial
    else:
        raise NotImplemented('DVSC type: {0} is not recognised'.format(dvsc_type))
