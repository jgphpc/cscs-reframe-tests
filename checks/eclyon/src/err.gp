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

plot 'error.txt' u 1:2 w lp lt 1 lc -1 dt 1 lw 2 title 'Newton'
set label 6 '-1' at 20000,2e-5 center tc ls -1
replot [x=6000:60000] exp(s(log(x))) w l lt 1 lc -1 dt 2 lw 2 notitle

set terminal push
set terminal svg # pdf color
set output 'error.svg'
replot
set terminal pop
