from boto import ec2


class AWSService:
    def __init__(self, profile_name=None, regions=None):
        """ This class helps find instances with a particular set of tags.

            If access key/secret are not given, they must be available as environment
            variables so boto can access them.
        """
        # todo get full region list
        self.regions = regions if regions else ['us-east-1']
        # Open connections to ec2 regions
        self.conn = {}
        for region in self.regions:
            self.conn[region] = ec2.connect_to_region(region,
                                                      profile_name=profile_name)

    def get_instances(self, instance_attr='public_dns_name', only_running=True, **kwargs):
        """ Return instances that match the given tags.

            Keyword arguments:
            instance_attr -- attribute of instance(s) to return (default public_dns_name)

            Additional arguments are used to generate tag filter e.g. "get_instances(role='test')
        """
        if not instance_attr:
            raise ValueError('instance_attr cannot be None or empty' % instance_attr)

        tag_filter = kwargs.pop('filter', {})

        hosts = []
        for region in self.regions:
            reservations = self.conn[region].get_all_instances(None, tag_filter)
            for res in reservations:
                for instance in res.instances:

                    if only_running and instance.state != 'running':
                        continue
                    instance_value = getattr(instance, instance_attr)
                    if instance_value:
                        # Terminated/stopped instances will not have a public_dns_name
                        hosts.append(instance_value)
                    else:
                        raise ValueError('%s is not an attribute of instance' % instance_attr)
        return hosts
