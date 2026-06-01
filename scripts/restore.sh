#!/bin/bash

FILE=$1

if [ -z "$FILE" ]; then
  echo "Usage: ./restore.sh backup.sql"
  exit 1
fi

cat $FILE | docker exec -i postgres_db psql -U postgres fastapi_db

echo "Restore completed"