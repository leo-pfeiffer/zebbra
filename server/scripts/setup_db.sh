#!/bin/zsh

# run from "/server" directory

# run this when you first set up the database

# source env file
source .env


mongosh <<EOF
  show dbs;
  use zebbra;
  db.createUser(
    {
      user: "$MONGODB_USER",
      pwd: "$MONGODB_PW",
      roles: [ { role: "readWrite", db: "zebbra" } ]
    }
  );
EOF

# import demo data
mongoimport --db zebbra --collection users --drop --file scripts/demo_data.json --jsonArray
