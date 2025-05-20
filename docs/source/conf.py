# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'swingmusic'
copyright = '2025, Mungai Njoroge'
author = 'Mungai Njoroge'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "myst_parser",
    "sphinx_design",
    "autodoc2",
]

autodoc2_packages = [
    "../../src/swingmusic",
]

myst_enable_extensions = ["colon_fence"]


language = 'en'
autosummary_generate = True  # Turn on sphinx.ext.autosummary


autodoc_default_options = {
    'member-order': 'bysource'
}

add_module_names = False



# dynamic module import when module is not installed
try:
    import swingmusic
    import swing_pydub
except ImportError:
    # append module to path
    import sys
    import os
    sys.path.insert(0, os.path.abspath('../..'))
    sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'src')))

# anywhere in conf.py before any of your modules are imported
import builtins
builtins.__sphinx_build__ = True



# remove to dont show todos:
todo_include_todos = True
