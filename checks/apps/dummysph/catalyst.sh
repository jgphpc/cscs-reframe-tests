#!/bin/bash

# us insitu_ascent/develop-gcc12:1827486263@daint -v default

ROOTD=/user-environment/linux-sles15-neoverse_v2/gcc-12.4.0/libcatalyst-2.0.0-bexhygrrm2fdm5ujkqziygkl5warsxs6
export catalyst_DIR=$ROOTD/lib64/cmake/catalyst-2.0
export CATALYST_IMPLEMENTATION_PATHS=$ROOTD/../paraview-git.d9100e04f9558222bbb48852d03035638812549b_master-35bobmbge36ydcndzhbzlzqbptsn6iwz/lib64/catalyst
export CATALYST_DATA_DUMP_DIRECTORY=$PWD
export CMAKE_PREFIX_PATH=`find /user-environment/ -name cmake |grep hdf5 |grep -v spack`:$CMAKE_PREFIX_PATH
export CPATH=/user-environment/env/default/include
insitu_flags="-DINSITU=Catalyst -Dcatalyst_DIR=$ROOTD/lib64/cmake/catalyst-2.0"
# /capstor/scratch/cscs/piccinal/santis/jf/dummysph/

INSITU=Catalyst
AOS=$1      # OFF
DBL=$2      # OFF
TIPSY=$3    # OFF
H5=$4       # ON

if [ "$5" = "b" ] ;then
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
export CATALYST_IMPLEMENTATION_NAME=paraview
unset MPICH_GPU_SUPPORT_ENABLED

EXE=./build+$INSITU-$AOS-$DBL-$TIPSY-$H5/bin/dummysph_catalystV2

echo EXE=$EXE
# for ii in --rendering --compositing --thresholding --histsampling --dumping --binning ;do
if [ $TIPSY = "ON" ]; then flags="--tipsy /capstor/store/cscs/userlab/vampir/hr8799_bol_bd1.017300" ;fi
if [ $H5 = "ON" ]; then     flags="--h5part /capstor/store/cscs/userlab/vampir/dump_wind-shock.h5" ;fi

#cat << EOF
CUDA_VISIBLE_DEVICES=$5 \
    $EXE $flags \
    --catalyst ./DummySPH.git/ParaView_scripts/catalyst_clipping.py \
    $6 $7 $8
#EOF
echo done
fi
