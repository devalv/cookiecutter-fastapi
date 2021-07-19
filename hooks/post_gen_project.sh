#!/bin/bash -e

echo -ne "Running with "
python --version

echo "Creating new venv .."
python -m pip install -U pipenv
cd backend
python -m pipenv install --dev

echo "Installing pre-commit hooks"
cd ..
git init
pipenv run pre-commit install

echo "Adding pretty-errors"
cd backend
pipenv run python -m pretty_errors

echo "Creating random secret keys"
cp core/.env.example core/.env
cp tests/.env.example tests/.env
sed -i'' -e "s/SECRET_VALUE/$(openssl rand -hex 32)/g" core/.env
sed -i'' -e "s/SECRET_VALUE/$(openssl rand -hex 32)/g" tests/.env

echo "Done.Please read README.md"
