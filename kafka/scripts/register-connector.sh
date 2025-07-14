#!/bin/sh
set -euo pipefail
apk add --no-cache curl gettext

envsubst < /kafka/kafka-connector-template.json > /tmp/connector.json

echo "Registering Debezium connector with the following configuration:"
cat /tmp/connector.json

response=$(curl -s -o /tmp/response.txt -w "%{http_code}" \
  -X POST -H "Content-Type: application/json" \
  --data @/tmp/connector.json \
  http://debezium:8083/connectors)

if [ "$response" = "201" ]; then
  echo "✅ Connector registered successfully"
elif [ "$response" = "409" ]; then
  echo "⚠️ Connector already exists"
else
  echo "❌ Failed to register connector (HTTP $response)"
  echo "Response:"
  cat /tmp/response.txt
  exit 1
fi
