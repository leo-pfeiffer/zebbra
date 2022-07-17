#!/bin/bash
. .env

openssl base64 -A -in .env -out enc.env

gh secret set DOT_ENV --body "$(cat enc.env)"
