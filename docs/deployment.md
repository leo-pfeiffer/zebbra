# Deploying the Zebbra API

Users are encouraged to deploy their own instance of the Zebbra API. This way, you have controll over your own data (and our deployment has to cope with less traffic).

We will deploy the API using gunicorn as the application server, and NGINX as the reverse proxy to handle HTTPS etc.

This deployment guide was tested on Ubuntu 20.04.

The deployment guide assumes the following:

- Logged in as superuser with username `zebbra`
- Python 3.10 is installed and the default Python version. We recommend using pyenv ([how to](https://www.liquidweb.com/kb/how-to-install-pyenv-on-ubuntu-18-04/))
- Mongo DB Community edition version 5.0 is installed and running ([how to](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/))

We further assume that you start out in the user's home directory `/home/zebbra`.

---

> Much of this guide was based on similar tutorials by [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04) and [Vultr](https://www.vultr.com/docs/how-to-deploy-fastapi-applications-with-gunicorn-and-nginx-on-ubuntu-20-04/).

---

## Project set up

> The project setup is similar to the setup for local development, so if you've set up the project locally before, feel free to step this step. 

### Repository and virtual environment

Start by cloning the repository, setting up a virtual environment and installing the required dependencies.

```shell
# /home/zebbra

# clone the repository
git clone git@github.com:leo-pfeiffer/zebbra.git

# set up virtual environment
cd zebbra/server
python -m venv venv
source venv/bin/activate

# install dependencies
make requirements
```

### `.env` file

Next, create the `.env` file with the environment variables. Run the following to create a file with the starter template. You will have to fill out the missing variable assignments (e.g. secrets etc.).


```shell
# /home/zebbra/zebbra/server

cat <<EOF > .env
# VALIDATION
ENV_SET="true"

# BASE URL
ZEBBRA_BASE_URL=
#ZEBBRA_BASE_URL="http://localhost:8000"

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
# /home/zebbra/zebbra/server

make setup_db
```

This creates the required users, sets up the indexes for caching, and loads some demo data.

### 🚩 Checkpoint

At this point you should be able to run the app with gunicorn.

```shell
gunicorn --bind 0.0.0.0:5000 main:app -k uvicorn.workers.UvicornWorker
```

Head to `http://your-domain.com:5000` (remember to allow port 5000 in your firewall first).

## Setting up the Zebbra service

Next, we will have to set up the Zebbra service that will later be run by NGINX.

### Service configuration

Run

```shell
sudo nano /etc/systemd/system/zebbra.service
```

and paste the following:

```ini
[Unit]
Description=Gunicorn instance to serve Zebbra API
After=network.target

[Service]
User=zebbra
Group=www-data
WorkingDirectory=/home/zebbra/zebbra/server
Environment="PATH=/home/zebbra/zebbra/server/venv/bin"
ExecStart=/home/zebbra/zebbra/server/venv/bin/gunicorn --workers 3 --bind unix:zebbra.sock -m 007 main:app -k uvicorn.workers.UvicornWorker --forwarded-allow-ips="*"

[Install]
WantedBy=multi-user.target
```

### Start and enable the service

With the service configuration in place, we can sart and enable the Zebbra service.

```shell
sudo systemctl start zebbra
sudo systemctl enable zebbra
```

### 🚩 Checkpoint 
You can confirm that all is well by runing `sudo systemctl status zebbra`. Your Zebbra service is running.

## Set up NGINX

We can now proceed to set up NGINX.

### Installing NGINX

If you don't already have NGINX installed on your server, you can do so like this:

```shell
sudo apt update
sudo apt install nginx
sudo ufw allow 'Nginx HTTP'
```

### Create the Zebbra site

With NGINX installed, we can add the Zebbra site.

Run

```shell
sudo nano /etc/nginx/sites-available/zebbra
```

and paste the following content. Remember to change `your_domain` to your actual domain.

```conf
server {
   listen 80;
   server_name your_domain www.your_domain;

   location / {
       include proxy_params;
       proxy_pass http://unix:/home/zebbra/zebbra/server/zebbra.sock;
   }
}
```

This site can now be enabled by setting up a symlink.

```shell
sudo ln -s /etc/nginx/sites-available/zebbra /etc/nginx/sites-enabled
```

You can confirm that the file is correctly formatted by running `sudo nginx -t`.

We now need to restart the NGINX service to pick up the Zebbra service.

```shell
sudo systemctl restart nginx
```

### Update firewall

Lastly, we need to update the firewall to allow full access to NGINX.

```shell
sudo ufw allow 'Nginx Full'
```

### 🚩 Checkpoint

The Zebbra API should now be deployed and accessible via `http://your_domain`.

## Setting up HTTPS

Since Zebbra handles financial data, security is paramount. In this step, access to the Zebbra API is secured with HTTPS. We will use a free Let's Encrypt certificate.

First, install the python certbot for NGINX.

```shell
sudo apt install python3-certbot-nginx
```

Next, request and generate a SSL certificate.

```shell
sudo certbot --nginx -d your_domain.xyz -d www.your_domain
```

When prompted, accept the T&Cs and select (2) to redirect all HTTP requests to HTTPS automatically.

Lastly, we can revoke the NGINX HTTP permission from the firewall again.

```shell
sudo ufw delete allow 'Nginx HTTP'
```

## 🏁 Checkpoint

You're done! If everything went well, you can now access the Zebbra API on `https://your_domain`.

# Deploying the Zebbra front end

Since the Zebbra front end is implemented as a Nuxt.js app, you can deploy it just as every other Nuxt.js out there. We recommend deploying via Netlify, which is free and works entirely out of the box. A guide is provided in the [official Nuxt documentation](https://v3.nuxtjs.org/guide/deploy/providers/netlify/). The only necessary modification will be to set the environment variable `BACKEND_URL_BASE`  of the front end to the URL on which your instance of the Zebbra API is deployed.
