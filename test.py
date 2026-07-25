"""
Just a test for stuff

1. Import plugins
2. Collect metrics
3. Show time
"""

# Import plugins
import collectors.system.collector as system
import collectors.load.collector as load
import collectors.cpu.collector as cpu
import collectors.memory.collector as memory
import collectors.swap.collector as swap

# Collect metrics
system_metrics = system.collect()
load_metrics = load.collect()
cpu_metrics = cpu.collect()
memory_metrics = memory.collect()
swap_metrics = swap.collect()

# Show metrics
print(system_metrics)
print(load_metrics)
print(cpu_metrics)
print(memory_metrics)
print(swap_metrics)
