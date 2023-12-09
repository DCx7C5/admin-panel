#!/bin/bash

set -o errexit
set -o nounset

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'  # No Color

# Check Django project dir is mounted
if [ ! -f manage.py ]; then
  echo -e "${RED}Project root is missing...${NC}"
  echo -e "${RED}Dropping into emergency shell...${NC}"
  exec /bin/bash
else
  echo -e "${GREEN}Project root found!${NC}"
  # Install package.json
  npm -D install
  npm audit fix
fi

echo -e "${GREEN}Initialisation successfull!${NC}"
exec "$@"
