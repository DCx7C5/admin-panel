#!/bin/ash

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# exits if any of your variables is not set
set -o nounset

. /project/.env

PG_LOCKFILE="/var/run/postgresql/.s.PGSQL.${DB_PORT:-5432}.lock"
PSQL_CMD="psql --username=$DB_USER --password=$DB_PASS $DB_NAME"
timeout=20
waitc=0

wait_for_postgres_db() {
  local con
  if [ -z "$DB_HOST" ] && [ -z "$DB_PORT" ]; then
    con="-f $PG_LOCKFILE"
  else
    con=$PSQL_CMD
  fi
  until [ "$con" ]; do
    if [ $waitc -eq $timeout ]; then return 1; fi
    echo "Waiting for PostgreSQL..."
    sleep 1
    ${waitc}+=1
  done
  return 0
}

# Check Django project dir is mounted
if [ ! -f manage.py ]; then
  echo "django-root is missing"
  exit 0
fi

# Wait for postgresdatabase
if ! wait_for_postgres_db; then
  echo "DB not reachable"
  exit 0
fi

exec "$@"
