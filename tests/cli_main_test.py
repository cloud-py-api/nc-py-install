from urllib import parse
from os import path

import pytest
import nc_py_install


APP_DATA_DIR = path.abspath("./cloud_py_api")
MAIN_ARGS = ["--appdata", parse.quote_plus(APP_DATA_DIR), "--target"]


@pytest.mark.parametrize(
    "package_name, version",
    (
        ("pg8000", "1.26.0"),
        ("pymysql", ""),
        ("pillow-heif", "0.2.2"),
        ("pillow-heif", ""),
        ("SQLAlchemy", "")
    )
)
def test_subpackages(package_name, version):
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