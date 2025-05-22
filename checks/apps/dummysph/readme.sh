#!/bin/bash

# RULES:
# TIPSY & H5P   = NO
# AOS   & H5P   = NO
# SOA   & TIPSY = NO
# DBL   & TIPSY = NO

LATEST = insitu_ascent/develop:1827451634

#{{{ AOS ON ~PKDGRAV
#{{{ ASCENT
#{{{ insitu_ascent_nocuda/develop-gcc12:1827699279@daint
# * = eff instead of /dev/shm/piccinal/eff
                                                                                                  #varname
#EXE     INSITU   AOS  DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping /dev/shm/piccinal/eff
DummySPH ASCENT    ON  ON   ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A           #DBL&TIPSY
DummySPH ASCENT    ON  OFF  ON OFF yes    CastAndCall OK*            vxvyvz/OK?    CastAndCall    rho/OK    OK
DummySPH ASCENT    ON  ON  OFF  ON N/A    N/A         N/A            N/A           N/A            N/A       N/A           #AOS&H5
DummySPH ASCENT    ON  OFF OFF  ON N/A    N/A         N/A            N/A           N/A            N/A       N/A           #AOS&H5
#}}}
#{{{ insitu_ascent/develop:1825576142 -v default
                                                                                                 #varname
#EXE     INSITU  AOS  DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping
DummySPH ASCENT   ON  ON   ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A      #DBL&TIPSY
DummySPH ASCENT   ON  OFF  ON OFF yes    KO          hangs?         blueprint?    CastAndCall?   KO        OK
DummySPH ASCENT   ON  ON  OFF  ON N/A    N/A         N/A            N/A           N/A            N/A       N/A      #AOS&H5
DummySPH ASCENT   ON  OFF OFF  ON N/A    N/A         N/A            N/A           N/A            N/A       N/A      #AOS&H5
#}}}
#{{{ /capstor/scratch/cscs/jfavre/Ascent-cuda/install/ascent-checkout + prgenv-gnu/24.11:v2
                                                                                               #varname:rho
#EXE     INSITU AOS DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping
DummySPH ASCENT  ON ON   ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A      #DBL&TIPSY
DummySPH ASCENT  ON OFF  ON OFF OK     CORE        OKslow         CORE?         CORE           CORE      OK
DummySPH ASCENT  ON ON  OFF  ON N/A    N/A         N/A            N/A           N/A            N/A       N/A      #AOS&H5
DummySPH ASCENT  ON OFF OFF  ON N/A    N/A         N/A            N/A           N/A            N/A       N/A      #AOS&H5
#}}}
#}}}
#{{{ VTK-m /users/piccinal/cscs-reframe-tests.git/checks/apps/dummysph/vtkm.sh
# ./vtkm.sh OFF ON OFF ON b
# ./vtkm.sh OFF ON OFF ON 0 --rendering /dev/shm/piccinal/r
#{{{ OLD insitu_ascent/develop:1825576142 -v default
                                                                                                #varname
#EXE     INSITU  AOS DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping
DummySPH VTKm    ON  ON   ON OFF yes    N/A         N/A            N/A           N/A            N/A       N/A           #DBL&TIPSY
DummySPH VTKm    ON  OFF  ON OFF yes    OK          OK             issues/7      OK             N/A       OK            
DummySPH VTKm    ON  ON  OFF  ON N/A    N/A         N/A            N/A           N/A            N/A       N/A           #AOS&H5
DummySPH VTKm    ON  OFF OFF  ON N/A    N/A         N/A            N/A           N/A            N/A       N/A           #AOS&H5
#}}}
#{{{ insitu_ascent/develop:1827451634 -v default
                                                                                                #varname
#EXE     INSITU  AOS DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping
DummySPH VTKm    ON  ON   ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A      #DBL&TIPSY
DummySPH VTKm    ON  OFF  ON OFF yes    OK          OK             issues/7      OK             issues/8  KO
DummySPH VTKm    ON  ON  OFF  ON N/A    N/A         N/A            N/A           N/A            N/A       N/A      #AOS&H5
DummySPH VTKm    ON  OFF OFF  ON N/A    N/A         N/A            N/A           N/A            N/A       N/A      #AOS&H5
#}}}
#{{{ /capstor/scratch/cscs/jfavre/Ascent-cuda/install/vtk-m-v2.3.0/ + prgenv-gnu/24.11:v2
                                                                                               #varname
