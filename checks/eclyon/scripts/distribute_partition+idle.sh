#!/bin/bash

# https://confluence.cscs.ch/spaces/reframe/pages/917505368/Flexible+Tests
# source checks/eclyon/scripts/distribute_partition+idle.sh haswell && echo nodelist=$nodelist

partition=$1

rc=$(scontrol show nodes --json &> /dev/null; echo $?)    
if [ $rc ] ;then
    json='N'
    # --json not supported
    # scontrol: fatal: serializer_required: could not find plugin for application/json
else
    json='Y'
fi

# get list of IDLE compute nodes from 1 partition
if [ "$json" = "Y" ] ;then
    nodelist_=$(scontrol show partition --json $partition |jq -r .partitions[0].nodes.configured)
    nodelist=$(scontrol show nodes --json $nodelist_ |jq -rc '.nodes[] | select(.state | index("IDLE")) | .hostname' |xargs hostlist -c)
fi

if [ "$json" = "N" ] ;then
    nodelist_=$(scontrol show partition $partition |grep " Nodes=" |cut -d= -f2)
    hostlist -e $nodelist_ > .eff.1
    scontrol show nodes $nodelist_ |grep "State=" |awk '{print $1}' |cut -d= -f2 > .eff.2
    nodelist=$(paste -d " " .eff.1 .eff.2 |grep " IDLE$" |awk '{printf "%s,",$1}' |xargs hostlist -c)
    rm -f .eff.1 .eff.2
fi

nnodes=$(hostlist -e $nodelist |wc -l)
echo "nodelist=$nodelist # $nnodes"
export nodelist=$nodelist

# ./R -c checks/system/slurm/slurm.py -n SlurmParanoidCheck -r --distribute -J w=$nodelist
