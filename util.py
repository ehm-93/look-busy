def find(values, func):
    """Finds a member of an iterable.

    :param values:
        an iterable
    :param func: 
        a callable object which will be passed the members of values
    :return: 
        the first member of values for which func returns true
    """
    for x in values:
        if func(x):
            return x
    return None


def toggle_file(dummy_path, on_delete=None, on_create=None):
    """Deletes the passed file if it exists, otherwise it is created.

    :param dummy_path:
        Path to the file to toggle
    :param on_delete:
        A callable which executes if the file is deleted
    :param on_create:
        A callable which executes if the file is created
    """
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


class Defer:
    """Convenient class to add handlers to a context exiting. 

    I'm not sure if this is a good idea or not.
    """

    def __init__(self):
        self.deferrals = []

    def __add__(self, other):
        """Adds a new deferral to this Defer."""
        assert other.__call__
        self.deferrals.append(other)

    def __enter__(self):
        """Starts this deferral context and return's self"""
        return self

    def __exit__(self, a, b, c):
        """Exits this deferral context and calls all deferrals in the reverse 
        order they were deferred in.

        If any of the deferrals throw an Exception, the other deferrals will continue to be
        called, but after they've all fired, a DeferralFailure exception will be raised.
        """
        errors = []

        self.deferrals.reverse()

        for deferral in self.deferrals:
            try:
                deferral()
            except Exception as e:
                errors.append(e)

        if (len(errors) is not 0):
            raise DeferralFailure(errors)


class DeferralFailure(Exception):
    """An exception to be raised if there are errors in a Defer's __exit__"""

    def __init__(self, errors):
        self.errors = errors
