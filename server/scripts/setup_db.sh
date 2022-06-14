#!/bin/zsh

# run this when you first set up the database

# source env file
source ../.env

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