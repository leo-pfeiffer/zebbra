.PHONY: test
# Run the unit tests
test:
	python -m pytest tests

.PHONY: setup_db
# Run the setup db script
setup_db:
	chmod +x scripts/setup_db.sh
	sh scripts/setup_db.sh

.PHONY: setup_db_no_integrations
# Run the setup db script
setup_db_no_integrations:
	chmod +x scripts/setup_db_no_integrations.sh
	sh scripts/setup_db_no_integrations.sh

.PHONY: setup_db_no_source
# Run the setup db script without sourcing. Necessary during GitHub action
setup_db_no_source:
	chmod +x scripts/setup_db.sh
	sh scripts/setup_db.sh "nosource"

.PHONY: run_server
# Start the Zebbra API server
run_server:
	python -m uvicorn main:app --reload

.PHONY: set_secret_env
# Set GitHub secrets from .env file
set_secret_env:
	gh secret set -f .env

.PHONY: help
# Found here: https://stackoverflow.com/a/35730928/12168211
# Print available commands
help:
	@echo "=============================================================="
	@echo "Available Make commands ======================================"
	@echo "=============================================================="
	@awk '/^#/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) | column -s: -t