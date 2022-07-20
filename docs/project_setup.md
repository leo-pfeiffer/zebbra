# Project Setup

This guide walks through the process of setting up Zebbra locally for development.

## Prerequisites

To run Zebbra you will have to make sure the following is given on your machine:

- Python 3.10+ is installed, we recommend pyenv ([how to](https://www.liquidweb.com/kb/how-to-install-pyenv-on-ubuntu-18-04/))
- Node 16+ is installed ([how to](https://nodejs.org/en/download/package-manager/))
- MongoDB Community Edition 5.0 is installed and running ([how to](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/))

## Repository

Start by cloning the repository, setting up a virtual environment and installing the required dependencies.

```shell
# clone the repository
git clone git@github.com:leo-pfeiffer/zebbra.git
```

## Backend setup

We start by setting up the backend, that is the API server, as well as the database.

First, create a virtual environment in the `server` directory
```shell
# zebbra/server

python -m venv venv
source venv/bin/activate
```

Next, use the `make` command to install all package requirements via pip.

```shell
# install dependencies
make requirements
```

### `.env` file

Next, create the `.env` file with the environment variables. Run the following to create a file with the starter template. You will have to fill out the missing variable assignments (e.g. secrets etc.).


```shell
# zebbra/server

cat <<EOF > .env
# VALIDATION
ENV_SET="true"

# BASE URL
ZEBBRA_BASE_URL="http://localhost:8000"

# SETTINGS
ENV_ENCRYPT_PASS=

# AUTH
AUTH_SECRET=
AUTH_ALGO="HS256"
# 30 days in minutes
AUTH_TOKEN_EXPIRE=43200

# MONGO DB
MONGODB_USER=
MONGODB_DB=
MONGODB_PW=
MONGODB_URL="127.0.0.1:27017"

# XERO
XERO_CLIENT_ID=
XERO_CLIENT_SECRET=

# GUSTO
GUSTO_CLIENT_ID=
GUSTO_CLIENT_SECRET=

# CACHE
# 24 hrs in seconds
CACHE_TTL=86400
EOF
```

### Database

If you've set up the `.env` file correctly, you can use the default script to set up the database.

```shell
# zebbra/server

make setup_db
```

This creates the required users, sets up the indexes for caching, and loads some demo data.

### Run the server

At this point you should be able to run the app with the provided `run_server` command on port 8000.

```shell
make run_server
```

![Zebbra API](https://user-images.githubusercontent.com/50983452/180023467-f8e66e8b-fad0-4063-952d-3d64b3f14f10.png)


## Client setup

Setting up the client is comparatively straightforward. 

### Install requirements

Start by installing the node modules from the `webclient` directory.

```shell
# zebbra/webclient

npm install
```

### `.env` file

Like the server, the client requires a simple `.env` file. You can create it with the following command.

```shell
# zebbra/webclient

cat <<EOF > .env
# URLS
FRONTEND_URL_BASE="http://localhost:3000"
BACKEND_URL_BASE="http://localhost:8000"
EOF
```

### Build and run the client

Lastly, we can build and run the client, like so:

```shell
# zebbra/webclient

npm run dev
```

The client will be served on `http://localhost:3000`.

![Zebbra client](https://user-images.githubusercontent.com/50983452/180023257-d47d1fbd-0a94-4582-be27-4559030a9a01.png)
