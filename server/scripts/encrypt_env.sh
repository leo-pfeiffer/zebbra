#!/bin/zsh
. .env

cat .env | \
  openssl enc -base64 -e -aes-256-cbc -nosalt -pass pass:$ENV_ENCRYPT_PASS > .env.enc
