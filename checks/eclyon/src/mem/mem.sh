#!/bin/bash
host=$(hostname)
mem1=$(head -n1 /proc/meminfo |tr -d " ")
mem2=$(grep MemAvailable: /proc/meminfo |tr -d " ")
scn=$(scontrol show nodes $host |grep RealMemory= |awk '{print $1,$2,$3}')

echo "$host / $mem1 / $mem2 / $scn / $1"
