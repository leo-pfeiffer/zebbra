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

.PHONY: encrypt_env
encrypt_env:
	chmod +x scripts/encrypt_env.sh
	sh scripts/encrypt_env.sh

.PHONY: decrypt_env
decrypt_env:
	chmod +x scripts/decrypt_env.sh
	sh scripts/decrypt_env.sh

.PHONY: gh_secret_passphrase
gh_secret_passphrase:
	chmod +x scripts/gh_set_secret.sh
	sh scripts/gh_set_secret.sh
