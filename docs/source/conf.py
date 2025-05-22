# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from sphinx.ext import todo

sys.path.insert(0, os.path.abspath("../../src"))


# -- Project information -----------------------------------------------------

project = "Embedded Systems Lab"
copyright = "2025, Universität Siegen"
author = "Utkarsh Raj"

# The full version, including alpha/beta/rc tags
release = "1.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "myst_parser",
    "sphinx.ext.todo",
]

todo_include_todos = True

# conf.py
myst_url_schemes = [
    "http",
    "https",
]  # Ensures that standard web protocols are recognized

myst_enable_extensions = [
    "dollarmath",  # Enables dollar symbol for inline math
    "amsmath",  # Allows more complex math formatting
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_favicon = "_static/unisiegen.png"


# Function to convert absolute paths to relative paths
def convert_todo_path(app, doctree, fromdocname):
    # Iterate over all nodes in the document tree
    for node in doctree.traverse(todo.todo_node):
        source_file = node.source
        if source_file:
            # Convert the absolute path to a relative path
            rel_path = os.path.relpath(source_file, start=app.srcdir)
            # Update the node's source attribute to the relative path
            node.source = rel_path


# Add the above function to the Sphinx setup
def setup(app):
    app.connect("doctree-resolved", convert_todo_path)
