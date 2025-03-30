import sys
import os
import tracemalloc

tracemalloc.start()

# List of imported modules
used_modules = set(sys.modules.keys())

print("\nTracking memory usage per module...\n")

# Get memory usage per module
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics("lineno")

for stat in top_stats[:10]:  # Show top 10 memory-consuming modules
    print(stat)

tracemalloc.stop()
