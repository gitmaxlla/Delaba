main := "-f docker-compose.yml"
dev := "-f docker-compose.dev.yml"
test := "-f docker-compose.test.yml"

exit := "--exit-code-from"

# Same as up-dev
default: up-dev

# Launch interactive .env file builder
build-dotenv:
  python3 dotenv-helper

up-dev:
  docker compose {{main}} {{dev}} up --build

up-prod:
  just down
  docker compose {{main}} up -d --build

down:
  docker compose {{main}} {{dev}} {{test}} down --remove-orphans

test-backend-unit:
  docker compose {{main}} {{dev}} {{test}} up {{exit}} backend-unit-testing backend-unit-testing

test-backend-integration:
  just down
  docker compose {{main}} {{dev}} {{test}} up -V {{exit}} backend-integration-testing backend-integration-testing

test-backend-coverage:
  just down
  docker compose {{main}} {{dev}} {{test}} up -V {{exit}} backend-coverage-testing backend-coverage-testing

test-frontend-components:
  docker compose {{main}} {{dev}} {{test}} up {{exit}} frontend-components-testing frontend-components-testing

test-frontend-scenarios:
  docker compose {{main}} {{dev}} {{test}} up {{exit}} frontend-scenarios-testing frontend-scenarios-testing

test-frontend-coverage:
  docker compose {{main}} {{dev}} {{test}} up {{exit}} frontend-coverage-testing frontend-coverage-testing

test-e2e:
  just down
  docker compose {{main}} {{dev}} {{test}} up {{exit}} e2e-testing e2e-testing

# Recommended for dev usage only
test-all: test-backend-coverage test-frontend-coverage test-e2e
