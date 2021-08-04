import pytest

import sfera


def test_replace():
    with pytest.raises(TypeError, match='foo'):
        with sfera.replace_error(ValueError, TypeError):
            raise ValueError('foo')


def test_no_replace():
    with pytest.raises(RuntimeError, match='foo'):
        with sfera.replace_error(ValueError, TypeError):
            raise RuntimeError('foo')