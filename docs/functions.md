# Functions

A collection of useful functions.

## Replace-Error

A context manager that replaces one raised exception with another:

```python
>>> with sfera.replace_error(ValueError, TypeError):
...     raise ValueError('foo')
Traceback (most recent call last):
  ...
TypeError: foo
```