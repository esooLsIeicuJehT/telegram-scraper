import time
import subprocess
import sys
import os

def benchmark_old(n=5):
    start_time = time.time()
    print(f"Benchmarking 'Old' method with {n} iterations...")
    for i in range(n):
        # Simulate os.system('start cmd') and waiting for window
        # In reality, os.system takes time too, but sleep is the main waiter
        time.sleep(1.5)
        # Simulate keyboard typing (negligible but > 0)
        time.sleep(0.1)
        # Simulate Enter press
        pass
    end_time = time.time()
    return end_time - start_time

def benchmark_new(n=5):
    start_time = time.time()
    print(f"Benchmarking 'New' method with {n} iterations...")
    processes = []
    for i in range(n):
        # Simulate launching a process
        # We use a simple command that exits quickly
        p = subprocess.Popen([sys.executable, '-c', 'print("hello")'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        processes.append(p)

    # We don't wait for them to finish in the main loop of the actual app,
    # but strictly speaking we just fire and forget in the app loop.
    # However, to be fair, Popen returns almost instantly.

    end_time = time.time()

    # Clean up
    for p in processes:
        p.wait()

    return end_time - start_time

if __name__ == "__main__":
    n = 5
    old_time = benchmark_old(n)
    print(f"Old method time: {old_time:.4f} seconds")

    new_time = benchmark_new(n)
    print(f"New method time: {new_time:.4f} seconds")

    improvement = old_time / new_time if new_time > 0 else float('inf')
    print(f"Speedup: {improvement:.2f}x")
