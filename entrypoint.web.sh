#!/bin/bash

set -o errexit
set -o nounset

PG_LOCKFILE="/var/run/postgresql/.s.PGSQL.5432.lock"
INIT_FAILED=0

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'  # No Color

# Function to drop a shell
drop_shell() {
  echo -e "${RED}Dropping into an interactive shell...${NC}"
  exec /bin/bash
}

# Check Django project dir is mounted
if [ ! -f manage.py ]; then
  echo -e "${RED}Project root is missing...${NC}"
  INIT_FAILED=1
else
  echo -e "${GREEN}Project root found!${NC}"
fi

# Wait for PostgreSQL database
if [ ! -f "$PG_LOCKFILE" ]; then
  echo -e "${RED}PostgreSQL database is missing...${NC}"
  INIT_FAILED=1
else
  echo -e "${GREEN}PostgreSQL database found!${NC}"
fi

# Check for changes in requirements.txt
if [ ! -f /project/requirements.txt ]; then
  INIT_FAILED=1
else
  if [ ! -f /home/user/req.bkp ]; then
    echo -e "${GREEN}Container first start detected...installing modules!${NC}"
    cp /project/requirements.txt /home/user/req.bkp
    pip install --user --no-deps --no-cache-dir -r /project/requirements.txt
  elif ! cmp -s /home/user/req.bkp /project/requirements.txt; then
    echo -e "${GREEN}Changes in requirements.txt detected...updating modules!${NC}"
    pip install --user --no-deps --no-cache-dir -r /project/requirements.txt
    cp /project/requirements.txt /home/user/req.bkp
  fi
fi

if [ $INIT_FAILED -eq 1 ]; then
  echo -e "${RED}requirements.txt is missing...${NC}"
  drop_shell
fi

echo -e "${GREEN}Initialisation successfull!${NC}"
exec "$@"
