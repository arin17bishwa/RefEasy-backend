from rest_framework import serializers


def isHR(email, *args, **kwargs):
    return email.endswith('nitdgp.ac.in')


def get_group_name(email: str, *args, **kwargs) -> str:
    if (not email.endswith('nitdgp.ac.in')) and (not email.endswith('gmail.com')):
        return 'APP'
    return 'HR' if isHR(email) else 'NHR'


class LowerEmailField(serializers.EmailField):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        if isinstance(data, bool) or not isinstance(data, (str, int, float,)):
            self.fail('invalid')
        value = str(data).lower()
        return value.strip() if self.trim_whitespace else value
