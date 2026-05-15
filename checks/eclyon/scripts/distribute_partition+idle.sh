#!/bin/bash

# https://confluence.cscs.ch/spaces/reframe/pages/917505368/Flexible+Tests
# source checks/eclyon/scripts/distribute_partition+idle.sh haswell && echo nodelist=$nodelist

partition=$1

# same with --json
# rc=$(scontrol show nodes --json &> /dev/null; echo $?)    
# if [ $rc ] ;then
#     json='N'
#     # --json not supported
#     # scontrol: fatal: serializer_required: could not find plugin for application/json
# else
#     json='Y'
# fi
json='N'

# get list of IDLE compute nodes from 1 partition
if [ "$json" = "N" ] ;then
    nodelist_a=$(scontrol show partition $partition |grep " Nodes=" |cut -d= -f2)
    hostlist -e $nodelist_a > .eff.1
    scontrol show nodes $nodelist_a |grep "State=" |awk '{print $1}' |cut -d= -f2 > .eff.2
    nodelist_b=$(paste -d " " .eff.1 .eff.2 |grep " IDLE$" |awk '{printf "%s,",$1}')
    rm -f .eff.1 .eff.2
    if [ -z $nodelist_b ] ;then
        echo "no.idle.nodes.found"
        # exit 0
    else
        nodelist=$(hostlist -c $nodelist_b)
        nnodes=$(hostlist -e $nodelist |wc -l)
        echo "nodelist=$nodelist # $nnodes"
        export nodelist=$nodelist
    fi
fi

# if [ "$json" = "Y" ] ;then
#     nodelist_=$(scontrol show partition --json $partition |jq -r .partitions[0].nodes.configured)
#     nodelist=$(scontrol show nodes --json $nodelist_ |jq -rc '.nodes[] | select(.state | index("IDLE")) | .hostname' |xargs hostlist -c)
#     echo "## nodelist=$nodelist"
# fi

# ./R -c checks/system/slurm/slurm.py -n SlurmParanoidCheck -r --distribute -J w=$nodelist
