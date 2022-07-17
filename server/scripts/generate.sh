#!/bin/bash

integration=$1

# check if provided name matches format
regex="^[A-Za-z0-9]+$"
if echo "$integration" | grep -Eq  "$regex"
  then
    echo "Generating files for integration ${integration}"
  else
    echo "Invalid integration name"
    exit
fi

lower_case_name=$(echo "$integration" | awk '{print tolower($0)}')

# OAuth
template_integration_oauth="resources/templates/_integration_oauth.py"
new_file_integration_oauth="core/integrations/oauth/${lower_case_name}_oauth.py"

# Adapter
template_adapter="resources/templates/_adapter.py"
new_file_adapter="core/integrations/adapters/${lower_case_name}_adapter.py"

# replace the placeholder and create the new file
generate_from_template () {
  template="$1"
  new_file="$2"
  name="$3"
  pattern='XxXxX'
  sed "s/${pattern}/${name}/g" ${template} > "$new_file"
  echo "Created file: ${new_file}"
}

# run generator
generate_from_template "$template_integration_oauth" "$new_file_integration_oauth" "$1"
generate_from_template "$template_adapter" "$new_file_adapter" "$1"
