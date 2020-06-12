def find(values, func):
    for x in values:
        if func(x):
            return x
    return None


def toggle_file(dummy_path, on_delete=None, on_create=None):
    from os.path import exists
    from os import remove

    if not exists(dummy_path):
        with open(dummy_path, 'x'):
            pass
        if on_create:
            on_create()
    else:
        remove(dummy_path)
        if on_delete:
            on_delete()


class DeferralFailure(Exception):
    def __init__(self, errors):
        self.errors = errors


class Defer:
    def __init__(self):
        self.deferrals = []

    def __add__(self, other):
        assert other.__call__
        self.deferrals.append(other)

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        errors = []

        self.deferrals.reverse()

        for deferral in self.deferrals:
            try:
                deferral()
            except Exception as e:
                errors.append(e)

        if (len(errors) is not 0):
            raise DeferralFailure(errors)
