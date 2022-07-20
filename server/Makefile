.PHONY: test
# Run the unit tests
test:
	python -m pytest tests

.PHONY: requirements
# Install requirements with pip
requirements:
	pip install --upgrade pip
	pip install -r requirements.txt

.PHONY: setup_db
# Run the setup db script
setup_db:
	chmod +x scripts/setup_db.sh
	scripts/setup_db.sh

.PHONY: setup_db_no_integrations
# Run the setup db script
setup_db_no_integrations:
	chmod +x scripts/setup_db_no_integrations.sh
	scripts/setup_db_no_integrations.sh

.PHONY: run_server
# Start the Zebbra API server
run_server:
	python -m uvicorn main:app --reload

.PHONY: run_server_prod
# Start the Zebbra API server in production
run_server_prod:
	python -m uvicorn main:app --reload --port 80 --host 0.0.0.0

.PHONY: gh_set_secret
# Set GitHub secrets from .env file
gh_set_secret:
	gh secret set -f .env

.PHONY: generate_from_template
# Generate integration files from templates. Args: INTEGRATION=<integration_name> API_TYPE=<payroll | accounting>
generate_from_template:
	chmod +x scripts/generate.sh
	scripts/generate.sh $(INTEGRATION) $(API_TYPE)

.PHONY: help
# Found here: https://stackoverflow.com/a/35730928/12168211
# Print available commands
help:
	@echo "=============================================================="
	@echo "Available Make commands ======================================"
	@echo "=============================================================="
	@awk '/^#/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) | column -s: -t