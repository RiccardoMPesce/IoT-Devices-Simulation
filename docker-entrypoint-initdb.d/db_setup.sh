#!/usr/bin/env bash

echo "--------------------------------------"
echo "      --------------------------      "
echo "          ------------------          "
echo "              ----------              "
echo "Creating application user and database"

mongo ${MONGO_INITDB_DATABASE} \
        --host localhost \
        --port ${MONGO_PORT} \
        -u ${MONGO_INITDB_ROOT_USERNAME} \
        -p ${MONGO_INITDB_ROOT_PASSWORD} \
        --authenticationDatabase admin \
        --eval "db.createUser({user: '${DATABASE_USER}', pwd: '${DATABASE_PASSWORD}', roles:[{role:'readWrite', db: '${MONGO_INITDB_DATABASE}'}]});"

mongo --eval "db.auth('$MONGO_INITDB_ROOT_USERNAME', '$MONGO_INITDB_ROOT_PASSWORD'); db = db.getSiblingDB('$MONGO_INITDB_DATABASE'); db.createCollection('devices'); db.createCollection('measures');"

echo "Done"
echo "              ----------              "
echo "          ------------------          "
echo "      --------------------------      "
echo "--------------------------------------"
