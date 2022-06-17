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

