#!/bin/bash

# wget https://github.com/jqlang/jq/releases/download/jq-1.8.1/jq-linux-amd64

in=$1  # latest.json

jq -r '.runs[].testcases[] | [
    .intervalles,
    (.perfvalues | to_entries[] | select(.key | test("^.*:.*:sim_error$")) | .value[0]),
    (.perfvalues | to_entries[] | select(.key | test("^.*:.*:sim_elapsed$")) | .value[0]),
    .partition, .environ
    ] | @csv ' $in |tr , " " > error.txt

