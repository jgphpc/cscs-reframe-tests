#!/usr/bin/env bash
# gpumon.sh — sample rocm-smi telemetry on all GPUs of this node while a GPU
# job (e.g. coralgemm) is running, then print a per-GPU load summary.
#
# Usage:
#   ./gpumon.sh start [interval_s] [duration_s] [outdir]   background it, return now
#   ./gpumon.sh stop                                       "ctrl-c" it, wait, print summary
#   ./gpumon.sh [interval_s] [duration_s] [outdir]         foreground (ctrl-c to stop)
#
# Arguments:
#     interval_s  seconds between samples        (default 5)
#     duration_s  stop after this many seconds   (default 0 = until stopped)
#     outdir      output directory               (default ./gpumon_<host>_<ts>)
#
# start/stop write ./gpumon.pid (override: GPUMON_PIDFILE=/path/to/file).
# The summary table is printed by the monitor when it receives the stop
# signal, so it lands in the job log if the monitor was started by the job.
#
# Jobscript wiring:
#     ./gpumon.sh start 5
#     srun .../gemm ...          # your test
#     ./gpumon.sh stop
# ReFrame equivalent (e.g. in a prerun_cmds/postrun_cmds pair):
#     self.prerun_cmds  += ['./gpumon.sh start 5']
#     self.postrun_cmds += ['./gpumon.sh stop']
#
# The key summary column is sclk_avg over samples under load (sclk>=1 GHz or
# use>=50%). Run it the same way on a known-good node and compare.

set -u

PIDFILE=${GPUMON_PIDFILE:-gpumon.pid}

# ------------------------------------------------------------------ helpers --

# parse one rocm-smi log into CSV rows (POSIX sed+awk, portable)
parse_sample() {  # $1 = raw log file, $2 = epoch timestamp
    sed -n \
        -e 's/^GPU\[\([0-9][0-9]*\)\][^:]*: sclk clock level: [^:]*: (\([0-9][0-9]*\)Mhz).*/\1 sclk \2/p' \
        -e 's/^GPU\[\([0-9][0-9]*\)\][^:]*: mclk clock level: [^:]*: (\([0-9][0-9]*\)Mhz).*/\1 mclk \2/p' \
        -e 's/^GPU\[\([0-9][0-9]*\)\][^:]*: fclk clock level: [^:]*: (\([0-9][0-9]*\)Mhz).*/\1 fclk \2/p' \
        -e 's/^GPU\[\([0-9][0-9]*\)\][^:]*: socclk clock level: [^:]*: (\([0-9][0-9]*\)Mhz).*/\1 socclk \2/p' \
        -e 's/^GPU\[\([0-9][0-9]*\)\][^:]*: Temperature (Sensor junction) (C): \([0-9.][0-9.]*\).*/\1 tj \2/p' \
        -e 's/^GPU\[\([0-9][0-9]*\)\][^:]*: Temperature (Sensor memory) (C): \([0-9.][0-9.]*\).*/\1 tmem \2/p' \
        -e 's/^GPU\[\([0-9][0-9]*\)\][^:]*: .*Power (W): \([0-9.][0-9.]*\).*/\1 pw \2/p' \
        -e 's/^GPU\[\([0-9][0-9]*\)\][^:]*: GPU use (%): \([0-9.][0-9.]*\).*/\1 use \2/p' \
        -e 's/^GPU\[\([0-9][0-9]*\)\][^:]*: GPU [Mm]emory use (%): \([0-9.][0-9.]*\).*/\1 memuse \2/p' \
        "$1" | awk -v ts="$2" '
        {
            if (!($1 in seen)) { seen[$1] = 1; ord[++n] = $1 }
            val[$1 "," $2] = $3
        }
        END {
            for (i = 1; i <= n; i++) {
                g = ord[i]
                printf "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n", ts, g,
                    val[g ",sclk"], val[g ",mclk"], val[g ",fclk"], val[g ",socclk"],
                    val[g ",tj"], val[g ",tmem"], val[g ",pw"], val[g ",use"], val[g ",memuse"]
            }
        }'
}

# ------------------------------------------------------------- monitor body --

