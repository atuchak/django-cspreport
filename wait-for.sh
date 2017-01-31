#!/usr/bin/env bash

set -e

host=$DB_HOST
export PGPASSWORD=$POSTGRES_PASSWORD

echo "Postgres host=$DB_HOST adp password=$PGPASSWORD"

until psql -h "$host" -U "postgres" -c '\l'; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing command"
