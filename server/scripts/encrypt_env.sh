#!/bin/zsh
. .env

openssl enc -aes-256-cbc -e -in ".env"  -out "encrypted_dotenv" -pass pass:$ENV_ENCRYPT_PASS
