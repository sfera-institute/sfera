import pathlib
import sys

import pytest


root = pathlib.Path(__file__).absolute().parent.parent
autoimport_path = root / root.name / 'autoimport.py'


@pytest.fixture
def p(tmp_path):
    p = tmp_path / 'p'
    p.mkdir()
    autoimport = p / 'autoimport.py'
    autoimport.write_text(autoimport_path.read_text())
    init = p / '__init__.py'
    init.write_text('''
from .autoimport import autoimport as __getattr__
''')
    v = p / 'v.py'
    v.write_text('''
x = 1
_y = 2
''')
    f = p / 'f.py'
    f.write_text('''
def f():
    return 1
def _g():
    return 2
''')
    c = p / 'c.py'
    c.write_text('''
class A:
    x = 1
class _B:
    y = 2
''')
    root = str(tmp_path)
    sys.path.append(root)
    try:
        yield __import__(p.name)
    finally:
        for name in list(sys.modules):
            if name == p.name or name.startswith(f'{p.name}.'):
                del sys.modules[name]
        if root in sys.path:
            sys.path.remove(root)


def test_all(p):
    assert p.__all__ == ['autoimport', 'A', 'f', 'x']


def test_variable(p):
    assert p.x == 1
    with pytest.raises(ImportError, match=r"cannot import '_y' \(expected one of: autoimport, A, f, x\)"):
        p._y


def test_function(p):
    assert p.f() == 1
    with pytest.raises(ImportError, match=r"cannot import '_g' \(expected one of: autoimport, A, f, x\)"):
        p._g()


def test_class(p):
    a = p.A()
    assert a.x == 1
    with pytest.raises(ImportError, match=r"cannot import '_B' \(expected one of: autoimport, A, f, x\)"):
        p._B()


def test_valid_circular_import(p):
    a = pathlib.Path(p.__file__).parent / 'loop' / 'a.py'
    a.parent.mkdir()
    a.write_text('''
import p
a = 1
c = p.b + 1
''')
    b = a.parent / 'b.py'
    b.write_text('''
import p
b = p.a + 1
''')
    assert p.a == 1
    assert p.b == 2
    assert p.c == 3


def test_circular_import(p):
    a = pathlib.Path(p.__file__).parent / 'loop' / 'a.py'
    a.parent.mkdir()
    a.write_text('''
import p
a = p.b + 1
''')
    b = a.parent / 'b.py'
    b.write_text('''
import p
b = p.a + 1
''')
    with pytest.raises(ImportError):
        p.a
    with pytest.raises(ImportError):
        p.b


def test_cache(p):
    assert p.A.x == 1
    p.A.x = 2
    assert p.A.x == 2


def test_missing_name(p):
    with pytest.raises(ImportError, match=r"cannot import 'foo' \(expected one of: autoimport, A, f, x\)"):
        p.foo