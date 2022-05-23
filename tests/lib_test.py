from os import path, remove

import pytest
import requirements

import nc_py_install

APP_DATA_DIR = path.abspath("./cloud_py_api")
nc_py_install.OPTIONS.app_data = APP_DATA_DIR
nc_py_install.update_pip_info()


@pytest.mark.parametrize(
    "package_name, version",
    (
        ("pg8000", "1.26.0"),
        ("pymysql", ""),
        ("pillow-heif", "0.2.2"),
        ("pillow-heif", ""),
        ("SQLAlchemy", ""),
        ("nc_py_frm", ""),
    ),
)
def test_subpackages(package_name, version):
    nc_py_install.pckg_delete(package_name)
    yes, no, no_opt = nc_py_install.pckg_check(package_name)
    assert not yes
    install_string = package_name + "==" + version if version else package_name
    assert nc_py_install.pckg_install(install_string)
    if version:
        added_path = nc_py_install.add_python_path(nc_py_install.api.get_site_packages(), first=True)
        assert nc_py_install.get_package_version(package_name) == version
        assert nc_py_install.pckg_install(package_name, extra_args=["--upgrade"])
        assert nc_py_install.get_package_version(package_name) != version
        nc_py_install.remove_python_path(added_path)
    assert nc_py_install.pckg_delete(install_string)
    yes, no, no_opt = nc_py_install.pckg_check(package_name)
    assert not yes


@pytest.fixture(params=["boto3", "boto3==1.23.1"])
def requirements_create(request):
    with open("requirements.txt", mode="w") as f:
        f.write(request.param + "\n")
    yield
    remove("requirements.txt")


def test_requirements(requirements_create):
    def requirements_delete(requirements_file: str, userbase: str = "") -> None:
        dependencies = []
        with open(requirements_file, "r", encoding="utf-8") as f:
            for req in requirements.parse(f):
                dependencies.append(req.name)
        nc_py_install.pckg_delete(dependencies, userbase=userbase)

    requirements_delete("requirements.txt")
    yes, no = nc_py_install.requirements_check("requirements.txt")
    assert not yes
    assert nc_py_install.pckg_install("-r requirements.txt")
    yes, no = nc_py_install.requirements_check("requirements.txt")
    assert yes
