import subprocess
import sys
from os import path
from unittest.mock import patch
from urllib import parse

import pytest

import nc_py_install

APP_DATA_DIR = path.abspath("./cloud_py_api")
MAIN_ARGS = ["--appdata", parse.quote_plus(APP_DATA_DIR)]


@pytest.fixture(scope="function")
def remove_frm():
    # remove it if it was previously installed by call to internal api.
    nc_py_install.pckg_delete("nc_py_frm")
    yield
    nc_py_install.pckg_delete("nc_py_frm")


def test_main(remove_frm):
    # Check must fail here and return exitcode = 1
    assert nc_py_install.main(MAIN_ARGS + ["--check"]) == 1
    # Install must succeed
    assert nc_py_install.main(MAIN_ARGS + ["--install"]) == 0
    # Call here `check` again to see that `install` was successful.
    assert nc_py_install.main(MAIN_ARGS + ["--check"]) == 0
    # Update must succeed
    assert nc_py_install.main(MAIN_ARGS + ["--update"]) == 0


def test_dev_logs(remove_frm):
    assert nc_py_install.main(MAIN_ARGS + ["--check", "--dev"]) == 1
    assert nc_py_install.main(MAIN_ARGS + ["--install", "--dev"]) == 0
    assert nc_py_install.main(MAIN_ARGS + ["--check", "--dev"]) == 0


@patch("nc_py_install.cli.getuser", side_effect=OSError("can handle"))
def test_exception_handled_get_user(_mock_class, remove_frm):
    assert nc_py_install.main(MAIN_ARGS + ["--install"]) == 0


@patch("nc_py_install.cli.getuser", side_effect=Exception("can not handle"))
def test_exception_not_handled_get_user(_mock_class, remove_frm):
    assert nc_py_install.main(MAIN_ARGS + ["--install"]) == 2


def test_subprocess(remove_frm):
    args = [sys.executable, "-m", "nc_py_install", "--appdata", parse.quote_plus(APP_DATA_DIR)]
    r = subprocess.run(args + ["--check"], capture_output=False)
    assert r.returncode == 1
    r = subprocess.run(args + ["--install"], capture_output=False)
    assert r.returncode == 0
    r = subprocess.run(args + ["--check"], capture_output=False)
    assert r.returncode == 0
    r = subprocess.run(args + ["--update"], capture_output=False)
    assert r.returncode == 0