#EXE     INSITU AOS DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping
DummySPH VTKm   ON ON   ON OFF  N/A    N/A         N/A            N/A           N/A            N/A       N/A      #DBL&TIPSY
DummySPH VTKm   ON OFF  ON OFF  OK     OK          OK             CORE          OK             N/A       CORE
DummySPH VTKm   ON ON  OFF  ON  N/A    N/A         N/A            N/A           N/A            N/A       N/A      #AOS&H5
DummySPH VTKm   ON OFF OFF  ON  N/A    N/A         N/A            N/A           N/A            N/A       N/A      #AOS&H5
#}}}
#}}}
#}}}
# ---------------------
#{{{ AOS OFF ~SPHEXA
#{{{ ASCENT
# Usage:
# ./ascent.sh OFF ON OFF ON b
# ./ascent.sh OFF ON OFF ON 0 --rendering /dev/shm/piccinal/r
#{{{ insitu_ascent_nocuda/develop-gcc12:1827699279@daint -v default 
                                                                                                #varname
#EXE     INSITU  AOS DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping
DummySPH ASCENT  OFF ON   ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A           #SOA&TIPSY
DummySPH ASCENT  OFF OFF  ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A           #SOA&TIPSY
DummySPH ASCENT  OFF ON  OFF  ON OK     OK*         OK*            vxvyvz:OK?    OK*            rho:OK    OK
DummySPH ASCENT  OFF OFF OFF  ON OK     OK*         OK             vxvyvz:OK?    Cast_failed    rho:OK    OK

#}}}
#{{{ insitu_ascent/develop:1825576142 -v default 
                                                                                                #varname
#EXE     INSITU  AOS DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping
DummySPH ASCENT  OFF ON   ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A           #SOA&TIPSY
DummySPH ASCENT  OFF OFF  ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A           #SOA&TIPSY
DummySPH ASCENT  OFF ON  OFF  ON KO
DummySPH ASCENT  OFF OFF OFF  ON KO

SPHEXA   ASCENT
#}}}
#{{{ /capstor/scratch/cscs/jfavre/Ascent-cuda/install/ascent-checkout/lib/cmake/ascent/ + prgenv-gnu/24.11:v2
                                                                                                #varname
#EXE     INSITU  AOS DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping
DummySPH ASCENT  OFF ON   ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A      #SOA&TIPSY
DummySPH ASCENT  OFF OFF  ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A      #SOA&TIPSY
DummySPH ASCENT  OFF ON  OFF  ON OK     OK          CORE           CORE          CORE           OK        CORE
DummySPH ASCENT  OFF OFF OFF  ON OK     OK          CORE           CORE          CORE           OK        CORE
SPHEXA   ASCENT                                     #WINDSHOCK                   #WINDSHOCK
                                                    #ifdef CLIPS                 #ifdef HISTSAMPLING
