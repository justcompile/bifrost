import os
import boto3
from botocore.exceptions import ProfileNotFound


class AWSProfile(object):
    @staticmethod
    def exists(profile_name):
        try:
            boto3.Session(profile_name=profile_name)
        except ProfileNotFound:
            return False

        return True

    @staticmethod
    def save(profile_name, access_key_id, access_secret_key):
        file_name = AWSProfile._get_file_path()
        lines = [
            '[{}]\n'.format(profile_name),
            'aws_access_key_id = {}\n'.format(access_key_id),
            'aws_secret_access_key = {}\n'.format(access_secret_key),
            '\n'
        ]

        if os.path.exists(file_name):
            with(open(file_name)) as fp:
                lines.extend(fp.readlines())

        with(open(file_name, 'w')) as fp:
            fp.writelines(lines)


    @staticmethod
    def _get_file_path():
        return os.path.expanduser('~/.aws/credentials')

class EC2Service(object):
    def __init__(self, profile_name=None, regions=None):
        """ This class helps find instances with a particular set of tags.

            If access key/secret are not given, they must be available as environment
            variables so boto can access them.
        """
        # todo get full region list
        self.regions = regions if regions else ['us-east-1']
        # Open connections to ec2 regions
        self.conn = {}
        session = boto3.Session(profile_name=profile_name)
        for region in self.regions:
            self.conn[region] = session.resource('ec2', region_name=region)

    def get_instances(self, instance_attr='public_dns_name', only_running=True, **kwargs):
        """ Return instances that match the given tags.

            Keyword arguments:
            instance_attr -- attribute of instance(s) to return (default public_dns_name)

            Additional arguments are used to generate tag filter e.g. "get_instances(role='test')
        """
        if not instance_attr:
            raise ValueError('instance_attr cannot be None or empty' % instance_attr)

        tag_filter = kwargs.pop('filter', {})
        filters = []
        if only_running:
            filters.append({'Name': 'instance-state-name', 'Values': ['running']})

        for key, value in tag_filter.iteritems():
            filters.append({'Name': key, 'Values': [value]})

        hosts = []
        for region in self.regions:
            instances = self.conn[region].instances.filter(Filters=filters)

            for instance in instances:
                instance_value = getattr(instance, instance_attr)
                if instance_value:
                    # Terminated/stopped instances will not have a public_dns_name
                    hosts.append(instance_value)
                else:
                    raise ValueError('%s is not an attribute of instance' % instance_attr)
        return hosts
