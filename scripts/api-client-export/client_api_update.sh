#!/bin/bash

# Move to project root
echo $PWD

# 2. Backup do arquivo "localhost.bru" se existir no folder "api-client" (nível 1, 2 ou 3)
BRU_BACKUP="/tmp/localhost.bru.bak"
rm -f "$BRU_BACKUP"
BRU_FILE=$(find api-client -maxdepth 3 -name "localhost.bru" | head -n 1)
if [ -n "$BRU_FILE" ] && [ -f "$BRU_FILE" ]; then
    cp "$BRU_FILE" "$BRU_BACKUP"
    echo "Backup created: $BRU_BACKUP"
fi

# 1. Altere a parte do "temporary directory"
TEMP_DIR=$(mktemp -d)
echo "Using temporary directory: $TEMP_DIR"
trap 'rm -rf "$TEMP_DIR"; rm -f "$BRU_BACKUP"' EXIT

# Generate openapi.json
EXPORT_DIR="$TEMP_DIR" python3 ./scripts/api-client-export/export_swagger.py

# Import to Bruno in temp directory
npx @usebruno/cli import openapi \
  --source "$TEMP_DIR/openapi.json" \
  --output "$TEMP_DIR" \
  --collection-name "Blood Donation API" \
  --collection-format bru

# Move content to the final folder and remove temp
# This ensures it "increments" (overwrites existing, keeps others) without nesting
# We remove old .yml files if we are migrating to .bru
find ./api-client/blood-donation-api -name "*.yml" -delete
mkdir -p ./api-client/blood-donation-api
cp -r "$TEMP_DIR/Blood Donation API/"* ./api-client/blood-donation-api/

# Copy results from export_swagger.py
cp "$TEMP_DIR/openapi.json" ./api-client/
if [ -d "$TEMP_DIR/blood-donation-api/environments" ]; then
    mkdir -p ./api-client/blood-donation-api/environments
    cp -r "$TEMP_DIR/blood-donation-api/environments/"* ./api-client/blood-donation-api/environments/
fi

echo "Success: API Client exported/updated in ./api-client/blood-donation-api"