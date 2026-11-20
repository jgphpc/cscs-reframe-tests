#!/bin/bash

tar zcf ~/eff.tar \
    nid0025{18,20}/latest.json \
    nid0025{18,20}/stage/beverin/mi300/prgenv-gnu_7_2_3_v1_default/CoralGemm_*/gpumon.sh.rpt \
    nid0025{18,20}/stage/beverin/mi300/prgenv-gnu_7_2_3_v1_default/CoralGemm_*/gpumon_*/telemetry.csv
