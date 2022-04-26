import sys


if sys.version_info < (3, 8):
    # compatibility for python <3.8
    import importlib_metadata as metadata
else:
    from importlib import metadata  # noqa: F401, TC002


__version__ = metadata.version('uni')