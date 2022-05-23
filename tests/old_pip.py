import subprocess
import sys
from os import path
from urllib import parse

import pytest

import nc_py_install

APP_DATA_DIR = path.abspath("./cloud_py_api")
MAIN_ARGS = ["--appdata", parse.quote_plus(APP_DATA_DIR), "--target"]

if not sys.executable.startswith(APP_DATA_DIR):
    pytest.skip("skipping `old pip test` on system interpreter.", allow_module_level=True)


@pytest.fixture(scope="module")
def install_old_pip():
    subprocess.run([sys.executable, "-m", "pip", "install", "pip<21"], capture_output=False, check=True)
    yield
    subprocess.run([sys.executable, "-m", "pip", "install", "-U", "pip"], capture_output=False, check=True)


def test_subpackages(install_old_pip):
    package_name = "pg8000"
    version = ""
    # Check must fail here and return exitcode = 1
    r_code = nc_py_install.main(MAIN_ARGS + [package_name] + ["--check"])
    assert r_code == 1
    install_string = package_name + "==" + version if version else package_name
    # Install must succeed
    r_code = nc_py_install.main(MAIN_ARGS + [install_string] + ["--install"])
    assert r_code == 0
    if version:
        r_code = nc_py_install.main(MAIN_ARGS + [package_name] + ["--update"])
        assert r_code == 0
    # Clean up, by deleting package.
    r_code = nc_py_install.main(MAIN_ARGS + [install_string] + ["--delete"])
    assert r_code == 0
    # Call here `check` again to see that `delete` was successful.
    r_code = nc_py_install.main(MAIN_ARGS + [package_name] + ["--check"])
    assert r_code == 1
