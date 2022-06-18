.PHONY: test
test:
	python -m pytest tests

.PHONY: setup_db
setup_db:
	chmod +x scripts/setup_db.sh
	sh scripts/setup_db.sh

.PHONY: run_server
run_server:
	python -m uvicorn main:app --reload

.PHONY: set_secret_env
set_secret_env:
	chmod +x scripts/gh_set_secret.sh
	sh scripts/gh_set_secret.sh
