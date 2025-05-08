# VTKm

- git clone https://github.com/jfavre/DummySPH DummySPH.git

## UENV

```
uenv image pull service::insitu_ascent/develop_gcc13:1802669257  # DAINT
uenv start -v default insitu_ascent/develop_gcc13:1802669257
```
# cd /capstor/scratch/cscs/piccinal/santis/jf/tests/JG2/

## BUILD

```
export CMAKE_PREFIX_PATH=`find /user-environment/ -name cmake |grep hdf5 |grep -v spack`:$CMAKE_PREFIX_PATH
export CPATH=/user-environment/env/default/include
insitu_flags="-DINSITU=VTK-m -DVTKm_DIR=`find /user-environment/ -name vtkm-2.2 |grep -m1 cmake`"

INSITU=VTK-m
AOS=ON
DBL=OFF
TIPSY=ON
H5=OFF
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
```

## RUN

```
rm -fr /dev/shm/piccinal/* *.yaml datasets
CUDA_VISIBLE_DEVICES=1 \
    ./build+VTK-m-ON-OFF-ON-OFF/bin/dummysph_vtkm \
    --tipsy /capstor/store/cscs/userlab/vampir/hr8799_bol_bd1.017300 --rendering /dev/shm/eff
```

will `pass` with:

```
147dummydata = 0 H5PartFileName =
CPU 0 allocating 30766061 SPH  particles of size 48 = 1442159 Kbytes
421: TipsyFile: read file /capstor/store/cscs/userlab/vampir/hr8799_bol_bd1.017300
time   : 17301
nbodies: 30766063
nsph   : 30766061
ndark  : 0
nstar  : 2
swapped endian: 1
free(sph)...
TipsyReader: releasing all resources
# pre-initialization: 5.0462e-05s / MemFree = 455233792 / MemAvailable = 550483456 / MemTotal = 895967296 kB
VTK-m::Initialize
forcing DeviceAdapterTagCuda
creating fields with strided access
copying single block data to device
VTK-mInitialize
# post-initialization: 0.884177s / MemFree = 452081728 / MemAvailable = 547331264 / MemTotal = 895967296 kB
written image to disk: /dev/shm/eff.00.0001.png
# post-exec: 0.312716s / MemFree = 451275456 / MemAvailable = 546547904 / MemTotal = 895967296 kB
VTK-mFinalize
Shutting down VTK-m at end of processing

--> /dev/shm/eff.00.0001.png
```
