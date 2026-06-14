#!/bin/bash

# ./checks/eclyon/scripts/bencher.sh $XX 'bencher=pilatus=login=builtin.json' 'bencher=pilatus=login=builtin=reference.json'
# -> https://bencher.dev/perf/jgproject

# token=$1
jsonfile1=$1
jsonfile2=$2

if [ -z $BENCHER_API_TOKEN ] ;then
    echo "export BENCHER_API_TOKEN=..."
    exit 0
    # --token $BENCHER_API_TOKEN \
fi

branch='newton'
syst_name=$(echo "$jsonfile1" |cut -d= -f2)
part_name=$(echo "$jsonfile1" |cut -d= -f3)
prog_name=$(echo "$jsonfile1" |cut -d= -f4 |cut -d \. -f1)

# measured perf. values
~/bencher-v0.6.6-linux-x86-64 run \
    --adapter json \
    --project "ecl-newton" \
    --thresholds-reset \
    --branch $branch \
    --testbed "$syst_name=$part_name=$prog_name=" \
    --file $jsonfile1

# # reference perf. values
# ./bencher run --adapter json --token $token --project jgproject --thresholds-reset \
# --branch $branch \
# --testbed "$syst_name=$part_name=$prog_name=reference" \
# --file $jsonfile2
