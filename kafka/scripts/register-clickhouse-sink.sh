#!/bin/sh

set -euo pipefail

for table in animals trackers events; do
    echo "Registering CDC sink for table: $table"

    sed "s/__TABLE__/$table/g;" /kafka/clickhouse-sink.template.json > /tmp/clickhouse-sink-$table.json

    response=$(curl -s -o /tmp/response.txt -w "%{http_code}" \
      -X POST -H "Content-Type: application/json" \
      --data @/tmp/clickhouse-sink-$table.json \
      http://debezium:8083/connectors)

    echo "Response code: $response"

    case "$response" in
        201)
            echo "✅ Connector for $table registered successfully"
            ;;
        409)
            echo "⚠️ Connector for $table already exists"
            ;;
        400)
            echo "❌ Bad request for $table (HTTP $response)"
            echo "Response:"
            cat /tmp/response.txt
            exit 1
            ;;
        *)
            echo "❌ Failed to register connector for $table (HTTP $response)"
            echo "Response:"
            cat /tmp/response.txt
            exit 1
            ;;
    esac

    echo "---------------------------------------------"

done
