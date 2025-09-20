import timeit

# Setup with 1 million items, half of which are duplicates
data = [(f"key_{i}", i) for i in range(500000)] * 2

def direct_assignment():
    table = {}
    for key, value in data:
        table[key] = value
    return table

def check_then_set():
    table = {}
    for key, value in data:
        if key not in table:
            table[key] = value
    return table

def check_then_set_with_try():
    table = {}
    for key, value in data:
        try:
            _ = table[key]
        except KeyError:
            table[key] = value
    return table

def check_then_set_with_get_4():
    table = {}
    for key, value in data:
        if table.get(key):
            pass
        else:
            table[key] = value
    return table

def check_then_set_with_get_5():
    table = {}
    for key, value in data:
        _value = table.get(key)
        if _value:
            continue
        table[key] = value
    return table

# Time the two approaches
time1 = timeit.timeit(direct_assignment, number=10)
time2 = timeit.timeit(check_then_set, number=10)
time3 = timeit.timeit(check_then_set_with_try, number=10)
time4 = timeit.timeit(check_then_set_with_get_4, number=10)
time5 = timeit.timeit(check_then_set_with_get_5, number=10)


print(f"Direct assignment: {time1:.4f} seconds")
print(f"Check then set:    {time2:.4f} seconds")
print(f"check_then_set_with_try:    {time3:.4f} seconds")
print(f"check_then_set_with_get_4:    {time4:.4f} seconds")
print(f"check_then_set_with_get_5:    {time5:.4f} seconds")

# Example Output:
# Direct assignment: 0.8531 seconds
# Check-then-set:    1.0245 seconds