#SPHEXA   ASCENT  windshock ~= dummysph~strided+cuda
{{{CORE --dumping:
Threads,Function
1,main (Driver.cxx:188)
1,  viz::execute<float> (insitu_viz.h:115)
1,    AscentAdaptor::Execute<float> (AscentAdaptor.h:334)
1,      ascent::Ascent::execute(conduit::Node const&)
1,        ascent::AscentRuntime::Execute(conduit::Node const&)
1,          flow::Workspace::execute()
1,            ascent::runtime::filters::BasicTrigger::execute()
1,              ascent::Ascent::execute(conduit::Node const&)
1,                ascent::AscentRuntime::Execute(conduit::Node const&)
1,                  flow::Workspace::execute()
1,                    ascent::runtime::filters::RelayIOSave::execute()
1,                      ascent::runtime::filters::mesh_blueprint_save(conduit::Node const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int, conduit::Node const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&)
1,                        conduit::relay::mpi::io::blueprint::save_mesh(conduit::Node const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, conduit::Node const&, int)
1,                          conduit::relay::mpi::io::blueprint::write_mesh(conduit::Node const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, conduit::Node const&, int)
1,                            conduit::relay::io::IOHandle::write(conduit::Node const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)
1,                              conduit::relay::io::HDF5Handle::write(conduit::Node const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, conduit::Node const&)
1,                                conduit::relay::io::hdf5_write(conduit::Node const&, long&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, conduit::Node const&)
1,                                  conduit::relay::io::write_conduit_node_to_hdf5_tree(conduit::Node const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, long&, conduit::Node const&)
1,                                    conduit::relay::io::write_conduit_node_children_to_hdf5_group(conduit::Node const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, long, conduit::Node const&)
1,                                      conduit::relay::io::write_conduit_node_children_to_hdf5_group(conduit::Node const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, long, conduit::Node const&)
1,                                        conduit::relay::io::write_conduit_node_children_to_hdf5_group(conduit::Node const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, long, conduit::Node const&)
1,                                          conduit::relay::io::write_conduit_node_children_to_hdf5_group(conduit::Node const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, long, conduit::Node const&)
1,                                            conduit::relay::io::write_conduit_leaf_to_hdf5_group(conduit::Node const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, long, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, conduit::Node const&)
1,                                              conduit::relay::io::write_conduit_leaf_to_hdf5_dataset(conduit::Node const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, long&, conduit::Node const&)
1,                                                H5Dwrite
1,                                                  H5D__write_api_common.constprop.0
1,                                                    H5VL_dataset_write
1,                                                      H5VL__native_dataset_write
1,                                                        H5D__write
1,                                                          H5D__chunk_write
1,                                                            H5D__select_write
1,                                                              H5D__select_io
1,                                                                H5D__compact_writevv
1,                                                                  H5VM_memcpyvv
1,                                                                    __memcpy_generic
}}}
#}}}
#}}}
#{{{ VTK-m
# ./vtkm.sh OFF ON OFF ON
# ./vtkm.sh OFF ON OFF ON 0 --rendering /dev/shm/piccinal/r
#{{{ insitu_ascent/develop:1825576142 -v default 
#EXE     INSITU  AOS DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping
DummySPH VTKm    OFF ON   ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A           #SOA&TIPSY
DummySPH VTKm    OFF OFF  ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A           #SOA&TIPSY
DummySPH VTKm    OFF ON  OFF  ON yes    OK          OK             KO?           OK             N/A       issues/11
DummySPH VTKm    OFF OFF OFF  ON yes    OK          OK             KO?           OK             N/A       KO            
#}}}
#{{{ insitu_ascent/develop:1827451634 -v default 
                                                                                                #varname
#EXE     INSITU  AOS DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping
DummySPH VTKm    OFF ON   ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A           #SOA&TIPSY
DummySPH VTKm    OFF OFF  ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A           #SOA&TIPSY
DummySPH VTKm    OFF ON  OFF  ON yes    OK          OK             CORE          OK             OK        issues/11
DummySPH VTKm    OFF OFF OFF  ON yes    OK          OK             CORE          OK             OK        issues/11 (try ~cuda)
                                                    =WINDSHOCK
                                                    #ifdef CLIPS                 #ifdef HISTSAMPLING
#}}}
#{{{ /capstor/scratch/cscs/jfavre/Ascent-cuda/install/vtk-m-v2.3.0/ + prgenv-gnu/24.11:v2
                                                                                                #varname
#EXE     INSITU  AOS DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping
DummySPH VTKm    OFF ON   ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A      #SOA&TIPSY
DummySPH VTKm    OFF OFF  ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A      #SOA&TIPSY
DummySPH VTKm    OFF ON  OFF  ON yes    OK          OK             CORE          OK             OK        CORE
DummySPH VTKm    OFF OFF OFF  ON yes    OK          OK             CORE          OK             OK        CORE
                                                    #WINDSHOCK                   #WINDSHOCK
                                                    #ifdef CLIPS                 #ifdef HISTSAMPLING
#}}}
#}}}
#{{{ CATALYST insitu_ascent/develop-gcc12:1827486263@daint -v default
# gcc-12.4.0/libcatalyst-2.0.0
# ./catalyst.sh OFF OFF OFF ON 0
#EXE     INSITU  AOS DBL TIP H5P BUILD? catalyst_clipping.py
DummySPH CATA    OFF OFF OFF ON  OK     OK

#}}}
#}}}
