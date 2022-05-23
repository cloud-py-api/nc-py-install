import os
import subprocess
from unittest.mock import patch

import pytest

import nc_py_install


def mocked_run_no_wget(*args, **kwargs):
    if str(args[0]).find("wget") != -1:
        raise FileNotFoundError
    return subprocess.run(*args, **kwargs)


def test_download_file_with_curl():
    with patch("nc_py_install.api.run", mocked_run_no_wget):
        assert nc_py_install.api.download_file(
            "https://github.com/cloud-py-api/nc-py-install/blob/master/README.md", "test_download.md"
        )
        os.remove("test_download.md")


def mocked_run_no_curl_no_wget(*args, **kwargs):
    if str(args[0]).find("wget") != -1 or str(args[0]).find("curl") != -1:
        raise FileNotFoundError
    return subprocess.run(*args, **kwargs)


def test_no_curl_no_wget():
    with patch("nc_py_install.api.run", mocked_run_no_curl_no_wget):
        assert not nc_py_install.api.download_file(
            "https://github.com/cloud-py-api/nc-py-install/blob/master/README.md", "test_download.md"
        )
        assert not os.path.isfile("test_download.md")


def test_no_requirements_parser(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(nc_py_install.api, "requirements", None)
        with pytest.warns(UserWarning):
            nc_py_install.requirements_check("requirements.txt")
