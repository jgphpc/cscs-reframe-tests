#!/bin/bash

# if [[ $LOCAL_RANK == 0 ]]; then

    _cn=$SLURM_JOB_NODELIST # needed for _t0
    _t0=$(scontrol show nodes $_cn --json | jq '.nodes[].boot_time.number')
    _t1=$(date +%s)
    diff=$(($_t1 - $_t0))
    _mi=$(rocm_agent_enumerator | sort -u)
    # rocm-smi --showallinfo |grep -m1 MI

    printf '# boot_time %d h %d m / %d / %d / %s / MI=%s \n' \
        $(( diff / 3600 )) \
        $(( diff % 3600 / 60 )) \
        $_t0 \
        $_t1 \
        $_cn \
        $_mi

# fi
