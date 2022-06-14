# Server

## Setup

### Python virtual environment

> Please make sure you're using Python >= 3.10

```shell
# /server
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements
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

