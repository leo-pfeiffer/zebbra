#!/bin/zsh
. .env

cat .env | \
  openssl enc -base64 -e -aes-256-cbc -salt -pass pass:$ENV_ENCRYPT_PASS -md md5 > .env.enc
