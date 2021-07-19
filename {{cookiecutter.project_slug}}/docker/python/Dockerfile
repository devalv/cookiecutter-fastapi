FROM python:3.9-slim

RUN set -ex \
    \
    && apt-get update \
    && apt-get install -y gcc python3-dev python3-setuptools \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/{{ cookiecutter.project_slug }}/app
COPY backend/Pipfile* ./
RUN pip install pipenv
RUN pipenv install --dev
