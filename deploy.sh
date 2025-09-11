#!/bin/bash


# Poetry install dependencies
poetry install

# Enter venv
source .venv/bin/activate

# Launch test_db
docker compose -f docker-compose-local.yaml up -d test_db

# Enter project directory
cd project

# Run Pytest
pytest

pytest_exit_status=$?

# Check the exit status and handle the failures
if [ $pytest_exit_status -eq 0 ]; then
  echo "Pytest succeeded"

else
  echo "Pytest failed"

  # Close test_db
  cd ..
  docker compose -f docker-compose-local.yaml down test_db -t 1
  docker network prune --force

  exit 1
fi

# Continue with the script if Pytest succeeded
cd ..
docker compose -f docker-compose-local.yaml down test_db -t 1
docker network prune --force

# ...