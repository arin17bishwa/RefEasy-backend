def isHR(email, *args, **kwargs):
    return True


def get_group_name(email: str, *args, **kwargs) -> str:
    if not email.endswith('@nitdgp.ac.in'):
        return 'APP'
    return 'HR' if isHR(email) else 'NHR'
