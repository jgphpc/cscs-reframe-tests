#!/bin/bash

partition=$1

scontrol show partition $partition &> /dev/null
if [ $? -ne 0 ] ;then
    echo "# partition=$partition not found"
    scontrol show partition |grep PartitionName=
    return
fi

# partition state:
sinfo -s |egrep "TIMELIMIT|^$partition"

# report nodes state in partition:
# --- list of nodes in partition:
nodelist_a=$(scontrol show partition $partition |grep " Nodes=" |cut -d= -f2)
# --- list of nodes name:
hostlist -e $nodelist_a > .eff.1
# --- list of nodes state:
scontrol show nodes $nodelist_a |grep "State=" |awk '{print $1}' |cut -d= -f2 |awk '{print "@"$0"@"}' > .eff.2
list_of_states=$(sort -u .eff.2)
# list_of_states=$(scontrol show nodes $nodelist_a |grep "State=" |awk '{print $1}' |cut -d= -f2 |sort -u)
paste -d " " .eff.1 .eff.2 > .eff.3

for ss in $list_of_states ;do
    nodelist=`hostlist -c $(grep "$ss" .eff.3 |awk '{print $1}')`
    nnodes=$(hostlist -e $nodelist |wc -l)
    echo "# $ss $nodelist # $nnodes" |tr -d @
done

rm -f .eff.1 .eff.2 .eff.3
