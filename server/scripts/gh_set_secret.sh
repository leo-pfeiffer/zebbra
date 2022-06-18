#!/bin/zsh
source .env

echo "$ENV_ENCRYPT_PASS"

gh secret set ENV_ENCRYPT_PASS --body "$ENV_ENCRYPT_PASS"
