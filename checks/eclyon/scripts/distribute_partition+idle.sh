#!/bin/bash

# https://confluence.cscs.ch/spaces/reframe/pages/917505368/Flexible+Tests

partition=$1

rc=$(scontrol show nodes --json &> /dev/null; echo $?)    
if [ $rc ] ;then
    json='Y'
else
    # --json not supported
    # scontrol: fatal: serializer_required: could not find plugin for application/json
    json='N'
fi

# exit 0

# get list of IDLE compute nodes from 1 partition
if [ "$json" = "Y" ] ;then
    nodelist_=$(scontrol show partition --json $partition |jq -r .partitions[0].nodes.configured)

    hostlist -e $nodelist_ > .eff.1
    scontrol show nodes $nodelist_ |grep "State=" |awk '{print $1}' |cut -d= -f2 > .eff.2
    nodelist=$(paste .eff.1 .eff.2 |grep IDLE |awk '{printf "%s,",$1}' |xargs hostlist -c)
    rm -f .eff.1 .eff.2

    nnodes=$(hostlist -e $nodelist |wc -l)
fi

if [ "$json" = "N" ] ;then
    nodelist_=$(scontrol show partition $partition |grep " Nodes=" |cut -d= -f2)

fi

echo "nodelist=$nodelist # $nnodes"

# ./R -c checks/system/slurm/slurm.py -n SlurmParanoidCheck -r --distribute -J w=$nodelist

exit 0
