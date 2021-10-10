#!/bin/bash -e

echo -ne "Running with "
python --version

echo "Init git"
git init
git branch -m main

echo "Creating random secret keys"
cd backend
cp core/.env.example core/.env
cp tests/.env.example tests/.env

echo "Creating random secret keys"
sed -i "" -e "s/%%SECRET_VALUE%%/$(openssl rand -hex 32)/g" core/.env
sed -i "" -e "s/%%SECRET_VALUE%%/$(openssl rand -hex 32)/g" tests/.env

echo "Installing pre-commit hook"
pre-commit install

echo "Done."
echo "Please read README.md"
