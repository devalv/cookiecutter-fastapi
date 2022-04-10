# Fast API boilerplate

This is a [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template
for a simple **FastAPI** project.

```bash
$ pip install --upgrade cookiecutter
Pre-commit should be installed before pulling template.
$ pip install pre-commit
$ cookiecutter gh:devalv/cookiecutter-fastapi
Install pipenv and project dependencies
$ python -m pip install -U pipenv
$ cd backend && pipenv install --dev
Pretty errors for extra verbosity
$ pipenv run python -m pretty_errors
```

For additional instructions please see [README](./{{cookiecutter.project_slug}}/README.md)

## Backend
* Pipenv
* FastAPI
* Alembic
* Gino
* Httpx
* Passlib
* Pytest

For additional instructions please see [README](./{{cookiecutter.project_slug}}/backend/README.md)

## Hooks
**pre-commit**:
* isort
* pre-commit-hooks
* black
* flake8

### FAQ

```bash
pre-commit run --all-files
```

## CI
GitHub actions located on **.github/workflows** directory.

### Default rules:
* any commit starts linter check
* any PR/MR starts docker-compose docker-compose-test.yml
* any PR/MR starts codecov uploader
