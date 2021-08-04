import contextlib


@contextlib.contextmanager
def replace_error(source, target):
    try:
        yield
    except source as error:
        raise target(*error.args)