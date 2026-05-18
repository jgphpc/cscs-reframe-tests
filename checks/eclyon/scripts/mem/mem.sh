#!/bin/bash

in=latest.json

#kB: mem_avail=$(jq -r '.runs[].testcases[].perfvalues' $in |grep -A1 mem_avail\" |grep , |tr -d , |sort -nk 1)
mem_avail=$(jq -r '.runs[].testcases[].perfvalues' $in |grep -A1 mem_avail_GB\" |grep , |tr -d , |sort -nk 1)

echo "# mem_avail=$mem_avail"
# max=$(echo $mem_avail |tr " " "\n" |tail -1)

# AVERAGE
qavg=$(echo $mem_avail |tr " " "\n" |awk '{s=s+$1}END{printf "%.1f", s/NR}')

# MEDIAN
qm=$(echo $mem_avail |tr " " "\n" |awk ' { a[i++]=$1; } END { print a[int(i/2)]; }')

# PERCENTILE 25th
q1=$(echo $mem_avail |tr " " "\n" |awk '{ a[NR] = $1 } END {pos=0.25*(NR+1); if (pos == int(pos)) {print a[pos] } else { lower=int(pos) ;upper=lower+1 ;frac=pos-lower ;print a[lower] + frac * (a[upper] - a[lower])} }')
pctq1=$(echo $qm $q1 |awk '{printf "%.4f", ($1-$2)/$1*100}')
pctq1_=$(echo $pctq1 |awk '{printf "%.4f", 100-$1}')

# MIN
qmin=$(echo $mem_avail |tr " " "\n" |head -1)
pctqmin=$(echo $qm $qmin |awk '{printf "%.4f", ($1-$2)/$1*100}')
pctqmin_=$(echo $pctqmin |awk '{printf "%.4f", 100-$1}')

# REPORT
echo "# $qavg = average"
echo "# $qm = median (100%)"
echo "# $q1 = q1 = median - $pctq1 % ($pctq1_ % of median)"
echo "# $qmin = min = median - $pctqmin % ($pctqmin_ % of median)"
