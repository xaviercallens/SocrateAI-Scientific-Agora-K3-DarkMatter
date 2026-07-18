#!/bin/bash
# monitor_parallel_batteries.sh
# Monitor both battery processes and run comparison when vectorized completes

set -e

echo "======================================================================"
echo "Parallel Battery Monitor"
echo "======================================================================"
echo ""
echo "Monitoring PIDs:"
echo "  Original (loop): 7371"
echo "  Vectorized (broadcast): $(pgrep -f 'run_s2_1_kernel_swap_battery_vectorized' | head -1)"
echo ""

ORIG_PID=7371
VECT_PID=$(pgrep -f 'run_s2_1_kernel_swap_battery_vectorized' | head -1)

if [ -z "$VECT_PID" ]; then
    echo "✗ Vectorized battery not running"
    exit 1
fi

echo "Waiting for vectorized battery to complete (PID $VECT_PID)..."
echo ""

# Poll until process completes
while kill -0 $VECT_PID 2>/dev/null; do
    echo "[$(date '+%H:%M:%S')] Vectorized battery running..."

    # Check output file size (should grow during execution)
    if [ -f "data/k3t2/d1_3b_kernel_swap_v2_vectorized.json" ]; then
        SIZE=$(stat -c%s "data/k3t2/d1_3b_kernel_swap_v2_vectorized.json")
        echo "  Output file size: $SIZE bytes"
    fi

    # Check both process status
    echo -n "  Status: "
    ps aux | grep -E "(PID $ORIG_PID|PID $VECT_PID)" | grep -v grep | awk '{print $3 "% CPU"}' || echo "(process check)"

    sleep 5
done

echo ""
echo "✓ Vectorized battery complete!"
echo ""

# Wait for original battery if still running
if kill -0 $ORIG_PID 2>/dev/null; then
    echo "Original battery still running (PID $ORIG_PID)"
    echo "Waiting for original..."
    while kill -0 $ORIG_PID 2>/dev/null; do
        echo "[$(date '+%H:%M:%S')] Original battery running..."
        sleep 10
    done
    echo "✓ Original battery complete!"
fi

echo ""
echo "======================================================================"
echo "Both batteries complete. Running comparison..."
echo "======================================================================"
echo ""

python3 compare_battery_results.py

echo ""
echo "======================================================================"
echo "Monitor complete. Check COMPARISON_REPORT.md for results."
echo "======================================================================"
