#!/bin/zsh

# run from "/server" directory

# run this when you first set up the database

# source env file
ls -la
. .env

mongosh <<EOF
  show dbs;
  use zebbra;
  use zebbra_test;

  if (db.getUsers({filter: {'user': "$MONGODB_USER"}}).users.length != 0) {
    db.dropUser("$MONGODB_USER")
  }

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
DEMO_DIR="resources/demo"

mongoimport --db zebbra --collection users --drop --file $DEMO_DIR/users.json --jsonArray
mongoimport --db zebbra --collection workspaces --drop --file $DEMO_DIR/workspaces.json --jsonArray

# test db
mongoimport --db zebbra_test --collection users --drop --file $DEMO_DIR/users.json --jsonArray
mongoimport --db zebbra_test --collection workspaces --drop --file $DEMO_DIR/workspaces.json --jsonArray
