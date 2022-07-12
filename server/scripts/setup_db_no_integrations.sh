#!/bin/zsh

# run from "/server" directory

# run this when you first set up the database

# source env file

if [ "$1" != "nosource" ]
  then 
    source .env
fi

mongosh <<EOF
  show dbs;
  use zebbra;
  use zebbra_test;

  if (db.getUsers({filter: {'user': "$MONGODB_USER"}}).users.length != 0) {
    db.dropUser("$MONGODB_USER")
  };

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
mongoimport --db zebbra --collection models --drop --file $DEMO_DIR/models_no_integrations.json --jsonArray
mongoimport --db zebbra --collection invite_codes --drop --file $DEMO_DIR/invite_codes.json --jsonArray
mongoimport --db zebbra --collection integration_access --drop --file $DEMO_DIR/integration_access.json --jsonArray
mongoimport --db zebbra --collection integration_cache --drop --file $DEMO_DIR/integration_cache.json --jsonArray


# create index
mongosh <<EOF
  use zebbra;

  if (db.integration_cache.getIndexes().filter(e => e.name == "created_at_1").length > 0) {
    db.integration_cache.dropIndex("created_at_1");
  };
  db.integration_cache.createIndex({ "created_at": 1 }, { expireAfterSeconds: $CACHE_TTL });

  db.integration_cache.getIndexes();
EOF

# todo this should be unnecessary but if I take it out the first auth test in CI fails,
#  likely because the users aren't properly loaded
## test db
mongoimport --db zebbra_test --collection users --drop --file $DEMO_DIR/users.json --jsonArray
mongoimport --db zebbra_test --collection workspaces --drop --file $DEMO_DIR/workspaces.json --jsonArray
mongoimport --db zebbra_test --collection models --drop --file $DEMO_DIR/models_no_integrations.json --jsonArray
mongoimport --db zebbra_test --collection invite_codes --drop --file $DEMO_DIR/invite_codes.json --jsonArray
mongoimport --db zebbra_test --collection integration_access --drop --file $DEMO_DIR/integration_access.json --jsonArray
mongoimport --db zebbra_test --collection integration_cache --drop --file $DEMO_DIR/integration_cache.json --jsonArray