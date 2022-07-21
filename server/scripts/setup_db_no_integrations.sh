#!/bin/bash

# run from "/server" directory

# run this when you first set up the database

# export env variables

# check if we can import env from files
if [[ -f ".env" ]]
  then
    export $(grep -v '^#' .env | xargs)
fi

# if env not set at this point, exit
if [[ "$ENV_SET" == "" ]]
  then
    echo "ENV variables not set. Exiting."
    exit 1
fi
# Zebbra user set up
mongosh <<EOF
  use zebbra;

  if (db.getUsers({filter: {'user': "$MONGODB_USER"}}).users.length != 0) {
    db.dropUser("$MONGODB_USER")
  };

  db.createUser(
    {
      user: "$MONGODB_USER",
      pwd: "$MONGODB_PW",
      roles: [ { role: "readWrite", db: "zebbra" } ]
    }
  );
EOF

# Zebbra test user set up
mongosh <<EOF
  use zebbra_test;

  if (db.getUsers({filter: {'user': "$MONGODB_USER"}}).users.length != 0) {
    db.dropUser("$MONGODB_USER")
  };

  db.createUser(
    {
      user: "$MONGODB_USER",
      pwd: "$MONGODB_PW",
      roles: [ { role: "readWrite", db: "zebbra_test" } ]
    }
  );
EOF

# import demo data
# prod db
DEMO_DIR="resources/demo"

mongoimport --db zebbra --collection users --drop --file $DEMO_DIR/users.json --jsonArray
mongoimport --db zebbra --collection workspaces --drop --file $DEMO_DIR/workspaces.json --jsonArray
mongoimport --db zebbra --collection models --drop --file $DEMO_DIR/models_no_integrations.json --jsonArray
mongoimport --db zebbra --collection invite_codes --drop --file $DEMO_DIR/invite_codes.json --jsonArray
mongoimport --db zebbra --collection integration_access --drop --file $DEMO_DIR/integration_access.json --jsonArray
mongoimport --db zebbra --collection accounting_cache --drop --file $DEMO_DIR/accounting_cache.json --jsonArray


# create index
mongosh <<EOF
  use zebbra;

  if (db.accounting_cache.getIndexes().filter(e => e.name == "created_at_1").length > 0) {
    db.accounting_cache.dropIndex("created_at_1");
  };
  db.accounting_cache.createIndex({ "created_at": 1 }, { expireAfterSeconds: $CACHE_TTL });

  if (db.payroll_cache.getIndexes().filter(e => e.name == "created_at_1").length > 0) {
    db.payroll_cache.dropIndex("created_at_1");
  };
  db.payroll_cache.createIndex({ "created_at": 1 }, { expireAfterSeconds: $CACHE_TTL });
EOF
