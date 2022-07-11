#!/bin/zsh

# This is a test script to authorize the Xero API for user johndoe@example.com
# Run the script while the Zebbra API is running

ACCESS_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lQGV4YW1wbGUuY29tIiwiZXhwIjoxNjU5MzgzNjkxfQ.yNkWCmM-3MGOydV_ysWb0cSeD2wqaJR-vpTOYdRpAlQ"
WORKSPACE="62bc5706a40e85213c27ce29"
URL="http://localhost:8000/integration/xero/login?workspace_id=${WORKSPACE}&access_token=${ACCESS_TOKEN}"

open $URL
