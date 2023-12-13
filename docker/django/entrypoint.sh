#!/bin/bash

set -o errexit
set -o nounset

INIT_FAILED=0
db_dump_file="db-$DB_NAME.dump"

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

check_sql_db() {
  # Check for PostgreSQL database
  if [ ! -S "/var/run/postgresql/.s.PGSQL.5432" ]; then
    echo -e "${RED}PostgreSQL database is missing...${NC}"
    INIT_FAILED=1
  else
    echo -e "${GREEN}PostgreSQL database found!${NC}"
    INIT_FAILED=0
  fi
}

check_redis_db() {
  # Check for redis channel layer database
  if [ ! -S "/tmp/redis/redis.sock" ]; then
    echo -e "${RED}Redis channel layer database is missing...${NC}"
    INIT_FAILED=1
  else
    echo -e "${GREEN}Redis channel layer database found!${NC}"
    INIT_FAILED=0
  fi
}

make_database_dump() {
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
  make_database_dump
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

# Check for changes in requirements.txt
if [ ! -f /project/requirements.txt ]; then
  echo -e "${RED}requirements.txt is missing...${NC}"
  INIT_FAILED=1
else
  if [ ! -f /home/user/req.bkp ]; then
    echo -e "${GREEN}Container first start detected...installing modules!${NC}"
    cp /project/requirements.txt /home/user/req.bkp
    install_and_update_requirements
  elif ! cmp -s /home/user/req.bkp /project/requirements.txt; then
    echo -e "${GREEN}Changes in requirements.txt detected...updating modules!${NC}"
    install_and_update_requirements
    cp /project/requirements.txt /home/user/req.bkp
  fi
fi

check_redis_db
check_sql_db

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