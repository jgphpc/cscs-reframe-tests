#!/bin/bash

partition=$1

scontrol show partition $partition &> /dev/null
if [ $? -ne 0 ] ;then
    echo "# partition=$partition not found"
    scontrol show partition |grep PartitionName=
    return
fi

# partition state:
# sinfo -s |egrep "TIMELIMIT|^$partition" |awk '{print "#",$0}'
sinfo |egrep "TIMELIMIT|^$partition" |awk '{print "#",$0}'

# part=haswell;mode=all; 
# sinfo |egrep "TIMELIMIT|^$part" |awk '{print "#",$0}' 
# ./R -c checks/system/slurm/slurm.py -n SlurmParanoidCheck --system newton:$part-all --dry-run --distribute=$mode &> eff 
# grep DRY eff |awk -F nid= '{print $2}' |awk '{print $1}' |sort |uniq -c |wc -l


#ok # report nodes state in partition:
#ok # --- list of nodes in partition:
#ok nodelist_a=$(scontrol show partition $partition |grep " Nodes=" |cut -d= -f2)
#ok # --- list of nodes name:
#ok hostlist -e $nodelist_a > .eff.1
#ok # --- list of nodes state:
#ok scontrol show nodes $nodelist_a |grep "State=" |awk '{print $1}' |cut -d= -f2 |awk '{print "@"$0"@"}' > .eff.2
#ok list_of_states=$(sort -u .eff.2)
#ok # list_of_states=$(scontrol show nodes $nodelist_a |grep "State=" |awk '{print $1}' |cut -d= -f2 |sort -u)
#ok paste -d " " .eff.1 .eff.2 > .eff.3
#ok 
#ok for ss in $list_of_states ;do
#ok     nodelist=`hostlist -c $(grep "$ss" .eff.3 |awk '{print $1}')`
#ok     nnodes=$(hostlist -e $nodelist |wc -l)
#ok     echo "# $ss $nodelist # $nnodes" |tr -d @
#ok done
#ok 
#ok rm -f .eff.1 .eff.2 .eff.3
