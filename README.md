# Aleksei Devyatkin`s python simple project template

This is a [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template
for a simple **FastAPI** project.

```bash
$ pip install --upgrade cookiecutter
$ cookiecutter gh:devalv/cookiecutter-fastapi
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
