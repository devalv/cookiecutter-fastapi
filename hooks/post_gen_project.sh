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

echo "Please read README.md"
cd ..
cat README.md

echo "Done"
