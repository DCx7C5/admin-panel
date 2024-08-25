#!/bin/bash

set -o errexit
set -o nounset

INIT_FAILED=0
db_dump_file="db-$DB_NAME.dump"

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'


check_socket() {
  n=0
  while [ ! -S "$2" ] ;
  do
    if [ "$n" -eq 10 ]; then
      echo -e "${RED}$1 database is missing...${NC}"
      INIT_FAILED=1
      exit 1
    fi
    sleep 1
    ((n+=1))
  done
  echo -e "${GREEN}$1 database found!${NC}"
}

dump_database() {
  if [ "$DB_BACKUP_ON_SHUTDOWN" -eq 1 ]; then
    echo -e "${GREEN}Creating database backup...${NC}"
    echo -e "${GREEN}Writing to: ${NC}${db_dump_file}"
    pg_dump --username "$DB_USER" -Fc -Z 9 --file "/project/$db_dump_file" "$DB_NAME"
    echo -e "${GREEN}...dump successful!${NC}"
  fi
}

restore_database_dump() {
  if [ "$DB_RESTORE_ON_START" -eq 1 ]; then
    echo -e "${GREEN}Restoring database dump...${NC}"
    echo -e "${GREEN}Restoring from: ${NC}${db_dump_file}"
    pg_restore -j 5 --username "$DB_USER" --dbname "$DB_NAME" "/project/$db_dump_file"
    echo -e "${GREEN}...restoring successful!${NC}"
  fi
}

install_and_update_requirements() {
  pip install --user --no-deps --no-cache-dir -U pip
  pip install --user --no-deps --no-cache-dir -r /project/requirements.txt
}

shutdown_hook() {
  dump_database
  echo -e "${GREEN}Shutting down ${RED}DJANGO${GREEN} docker container...${NC}"
  sleep 2
}

trap 'shutdown_hook' SIGTERM SIGINT

# Check Django project dir is mounted
if [ ! -f manage.py ]; then
  echo -e "${RED}Project root is missing...${NC}"
  INIT_FAILED=1
else
  echo -e "${GREEN}Project root found!${NC}"
fi


check_socket Postgresql /var/run/postgresql/.s.PGSQL.5432 &
check_socket Redis /tmp/redis/redis.sock

if [ $INIT_FAILED -eq 1 ]; then
  echo -e "${RED}Dropping into an interactive shell...${NC}"
  exec /bin/bash
fi

echo -e "${GREEN}Creating migrations if needed...${NC}"
python manage.py makemigrations
echo -e "${GREEN}Migrate database if possible...${NC}"
python manage.py migrate
echo -e "${GREEN}Initialisation successfull!${NC}"

"${@}" &
wait $!
shutdown_hook