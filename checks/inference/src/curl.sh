#!/bin/bash

target="$1"
url="$2"

if [ "$target" = "prod" ] ;then
    key=$CSCS_INFERENCE_API_KEY
elif [ "$target" = "tds" ] ;then
    key=$CSCS_INFERENCE_API_KEY_TDS
else
    echo "Error"
    exit -1
fi

curl -X GET "$url/models" \
    -H "Authorization: Bearer $key" \
    -H "Content-Type: application/json" | \
    jq |grep \"id\": |tr -d , |awk '{print $2": {\"name\": "$2"},"}'
