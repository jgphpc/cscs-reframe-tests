#!/bin/bash

# us insitu_ascent/develop:1825576142 -v default

export CMAKE_PREFIX_PATH=`find /user-environment/ -name cmake |grep hdf5 |grep -v spack`:$CMAKE_PREFIX_PATH
export CPATH=/user-environment/env/default/include
#JG insitu_flags="-DINSITU=VTK-m -DVTKm_DIR=`find /user-environment/ -name vtkm-2.2 |grep -m1 cmake`"
# ln -s Driver.cxx Driver.cu
JF=/capstor/scratch/cscs/jfavre/Ascent-cuda/install/vtk-m-v2.3.0
export CMAKE_PREFIX_PATH=$JF/lib/cmake/vtkm-2.3:$CMAKE_PREFIX_PATH
insitu_flags="-DINSITU=VTK-m -DVTKm_DIR=$JF/lib/cmake/vtkm-2.3 -DCMAKE_CUDA_HOST_COMPILER=/user-environment/env/default/bin/mpicxx"
# = JF us prgenv-gnu/24.11:v2 -v default

INSITU=VTK-m
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

# SPHEXA:
#export SPACK_SYSTEM_CONFIG_PATH="/user-environment/config"
#cmake -S .. -DBUILD_ANALYTICAL=OFF -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release \
#-DCSTONE_WITH_HIP=OFF -DRYOANJI_WITH_HIP=OFF -DSPH_EXA_WITH_H5PART=ON \
#-DSPH_EXA_WITH_HIP=OFF -DCMAKE_CUDA_ARCHITECTURES=90 \
#-DCMAKE_CUDA_HOST_COMPILER=/user-environment/env/default/bin/mpicc \
#-DCMAKE_C_COMPILER=mpicc -DCMAKE_CXX_COMPILER=mpicxx

cmake --build build+$INSITU-$AOS-$DBL-$TIPSY-$H5

else

export OMP_NUM_THREADS=16
# /user-environment/linux-sles15-neoverse_v2/gcc-12.4.0/hdf5-1.8.23-vz4wohxzrouobq42d32qs4isocztoo63/bin/h5dump -H /capstor/store/cscs/userlab/vampir/dump_wind-shock.h5
mkdir -p /dev/shm/piccinal
rm -fr *.yaml datasets core*
# cp DummySPH.git/Ascent_yaml/tipsy_actions.yaml simple_trigger_actions.yaml

EXE=./build+$INSITU-$AOS-$DBL-$TIPSY-$H5/bin/dummysph_vtkm
# EXE="./ddt-client ./build+$INSITU-$AOS-$DBL-$TIPSY-$H5/bin/dummysph_vtkm"
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
