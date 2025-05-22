#!/bin/bash

# us insitu_ascent/develop:1825576142 -v default # +cuda
# us insitu_ascent_nocuda/develop-gcc12:1827699279@daint -v default # ~cuda

export CMAKE_PREFIX_PATH=`find /user-environment/ -name cmake |grep hdf5 |grep -v spack`:$CMAKE_PREFIX_PATH
export CPATH=/user-environment/env/default/include
# insitu_flags="-DINSITU=Ascent -DAscent_DIR=/user-environment/env/default/lib/cmake"  # = JG
insitu_flags="-DINSITU=Ascent -DAscent_DIR=/capstor/scratch/cscs/jfavre/Ascent-cuda/install/ascent-checkout/lib/cmake/ascent"  # = JF = prgenv-gnu/24.11:v2

INSITU=Ascent
AOS=$1
DBL=$2
TIPSY=$3
H5=$4

if [ -z "$5" ] ;then
/user-environment/env/default/bin/cmake \
    -DCMAKE_C_COMPILER=mpicc \
    -DCMAKE_CXX_COMPILER=mpicxx \
    -DCMAKE_CUDA_ARCHITECTURES=90 \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCAN_DATADUMP=OFF \
    -DSTRIDED_SCALARS=$AOS \
    -DSPH_DOUBLE=$DBL \
    -DCAN_LOAD_TIPSY=$TIPSY \
    -DCAN_LOAD_H5Part=$H5 \
    -S DummySPH.git/src \
    -B build+$INSITU-$AOS-$DBL-$TIPSY-$H5 \
    $insitu_flags

cmake --build build+$INSITU-$AOS-$DBL-$TIPSY-$H5

else

mkdir -p /dev/shm/piccinal
rm -fr *.yaml datasets core*
# cp DummySPH.git/Ascent_yaml/tipsy_actions.yaml simple_trigger_actions.yaml

EXE=./build+$INSITU-$AOS-$DBL-$TIPSY-$H5/bin/dummysph_ascent
# EXE="./ddt-client ./build+$INSITU-$AOS-$DBL-$TIPSY-$H5/bin/dummysph_ascent"
echo EXE=$EXE

if [ $TIPSY = "ON" ]; then flags="--tipsy /capstor/store/cscs/userlab/vampir/hr8799_bol_bd1.017300" ;fi
if [ $H5 = "ON" ]; then    flags="--h5part /capstor/store/cscs/userlab/vampir/dump_wind-shock.h5" ;fi

#cat << EOF
CUDA_VISIBLE_DEVICES=$5 \
    $EXE $flags \
    $6 $7 $8
#EOF
echo done

# see results in readme.sh

fi
