[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }})

# {{ cookiecutter.project_name }}
For additional instructions please see
[Wiki](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/wiki)

## Git hooks
Please install [pre-commit](https://pre-commit.com) hook.

```bash
pre-commit install
```

## Project directory structure

```
├── .github
│   ├── workflows
├── backend
│   ├── api
│   ├── core
│   │   ├── database
│   │   ├── ...
│   │   └── .env
│   ├── tests
│   │   ├── snapshot
│   │   ├── ...
│   │   └── .env
│   ├── .coveragerc
│   ├── .isort.cfg
│   ├── ...
│   └── Pipfile
├── docker
│   ├── python
│   │   └── Dockerfile
│   ├── docker-compose-test.yml
│   └── docker-compose.yml
├── frontend
├── .gitignore
├── ...
└── .pre-commit-config.yaml
```

### backend
For additional instructions please see [README](./backend/README.md)

### docker
Docker-images and docker-compose configuration files.

#### FAQ

```bash
docker system prune -a -f --volumes
docker-compose -f docker/docker-compose.yml --env-file=backend/core/.env up --build
docker-compose -f docker/docker-compose-test.yml --env-file=backend/tests/.env  up --abort-on-container-exit --exit-code-from app-tests --build
```

## Participation
```
Fork -> Changes -> PR
```

## Frontend
Add your frontend repo as a git submodule
```bash
git submodule add https://your-frontend-repo
```
Review the state of the repository
```bash
git status
...
new file:   .gitmodules
new file:   frontend
```
Commit the changes to the repository
```bash
git add .gitmodules frontend/
git commit -m "added submodule"
...
```
