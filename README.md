# nc-py-install

[![Analysis & Coverage](https://github.com/cloud-py-api/nc-py-install/actions/workflows/analysis-coverage.yml/badge.svg)](https://github.com/cloud-py-api/nc-py-install/actions/workflows/analysis-coverage.yml)
[![codecov](https://codecov.io/gh/cloud-py-api/nc-py-install/branch/main/graph/badge.svg?token=ADRE9TBJ10)](https://codecov.io/gh/cloud-py-api/nc-py-install)
![style](https://img.shields.io/badge/code%20style-black-000000.svg)

![PythonVersion](https://img.shields.io/badge/python-3.9%20%7C%203.10-blue)
![impl](https://img.shields.io/pypi/implementation/nc-py-install)
![pypi](https://img.shields.io/pypi/v/nc-py-install.svg)


Package with helper scripts/functions for [cloud-py-api](https://github.com/cloud-py-api/cloud-py-api) and [nc-py-frm](https://github.com/cloud-py-api/nc-py-frm)

Provides API for installation of python modules and packages.

Usage from PHP, for installing `nc-py-frm`:
```bash
python3 -m nc_py_install --appdata "FRAMEWORK_APP_FOLDER" --target nc_py_frm
```

Where:
* Working directory must contain directory with sources of `nc_py_install`.
* `python3` in most cases must be an absolute path to portable `python3` interpreter.
* `FRAMEWORK_APP_FOLDER` must be an absolute path to folder in `quote+` format.

Additional optional parameter:
* `--loglvl DEBUG` to diagnose problems.


Later more description will arrive...
