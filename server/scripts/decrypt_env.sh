#!/bin/zsh
source .env

openssl enc -aes-256-cbc -d -in "encrypted_dotenv"  -out ".env" -pass pass:$ENV_ENCRYPT_PASS
