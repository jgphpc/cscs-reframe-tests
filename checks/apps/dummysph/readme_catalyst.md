# CATALYST

TODO...........

git clone https://github.com/jfavre/DummySPH DummySPH.git

## UENV

```
uenv image pull service::paraview/5.13.3:1802853997
uenv start -v default paraview/5.13.3:1802853997  # no cuda
```

## BUILD

```
ROOTD=/user-environment/linux-sles15-neoverse_v2/gcc-12.4.0/libcatalyst-2.0.0-2vzaznynvw5guggyeuz74uidbilpxode
export catalyst_DIR=$ROOTD/lib64/cmake/catalyst-2.0
export CATALYST_IMPLEMENTATION_PATHS=$ROOTD/../paraview-git.d9100e04f9558222bbb48852d03035638812549b_master-jzsvsbr3d4exbmb2jper3mhmbjiaf6ha/lib64/catalyst
export CATALYST_DATA_DUMP_DIRECTORY=$PWD

AOS=OFF
DBL=OFF
TIPSY=OFF
H5=ON
/user-environment/linux-sles15-neoverse_v2/gcc-12.4.0/cmake-3.30.5-boxxe6q7f3upqh6bbo4wawwhs7a5c7yr/bin/cmake \
    -DCMAKE_C_COMPILER=mpicc \
    -DCMAKE_CXX_COMPILER=mpicxx \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCAN_DATADUMP=OFF \
    -DSTRIDED_SCALARS=$AOS \
    -DSPH_DOUBLE=$DBL \
    -DCAN_LOAD_TIPSY=$TIPSY \
    -DCAN_LOAD_H5Part=$H5 \
    -S src \
    -B build+catalyst-$AOS-$DBL-$TIPSY-$H5 \
    -DINSITU=Catalyst \
    -Dcatalyst_DIR=$catalyst_DIR \

# -DCMAKE_CUDA_ARCHITECTURES=90 \

cmake --build build+catalyst-$AOS-$DBL-$TIPSY-$H5
```

## RUN

```
export CATALYST_IMPLEMENTATION_NAME=paraview
unset MPICH_GPU_SUPPORT_ENABLED
./build+catalyst-OFF-OFF-OFF-ON/bin/dummysph_catalystV2 \
    --catalyst ./DummySPH.git/ParaView_scripts/catalyst_clipping.py \
    --h5part /capstor/store/cscs/userlab/vampir/dump_wind-shock.h5
```

will give:

```
147dummydata = 0 H5PartFileName = /capstor/store/cscs/userlab/vampir/dump_wind-shock.h5
104 :found valid HDF5 file /capstor/store/cscs/userlab/vampir/dump_wind-shock.h5
116 :found 4037726 particles
124 :found valid HDF5 Step#0
Allocating 9 std::vectors of scalar fields of size 4 bytes
0.90804 < rho < 11.6893
185 finished loading H5Part data
# pre-initialization: 2.9759e-05s / MemFree = 551203648 / MemAvailable = 582822528 / MemTotal = 895967360 kB
CatalystInitialize
# post-initialization: 0.858095s / MemFree = 550733440 / MemAvailable = 582828160 / MemTotal = 895967360 kB
(   1.221s) [pvbatch         ]vtkSMColorMapEditorHelp:706   WARN| Could not determine array range.
(   1.239s) [pvbatch         ]vtkSMColorMapEditorHelp:706   WARN| Could not determine array range.
# post-exec: 1.55144s / MemFree = 549910336 / MemAvailable = 582342464 / MemTotal = 895967360 kB


ls -lh datasets/
drwxr-x---+ 2 piccinal csstaff 4.0K May  6 16:11 dataset_000000
-rw-r-----+ 1 piccinal csstaff  975 May  6 16:11 dataset_000000.vtpd
-rw-r-----+ 1 piccinal csstaff  32K May  6 16:11 RenderView1_000000.png
```

## VERSIONS

```
- paraview@git.d9100e04f9558222bbb48852d03035638812549b=master
pvpython --version # paraview version 5.13.3

unset MPICH_GPU_SUPPORT_ENABLED
pvpython -c "from paraview.simple import GetOpenGLInformation, servermanager;
info = GetOpenGLInformation(servermanager.vtkSMSession.RENDER_SERVER);
print('Vendor:   %s' % info.GetVendor());
print('Version:  %s' % info.GetVersion());
print('Renderer: %s' % info.GetRenderer())"

    Vendor:   NVIDIA Corporation
    Version:  4.6.0 NVIDIA 550.54.15
    Renderer: NVIDIA GH200 120GB/PCIe
```

- https://catalyst-in-situ.readthedocs.io/en/latest/introduction.html
- https://docs.paraview.org/en/latest/Catalyst/index.html
