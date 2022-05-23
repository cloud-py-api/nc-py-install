import subprocess
import sys
from os import path
from urllib import parse

import pytest

import nc_py_install

APP_DATA_DIR = path.abspath("./cloud_py_api")
MAIN_ARGS = ["--appdata", parse.quote_plus(APP_DATA_DIR)]

if not sys.executable.startswith(APP_DATA_DIR):
    pytest.skip("skipping `no pip tests` on system interpreter.", allow_module_level=True)


@pytest.fixture(scope="function")
def remove_pip():
    nc_py_install.pckg_delete("nc_py_frm")
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "pip", "-y"], capture_output=False, check=True)
    yield


def test_without_pip(remove_pip):
    # Check must fail here and return exitcode = 1
    assert nc_py_install.main(MAIN_ARGS + ["--check"]) == 1
    # Install must succeed
    assert nc_py_install.main(MAIN_ARGS + ["--install"]) == 0
    # Call here `check` again to see that `install` was successful.
    assert nc_py_install.main(MAIN_ARGS + ["--check"]) == 0


@pytest.fixture(scope="module")
def install_old_pip():
    subprocess.run([sys.executable, "-m", "pip", "install", "pip<21"], capture_output=False, check=True)
    nc_py_install.pckg_delete("nc_py_frm")
    yield
    subprocess.run([sys.executable, "-m", "pip", "install", "-U", "pip"], capture_output=False, check=True)


def test_old_pip(install_old_pip):
    # Check must fail here and return exitcode = 1
    assert nc_py_install.main(MAIN_ARGS + ["--check"]) == 1
    # Install must succeed
    assert nc_py_install.main(MAIN_ARGS + ["--install"]) == 0
    # Call here `check` again to see that `install` was successful.
    assert nc_py_install.main(MAIN_ARGS + ["--check"]) == 0
