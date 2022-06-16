#!/bin/zsh

# run from "/server" directory

# run this when you first set up the database

# source env file
source .env


mongosh <<EOF
  show dbs;
  use zebbra;
  use zebbra_test;
  db.createUser(
    {
      user: "$MONGODB_USER",
      pwd: "$MONGODB_PW",
      roles: [ { role: "readWrite", db: "zebbra" }, { role: "readWrite", db: "zebbra_test" } ]
    }
  );
EOF

# import demo data
# prod db
mongoimport --db zebbra --collection users --drop --file scripts/demo_users.json --jsonArray

# test db
mongoimport --db zebbra_test --collection users --drop --file scripts/demo_users.json --jsonArray
