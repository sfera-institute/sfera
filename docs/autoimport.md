# Auto-Import

A mechanism that automatically collects and exposes SFERA's public API
(instead of coding it manually in various `__init__.py` files).

The way it works is traversing all the Python files in the `sfera` package,
extracting any public variabes, functions or classes
(that is, any name that doesn't start with `_`),
and importing them on demand, when `sfera.<name>` is accessed.

Of course, in case of name clashes (i.e. similar names in different modules),
you get an exception; but otherwise, the imported values are cached,
circular imports are resolved gradually (to the extent it's even possible),
and everything is nice and simple.

To see it in action, you can enable its log:

```python
>>> sfera.autoimport.log.enabled = True
```

At which point, any import (that is, accessing `sfera.<name>`)
will print what's going on behind the scenes.