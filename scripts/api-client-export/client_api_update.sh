#!/bin/bash

# Move to project root
echo $PWD

# Generate openapi.json
python3 ./scripts/api-client-export/export_swagger.py

# Create a temporary directory for import
TEMP_DIR="api-client/temp_import"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# Import to Bruno in temp directory
npx @usebruno/cli import openapi \
  --source ./api-client/openapi.json \
  --output "$TEMP_DIR" \
  --collection-name "Blood Donation API" \
  --collection-format bru

# Move content to the final folder and remove temp
# This ensures it "increments" (overwrites existing, keeps others) without nesting
# We remove old .yml files if we are migrating to .bru
find ./api-client/blood-donation-api -name "*.yml" -delete
mkdir -p ./api-client/blood-donation-api
cp -r "$TEMP_DIR/Blood Donation API/"* ./api-client/blood-donation-api/
rm -rf "$TEMP_DIR"

echo "Success: API Client exported/updated in ./api-client/blood-donation-api"