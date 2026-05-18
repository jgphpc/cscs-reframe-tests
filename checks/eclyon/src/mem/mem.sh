#!/bin/bash
arg=$1
host=$(hostname)
mem_avail=$(grep MemAvailable: /proc/meminfo |tr -d " ")
echo "$host / $mem_avail / $arg"

# mem_total=$(head -n1 /proc/meminfo |tr -d " ")
# scn=$(scontrol show nodes $host |grep RealMemory= |awk '{print $1,$2,$3}')
# echo "$host / $mem_avail / $mem2 / $scn / $1"
