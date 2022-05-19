# Contributing to nc-py-install

Bug fixes, feature additions, tests, documentation and more can be contributed via [issues](https://github.com/cloud-py-api/nc-py-install/issues) and/or [pull requests](https://github.com/cloud-py-api/nc-py-install/pulls). All contributions are welcome.

## Bug fixes, feature additions, etc.

Please send a pull request to the `main` branch.  Feel free to ask questions at [discussions](https://github.com/cloud-py-api/cloud_py_api/discussions)

- Fork the nc-py-install repository.
- Create a branch from `main`.
- Install dev requirements with `pip install ".[dev]"`
- Develop bug fixes, features, tests, etc.
- Run the test suite. How to run coverage tests, you can see at [coverage workflow](https://github.com/cloud-py-api/nc-py-install/blob/master/.github/workflows/analysis-coverage.yml)
- Run PyLint inside project root: `pylint nc_py_install`
- Do not forget to install `pre-commit` hooks by `pre-commit install` command.
- Create a pull request to pull the changes from your branch to the nc-py-install `main`.

### Guidelines

- Separate code commits from reformatting commits.
- Provide tests for any newly added code.
- Follow PEP 8.
- When committing only documentation changes please include `[ci skip]` in the commit message to avoid running tests.
- Update CHANGELOG.md as needed or appropriate with your bug fixes, feature additions and tests.

## Security vulnerabilities

Please see our [security policy](https://github.com/cloud-py-api/nc-py-install/blob/master/SECURITY.md).
