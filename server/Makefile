.PHONY: test
test:
	python -m pytest tests

.PHONY: setup_db
setup_db:
	chmod +x scripts/setup_db.sh
	sh scripts/setup_db.sh

.PHONY: setup_db_no_source
setup_db_no_source:
	chmod +x scripts/setup_db.sh
	sh scripts/setup_db.sh "nosource"

.PHONY: run_server
run_server:
	python -m uvicorn main:app --reload

.PHONY: set_secret_env
set_secret_env:
	gh secret set -f .env
