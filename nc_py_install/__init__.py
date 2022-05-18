"""
Import all possible stuff that can be used in `nc-py-frm` and `nc-py-api`
"""

from ._version import __version__
from .api import pckg_check, pckg_install, pckg_delete, requirements_check, requirements_delete
from .api import OPTIONS, update_pip_info
from .api import (
    get_package_version,
    get_package_dependencies,
    get_package_location,
    get_userbase_for_app,
    get_site_packages,
    add_python_path,
    remove_python_path,
)
from .cli import main
