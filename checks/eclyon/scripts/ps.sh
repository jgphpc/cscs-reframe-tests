#!/bin/bash
#ok ps -o pid=,psr= -p $$
#ok ps -o pid=,psr=,comm= -p $$

pid=$$
psr=$(ps -o psr= -p $pid)
hname=$(hostname)

# retrieve the CPU affinity mask in hexadecimal format
## affinity_mask=$(taskset -p $pid | awk -F': ' '{print $2}')

# get numerical list (decimal) of numa nodes and cores in the affinity mask
## numa_list=$(hwloc-calc --physical --intersect NUMAnode 0x$affinity_mask)
## cpu_list=$(hwloc-calc --physical --intersect core 0x$affinity_mask)
cpu_list_short=$(taskset -pc $pid | awk -F': ' '{print $2}')

if [ $SLURM_NODEID = 0 ] ;then
    if [ $SLURM_LOCALID = 0 ] ;then
        lscpu |grep ^NUMA
    fi
fi
echo "host=$hname pid=$pid (core $psr) clist=$cpu_list_short Snid=$SLURM_NODEID Spid=$SLURM_PROCID Sid=$SLURM_LOCALID"

# echo $hname $pid $psr $affinity_mask $cpu_list_short 