monitor_main() {  # args: [interval_s] [duration_s] [outdir]
    INTERVAL=${1:-5}
    DURATION=${2:-0}
    OUTDIR=${3:-}

    ROCM_SMI=${GPUMON_ROCM_SMI:-$(command -v rocm-smi 2>/dev/null || echo /opt/rocm/bin/rocm-smi)}
    command -v "$ROCM_SMI" >/dev/null 2>&1 || {
        echo "gpumon: rocm-smi not found (tried PATH and /opt/rocm/bin)"; return 1; }

    [ -z "$OUTDIR" ] && OUTDIR="gpumon_$(hostname -s)_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$OUTDIR/raw"
    CSV="$OUTDIR/telemetry.csv"
    echo "epoch,gpu,sclk_mhz,mclk_mhz,fclk_mhz,socclk_mhz,tj_C,tmem_C,power_w,use_pct,memuse_pct" > "$CSV"

    # one-shot static info; each call may fail depending on rocm-smi version/root
    INFO="$OUTDIR/info.log"
    "$ROCM_SMI" --showproductname  > "$INFO" 2>&1 || true
    "$ROCM_SMI" --showvbios       >> "$INFO" 2>&1 || true
    "$ROCM_SMI" --showserial      >> "$INFO" 2>&1 || true
    "$ROCM_SMI" --showdriverversion >> "$INFO" 2>&1 || true

    STOP=0
    trap 'STOP=1' INT TERM
    SMPL=0
    end=$(( DURATION > 0 ? SECONDS + DURATION : 0 ))
    echo "gpumon: node=$(hostname -s) interval=${INTERVAL}s" \
         "$([ "$DURATION" -gt 0 ] && echo "duration=${DURATION}s" || echo "until stopped")" \
         "-> $OUTDIR"
    while [ $STOP -eq 0 ] && { [ "$DURATION" -le 0 ] || [ "$SECONDS" -lt "$end" ]; }; do
        SMPL=$((SMPL + 1))
        ts=$(date +%s)
        f="$OUTDIR/raw/sample_$(printf %05d "$SMPL")_${ts}.log"
        "$ROCM_SMI" --showclocks --showtemp --showpower --showuse --showmemuse > "$f" 2>&1
        parse_sample "$f" "$ts" >> "$CSV"
        sleep "$INTERVAL"
    done

    # per-GPU summary over the whole run (also saved to <outdir>/summary.txt)
    {
        echo
        echo "gpumon: $SMPL samples -> $CSV"
        awk -F, '
    NR > 1 {
        g = $2
        if (!(g in n)) { n[g] = 0; ord[++k] = g }
        n[g]++
        sclk = $3 + 0; use = $10 + 0; pw = $9 + 0
        if ($4 + 0 > 0) { ms[g] += $4; mc[g]++ }     # mclk, all samples
        if (sclk >= 1000 || use >= 50) {              # sample under load
            L[g]++; sum[g] += sclk; psum[g] += pw
            if (!(g in smin) || sclk < smin[g]) smin[g] = sclk
            if (sclk > smax[g]) smax[g] = sclk
        }
        if ($7 + 0 > tmax[g]) tmax[g] = $7 + 0        # junction temp max
    }
    END {
        if (k == 0) { print "gpumon: no data collected"; exit }
        best = 0
        for (i = 1; i <= k; i++) { g = ord[i]
            avg[g] = L[g] ? sum[g] / L[g] : 0
            if (avg[g] > best) best = avg[g] }
        printf "%-4s %6s %8s %9s %9s %9s %9s %8s %9s %12s\n", \
            "GPU", "busy%", "samples", "sclk_avg", "sclk_min", "sclk_max", \
            "mclk_avg", "Tj_max", "P_avg_W", "sclk_vs_best"
        for (i = 1; i <= k; i++) { g = ord[i]
            deficit = best > 0 ? 100 * avg[g] / best - 100 : 0
            printf "%-4s %6.1f %8d %9.0f %9.0f %9.0f %9.0f %8.1f %9.1f %11.1f%%\n", \
                g, 100 * L[g] / n[g], n[g], avg[g], smin[g], smax[g], \
                (mc[g] ? ms[g] / mc[g] : 0), \
                tmax[g], (L[g] ? psum[g] / L[g] : 0), deficit
        }
        print "note: sclk_vs_best below ~-1.5% on a busy GPU = sustained clock deficit"
    }' "$CSV"
    } &> gpumon.sh.rpt
    ## } | tee "$OUTDIR/summary.txt"
    rm -f "$PIDFILE"
}

# ----------------------------------------------------------------- dispatch --

case "${1:-}" in
    
start)  # fork the monitor into the background, remember its pid, return now
    shift
    "$0" __monitor__ "$@" &
    echo $! > "$PIDFILE"
    echo "gpumon: started monitor pid $(cat "$PIDFILE") (pidfile $PIDFILE)"
    ;;
    
stop)   # signal the monitor, then wait for its summary
    if [ ! -f "$PIDFILE" ]; then
        echo "gpumon: no pidfile $PIDFILE (monitor not started here?)"
        exit 0
    fi
    PID=$(cat "$PIDFILE")
    if ! kill -0 "$PID" 2>/dev/null; then
        echo "gpumon: monitor $PID not running"
        rm -f "$PIDFILE"; exit 0
    fi

    # NB: a monitor started via './gpumon.sh start ... &' runs with SIGINT
    # ignored (POSIX: async commands ignore SIGINT and it cannot be trapped
    # again), so TERM is what actually stops it. TERM is trapped and prints
    # the summary, just like INT/ctrl-c does in foreground mode.
    kill -TERM "$PID"
    i=0
    while kill -0 "$PID" 2>/dev/null && [ $i -lt 30 ]; do
        sleep 1; i=$((i + 1))
    done

    if kill -0 "$PID" 2>/dev/null; then
        echo "gpumon: monitor $PID did not stop after TERM, sending KILL"
        kill -KILL "$PID" 2>/dev/null
    fi

    rm -f "$PIDFILE"
    echo "gpumon: monitor stopped"
    ;;

__monitor__)
    shift
    monitor_main "$@"
    ;;

*)
    monitor_main "$@"
    ;;
esac
