# Sphinx Guide
Sphinx is a tool to automate documentation for Python software.

## Let's Use Sphinx
There isn't much- you just pip install Sphinx, put together a couple of configuration files, and let it rip.

- Install Sphinx: `pip install sphinx`
- Create a "docs" folder to contain all Sphinx configuration and build files
- Create configuration files:
  - **conf.py**
    - Configures HTML files generated
    - Make sure that the path in `os.path.abspath()` leads to your source files
    - Example of conf.py file:
```python
# docs/conf.py

import os
import sys

# Include the root directory in the Python path
sys.path.insert(0, os.path.abspath('../../../source'))  # Include the root directory in the Python path

# Project Information
project = 'Project Name Here'
author = 'Team Name Here'
version = '1.0'
release = '1.0.0'

# General Configuration
extensions = [
    'sphinx.ext.autodoc',   # Auto-generate documentation from docstrings
    'sphinx.ext.napoleon',  # Support for Google-style and NumPy-style docstrings
    'sphinx.ext.viewcode',  # Include links to the source code
]
templates_path = ['_templates']  # Path to custom templates
exclude_patterns = []            # Exclude certain files/folders from documentation

# HTML Output Configuration
html_theme = 'bizstyle'  # You can choose other themes like 'sphinx_rtd_theme'
#html_static_path = ['_static']  # Path to custom static files (CSS, JavaScript)
```

  - **index.rst**
    - Configures Index page that's generated
    - Example of index.rst file:
```
.. My Project documentation master file

Project Name Here
======================================

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   module_name_here
```
  - **xxx.rst** 
    - You need to create a ReStructured Text (rst) markup file for every Python file (aka module)
    - This can be automated by using Sphinx: `sphinx-apidoc -o <output_directory> <input_directory>` 
    - Example of Python module rst file:
```
module_name_here
===================

.. automodule:: module_name_here
   :members:
   :undoc-members:
   :show-inheritance:
```

- w/ cmd in the docs directory run `sphinx-build -b html docs/ docs/_build`
- go into the build folder and double click on the index.html file to open the generated documentation