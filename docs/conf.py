"""Sphinx configuration."""
import sys
import os

sys.path.insert(0, os.path.abspath('../src'))

project = "qlicS"
author = "Michael Mitchell"
copyright = f"2024, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]
