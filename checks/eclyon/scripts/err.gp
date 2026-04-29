# script pour gnuplot version > 5.0
reset

set terminal pop
set output

set logscale xy
set format x '10^{%T}'
set format y '10^{%T}'
set xlabel 'n Intervalles'
set ylabel '| pi - M\_PI | Error'

s(x)=-1.00*x-2

# M_PI = 3.14159265358979323846
set title 'https://pmcs2i.ec-lyon.fr/documentation/quick-start/first.html#realisation-d-une-exploration-parametrique'
set grid

# for ii in builtin PrgEnv-gnu PrgEnv-intel ;do grep $ii error.txt > $ii ;done
#plot 'builtin' u 1:2 w lp lt 1 lc -1 dt 1 lw 2 title 'Newton:builtin'
plot 'builtin' u 1:2 w lp lt 1 lw 1 title 'Newton:builtin', \
     'PrgEnv-gnu' u 1:2 w lp lt 2 lw 1 title 'Newton:PrgEnv-gnu', \
     'PrgEnv-intel' u 1:2 w lp lt 3 lw 1 title 'Newton:PrgEnv-intel'

# set label 6 '-1' at 20000,2e-5 center tc ls -1
# replot [x=6000:60000] exp(s(log(x))) w l lt 1 lc -1 dt 2 lw 2 notitle

set terminal push
set terminal svg
set output 'error.svg'

# set terminal pdf color
# set output 'error.pdf'
replot
set terminal pop
