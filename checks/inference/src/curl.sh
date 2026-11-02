#!/bin/bash

url="$1"

curl -X GET "$url/models" \
    -H "Authorization: Bearer $CSCS_INFERENCE_API_KEY" \
    -H "Content-Type: application/json" | \
    jq |grep \"id\": |tr -d , |awk '{print $2": {\"name\": "$2"},"}'
