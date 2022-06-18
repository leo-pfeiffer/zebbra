#!/bin/zsh

cat .env.enc | \
  openssl enc -base64 -d -aes-256-cbc -nosalt -pass pass:$ENV_ENCRYPT_PASS > .env
