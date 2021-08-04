# Auto-Import

A mechanism that automatically collects and exposes SFERA's public API
(instead of coding it manually in various `__init__.py` files).

The way it works is by traversing all the Python files in the `sfera` package,
extracting any variable, function or class names that don't start with `_`,
and importing them on demand, when `sfera.<name>` is accessed.

Of course, in case of names clashing (i.e. similar names in different modules),
you get an exception; but that shouldn't really happen.
Otherwise, the imported values are cached, circular imports are resolved gradually
(to the extent it's even possible), and everything is nice and simple.

To see it in action, you can enable its log:

```python
>>> sfera.autoimport.log.enabled = True
```

At which point, any import (that is, accessing `sfera.<name>`)
will print what's going on behind the scenes.

To use it in your own project, copy the `autoimport.py` file there,
and add the following line in your `__init__.py`:

```python
from .autoimport import autoimport as __getattr__
```

Et voila: all your public names should be automatically available through your package.