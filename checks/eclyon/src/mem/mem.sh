#!/bin/bash
host=$(hostname)
mem=$(head -n1 /proc/meminfo |tr -d " ")
scn=$(scontrol show nodes $host |grep RealMemory= |awk '{print $1,$2,$3}')

echo "$host / $mem / $scn / $1"
