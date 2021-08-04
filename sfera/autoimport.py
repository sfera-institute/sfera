import pathlib
import re


_root = pathlib.Path(__file__).absolute().parent
_names = {}
_modules = {}
_importing = {}
_name_regex = re.compile(r'''
    ^(?:
        # A variable:
        ([a-zA-Z][a-zA-Z0-9_]*) \s* =
        |
        # A function:
        def \s+ ([a-zA-Z][a-zA-Z0-9_]*) \s* \(
        |
        # Or a class:
        class \s+ ([a-zA-Z][a-zA-Z0-9_]*) \s* [:\(]
    )
''', flags=re.VERBOSE | re.MULTILINE)


def _log(format_string):
    if not _log.enabled:
        return
    import datetime as dt, inspect, string # Avoid polluting the global namespace.
    namespace = inspect.currentframe().f_back.f_locals
    message = string.Formatter().vformat(format_string, (), namespace)
    print(f'[{dt.datetime.now()}] {message}')


_log.enabled = False


def autoimport(name):
    _log('importing {name}')
    if not _names:
        _collect_names()
    if name == '__all__':
        _log('returning all names')
        return list(_names)
    if name not in _names:
        raise ImportError(f'cannot import {name!r} (expected one of: {", ".join(_names)})')
    source, cached = _names[name]
    if source is None:
        _log('returning cached {name}')
        return cached
    _log('found {name} in {source}')
    if source not in _modules:
        if source in _importing:
            _log('already importing module {source}')
            module, _ = _importing[source]
            try:
                return _get_value(module, name)
            except AttributeError:
                circle = ' -> '.join(f'{module.__name__}.{name_}' for module, name_ in [*_importing.values(), (module, name)])
                raise ImportError(f'cannot import {name!r} because of a circular import ({circle})')
        _import_module(source, name)
    module = _modules[source]
    _log('imported module {module}')
    try:
        return _get_value(module, name)
    except AttributeError:
        names = [name_ for name_ in module.__dict__ if not name_.startswith('_')]
        raise ImportError(f'cannot import {name!r} from module {module.__name__!r} (expected one of: {", ".join(names)})')


def _collect_names(root=_root):
    _log('traversing {root}')
    for path in root.iterdir():
        _log('considering {path}')
        if path.name.startswith(('.', '_')):
            continue
        if path.is_file() and path.suffix == '.py':
            _log('reading {path}')
            text = path.read_text()
            for name, function_name, class_name in _name_regex.findall(text):
                name = name or function_name or class_name
                if name in _names:
                    other_value, other_path = _names[name]
                    raise ImportError(f'multiple definitions of {name!r} (in {other_path} and in {path})')
                _log('collecting {name}')
                _names[name] = path, None
        if path.is_dir():
            _collect_names(root=path)


def _import_module(source, name):
    import os, types # Avoid polluting the global namespace.
    _log('reading {source}')
    text = source.read_text()
    module_name, _ = os.path.splitext(source.relative_to(_root))
    module_name = module_name.replace(os.sep, '.')
    module = types.ModuleType(f'{__package__}.{module_name}')
    module.__file__ = str(source)
    module.__package__ = __package__
    module.__path__ = []
    _importing[source] = module, name
    try:
        _log('compiling module {module.__name__}')
        code = compile(text, source.name, 'exec')
        exec(code, module.__dict__)
        _modules[source] = module
        _log('cached module {name}')
        return module
    finally:
        del _importing[source]


def _get_value(module, name):
    value = getattr(module, name)
    _names[name] = None, value
    _log('cached {value} as {name}')
    return value


autoimport.log = _log