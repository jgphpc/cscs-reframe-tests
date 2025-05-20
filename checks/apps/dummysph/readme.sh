#!/bin/bash

# RULES:
# TIPSY & H5P   = NO
# AOS   & H5P   = NO
# SOA   & TIPSY = NO
# DBL   & TIPSY = NO

#{{{ VTK-m
# ./vtkm.sh OFF ON OFF ON b
# ./vtkm.sh OFF ON OFF ON 0 --rendering /dev/shm/piccinal/r

#{{{ AOS ON ~PKDGRAV
#{{{ insitu_ascent/develop:1825576142 -v default

#EXE     INSITU  AOS DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping
DummySPH VTKm    ON  ON   ON OFF yes    N/A         N/A            N/A           N/A            N/A       N/A           #DBL&TIPSY
DummySPH VTKm    ON  OFF  ON OFF yes    OK          OK             issues/7      OK             N/A       OK            
DummySPH VTKm    ON  ON  OFF  ON N/A    N/A         N/A            N/A           N/A            N/A       N/A           #AOS&H5
DummySPH VTKm    ON  OFF OFF  ON N/A    N/A         N/A            N/A           N/A            N/A       N/A           #AOS&H5

#}}}
#}}}

#{{{ AOS OFF ~SPHEXA
#{{{ insitu_ascent/develop:1825576142 -v default

#EXE     INSITU  AOS DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping
DummySPH VTKm    OFF ON   ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A           #SOA&TIPSY
DummySPH VTKm    OFF OFF  ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A           #SOA&TIPSY
DummySPH VTKm    OFF ON  OFF  ON yes    OK          OK             KO?           OK             N/A       issues/11
DummySPH VTKm    OFF OFF OFF  ON yes    OK          OK             KO?           OK             N/A       KO            

#}}}
#}}}
#}}}

#{{{ ASCENT
# Usage:
# ./ascent.sh OFF ON OFF ON b
# ./ascent.sh OFF ON OFF ON 0 --rendering /dev/shm/piccinal/r

#{{{ AOS ON ~PKDGRAV
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

#EXE     INSITU   AOS  DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping
DummySPH ASCENT    ON  ON   ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A           #DBL&TIPSY
DummySPH ASCENT    ON  OFF  ON OFF yes    KO          hangs?         blueprint?    CastAndCall?   KO        OK
DummySPH ASCENT    ON  ON  OFF  ON N/A    N/A         N/A            N/A           N/A            N/A       N/A           #AOS&H5
DummySPH ASCENT    ON  OFF OFF  ON N/A    N/A         N/A            N/A           N/A            N/A       N/A           #AOS&H5

#}}}
#}}}

#{{{ AOS OFF ~SPHEXA
#{{{ insitu_ascent_nocuda/develop-gcc12:1827699279@daint
                                                                                                #varname
#EXE     INSITU  AOS DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping
DummySPH ASCENT  OFF ON   ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A           #SOA&TIPSY
DummySPH ASCENT  OFF OFF  ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A           #SOA&TIPSY
DummySPH ASCENT  OFF ON  OFF  ON OK     OK*         OK*            vxvyvz:OK?    OK*            rho:OK    OK
DummySPH ASCENT  OFF OFF OFF  ON OK     OK*         OK             vxvyvz:OK?    Cast_failed    rho:OK    OK

SPHEXA   ASCENT  TODO
#}}}
#{{{ insitu_ascent/develop:1825576142 -v default

#EXE     INSITU  AOS DBL TIP H5P BUILD? --rendering --thresholding --compositing --histsampling --binning --dumping
DummySPH ASCENT  OFF ON   ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A           #SOA&TIPSY
DummySPH ASCENT  OFF OFF  ON OFF N/A    N/A         N/A            N/A           N/A            N/A       N/A           #SOA&TIPSY
DummySPH ASCENT  OFF ON  OFF  ON KO
DummySPH ASCENT  OFF OFF OFF  ON KO

SPHEXA   ASCENT
#}}}
#}}}
#}}}
