"""
Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import os
import sys
from datetime import UTC, datetime
from importlib import metadata

# Agregar al PATH el código fuente del módulo libredte
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'LibreDTE: Cliente de API en Python'
project_copyright = f'2024-{datetime.now(tz=UTC).year}, LibreDTE'
author = 'LibreDTE'
# Versión del paquete instalado (definida solo en pyproject.toml): la
# completa (ej. 5.0.0) y la corta (ej. 5.0)
release = metadata.version('libredte')
version = '.'.join(release.split('.')[:2])

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
