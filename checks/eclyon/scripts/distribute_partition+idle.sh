#!/bin/bash

# https://confluence.cscs.ch/spaces/reframe/pages/917505368/Flexible+Tests
# source checks/eclyon/scripts/distribute_partition+idle.sh haswell && echo nodelist=$nodelist

# sinfo -sa
#   PARTITION AVAIL  TIMELIMIT   NODES(A/I/O/T) NODELIST
#   haswell*     up 14-00:00:0      17/28/17/62 haswell-f20-[01-03],haswell-t16-[03-29,31,33-54],haswell-x20-[01-08],haswell-x44-01
#   skylake      up 7-00:00:00        19/1/0/20 skylake-f32-[01-06],skylake-t32-[01-14]
#   cascade      up 7-00:00:00       31/21/0/52 cascade-f32-[01-08],cascade-t32-[01-40],cascade-x32-[01-04]
#   genoa        up 7-00:00:00          8/0/0/8 genoa-t64-[01-08]

# for ii in haswell skylake cascade genoa ;do ./distribute_partition+idle.sh $ii ;done
#  partition=haswell nodelist=haswell-f20-[02-03],haswell-t16-[19,27-29,35-42,44,48,50,52-53],haswell-x20-[01-08],haswell-x44-01 # 28
#  partition=skylake nodelist=skylake-f32-06 # 1
#  partition=cascade nodelist=cascade-f32-[02-04,06,08],cascade-t32-[04,12-13,15-17,22,28,32,35,39-40],cascade-x32-[01-04] # 21
#  partition=genoa no.idle.nodes.found

partition=$1

scontrol show partition $partition &> /dev/null
if [ $? -ne 0 ] ;then
    echo "# partition=$partition not found"
    scontrol show partition |grep PartitionName=
    return
fi

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
        echo "# partition=$partition no.idle.nodes.found"
        # exit 0
    else
        nodelist=$(hostlist -c $nodelist_b)
        nnodes=$(hostlist -e $nodelist |wc -l)
        echo "# partition=$partition nodelist=$nodelist # $nnodes"
        export nodelist=$nodelist
    fi
fi

# if [ "$json" = "Y" ] ;then
#     nodelist_=$(scontrol show partition --json $partition |jq -r .partitions[0].nodes.configured)
#     nodelist=$(scontrol show nodes --json $nodelist_ |jq -rc '.nodes[] | select(.state | index("IDLE")) | .hostname' |xargs hostlist -c)
#     echo "## nodelist=$nodelist"
# fi

# ./R -c checks/system/slurm/slurm.py -n SlurmParanoidCheck -r --distribute -J w=$nodelist
