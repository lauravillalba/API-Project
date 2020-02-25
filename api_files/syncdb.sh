#!/bin/bash


LOCAL_DB="mongodb://localhost/api_db"
REMOTE_DB= "mongodb+srv://admin:admin@cluster0-xtczl.mongodb.net/api_db?retryWrites=true&w=majority"

# Load REMOTE_DB env variable
source .private.env

echo "Importing from local db: $LOCAL_DB"
echo "\t ...to remote: $REMOTE_DB"

mongodump --uri=$LOCAL_DB
mongorestore --uri=$REMOTE_DB