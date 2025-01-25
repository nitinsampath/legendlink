.PHONY: migration migrate up down logs psql records

# Default migration message
MSG ?= "New migration"
QUERY ?= "SELECT * FROM financial_records;"

# Create a new migration
migration:
	docker compose run --rm backend alembic revision --autogenerate -m "$(MSG)"

# Apply migrations
migrate:
	docker compose run --rm backend alembic upgrade head

# Start all services
up:
	docker compose up -d

# Stop all services
down:
	docker compose down

# View logs
logs:
	docker compose logs -f

# Connect to database
psql:
	docker compose exec db psql -U postgres -d legendlink

# View all records
query:
	docker compose exec db psql -U postgres -d legendlink -c '$(QUERY)'