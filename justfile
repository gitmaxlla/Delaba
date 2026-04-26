sudo := if os() == "linux" {"sudo "} else { "" }

main := "-f docker-compose.yml"
dev := "-f docker-compose.dev.yml"
test := "-f docker-compose.test.yml"

# Same as up-dev
default: up-dev

# Launch interactive .env file builder
build-dotenv:
  python3 dotenv-helper

up-dev:
  {{sudo}}docker compose {{main}} {{dev}} up

up-prod:
  {{sudo}}docker compose {{main}} up --build

down:
  {{sudo}}docker compose {{main}} {{dev}} {{test}} down --remove-orphans

test-all:
  #

test-backend-coverage:
  {{sudo}}docker compose {{main}} {{dev}} {{test}} up -V backend-coverage-testing

test-frontend-coverage:
  {{sudo}}docker compose {{main}} {{dev}} {{test}} up frontend-coverage-testing

test-backend-unit:
  {{sudo}}docker compose {{main}} {{dev}} {{test}} up backend-unit-testing

test-frontend-components:
  {{sudo}}docker compose {{main}} {{dev}} {{test}} up frontend-components-testing

test-backend-integration:
  {{sudo}}docker compose {{main}} {{dev}} {{test}} up -V backend-integration-testing

test-frontend-scenarios:
  {{sudo}}docker compose {{main}} {{dev}} {{test}} up frontend-scenarios-testing

test-e2e:
  {{sudo}}docker compose {{main}} {{dev}} {{test}} up -V e2e-testing
