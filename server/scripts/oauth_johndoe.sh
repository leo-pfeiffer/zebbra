#!/bin/zsh

# Usage:
# sh oauth_johndoe.sh <INTEGRATION_NAME>

# This is a test script to authorize an API for user johndoe@example.com
# Run the script while the Zebbra API is running

INTEGRATION="$1"
ACCESS_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lQGV4YW1wbGUuY29tIiwiZXhwIjoxNjU5MzgzNjkxfQ.yNkWCmM-3MGOydV_ysWb0cSeD2wqaJR-vpTOYdRpAlQ"
WORKSPACE="62bc5706a40e85213c27ce29"
URL="http://localhost:8000/integration/$INTEGRATION/login?workspace_id=${WORKSPACE}&access_token=${ACCESS_TOKEN}"

echo $URL
open $URL
