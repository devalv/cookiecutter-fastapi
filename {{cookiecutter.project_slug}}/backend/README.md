# {{ cookiecutter.project_name }}

## FAQ

### First use

#### 1. Fill in external auth secrets in your **.env**
```bash
GOOGLE_CLIENT_ID=
GOOGLE_USERINFO_SCOPE=
GOOGLE_CLIENT_SECRETS_JSON=
```

#### 2. Run docker or local services and start the app.

### Installation without docker
Try dotfiles templates [MAC](https://github.com/devalv/mac_dotfiles) or [Ubuntu](https://github.com/devalv/ul_dotfiles).

### Alembic

#### set ENV variable for alembic
`export PYTHONPATH=backend`

#### Migrate to the last migration
`alembic upgrade head`

#### Create new migration for project schema
`alembic revision --autogenerate -m "text"`

### Tests
Database connection options should be at ENV. You can use env_files plugin, and create tests/.env data + additional docker-compose configuration file:

## Dir structure

```
├── core
│   ├── database
│   │   ├── models
│   │   └── migrations
│   ├── schemas
│   ├── services
│   ├── utils
│   ├── .env
│   └── config.py
├── tests
│   ├── snapshots
│   ├── .env
│   └── conftest.py
├── api
│   └── v1
│       └── handlers
├── main.py
└── .coveragerc
```

### root-dir
Project outer-startup files, such as:
* alembic configuration
* pytest configuration
* uvicorn app file
* project requirements lists
* coverage configuration

### core
Core project features such as:
* settings (config.py)
* database migrations and models
* services (business logic)
* schemas (pydantic models)
* utils (extra utils, such as fastapi-pagination custom Page)

### tests
Project tests

### api
Project API by versions (v1, v2 and etc.).
