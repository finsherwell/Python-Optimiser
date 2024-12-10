import time

def slow_function():
    time.sleep(2)  # Simulate a slow operation

def fast_function():
    return sum(range(1000))

slow_function()
fast_function()