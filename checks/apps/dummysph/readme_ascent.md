# ASCENT
git clone https://github.com/jfavre/DummySPH DummySPH.git

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
insitu_flags="-DINSITU=Ascent -DAscent_DIR=/user-environment/env/default/lib/cmake"
# insitu_flags="-DINSITU=VTK-m -DVTKm_DIR=`find /user-environment/ -name vtkm-2.2 |grep -m1 cmake`"

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
    ./build+-ON-OFF-ON-OFF/bin/dummysph_ascent \
    --tipsy /capstor/store/cscs/userlab/vampir/hr8799_bol_bd1.017300 --rendering /dev/shm/eff
```

will fail with:

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
# pre-initialization: 6.655e-06s / MemFree = 464716992 / MemAvailable = 551737536 / MemTotal = 895967296 kB
Creating output folder: datasetstime: 0 cycle: 0
Conduit Blueprint check found interleaved coordinates
AscentInitialize
# post-initialization: 1.06878s / MemFree = 463783040 / MemAvailable = 550803584 / MemTotal = 895967296 kB
[Error] Ascent::execute
file: /tmp/jenkssl/spack-stage/spack-stage-ascent-git.4da1379602c44f72d587a1c7efa8856197ae87df_develop-xzeetemryhvvbqkfkcbwkagavgdk5iez/spack-src/src/libs/ascent/runtimes/ascent_main_runtime.cpp
line: 2236
message:
Execution failed with vtkm: Could not find appropriate cast for array in CastAndCall.
Array: valueType=f storageType=N4vtkm4cont16StorageTagStrideE 30766061 values occupying 123064244 bytes [3.91332e-15 3.64001e-13 1.58098e-14 ... 4.06466e-15 1.23443e-14 2.2816e-14]
TypeList: N4vtkm4ListIJfdEEE

(Stack trace unavailable)

# post-exec: 0.900533s / MemFree = 463593344 / MemAvailable = 550640768 / MemTotal = 895967296 kB
AscentFinalize
```

- https://github.com/Alpine-DAV/ascent/issues/1468
