# Server

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Setup

### Python virtual environment

> Please make sure you're using Python >= 3.10

```shell
# /server
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Database
```shell
# install mongo db on MacOS with homebrew
brew install mongodb-community@5.0.7
# mongo db path
mongod --dbpath=/Users/<user>/data/db
sudo chown -R `id -un` /Users/<user>/data/db
sudo chown -R `id -un` /Users/leopoldpfeiffer/data/db

# start service
brew services start mongodb-community

# stop service
brew services stop mongodb-community

# or run as background process
mongod --config /usr/local/etc/mongod.conf --fork
```

## Testing

We use pytest for unit tests.

```shell
# /server
make test

# or
python -m pytest tests
```