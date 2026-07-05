#!/usr/bin/env python3
# this_file: gimeltra/__init__.py
"""Gimeltra: abjad transliteration between mostly-Semitic writing systems."""

from importlib.metadata import PackageNotFoundError, version

from .gimeltra import Transliterator, tr

try:
    __version__ = version("gimeltra")
except PackageNotFoundError:  # running from a source tree without install metadata
    __version__ = "0.0.0+unknown"

__all__ = ["Transliterator", "tr", "__version__"]
