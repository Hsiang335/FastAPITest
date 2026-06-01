#!/bin/bash

DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR=./backups

mkdir -p $BACKUP_DIR

docker exec postgres_db pg_dump -U postgres fastapi_db > $BACKUP_DIR/backup_$DATE.sql

echo "Backup completed: backup_$DATE.sql"