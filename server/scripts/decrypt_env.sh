#!/bin/zsh

openssl base64 -A -in .env -out .env.enc
