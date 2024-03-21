import random

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        less = [x for x in arr if x < pivot]
        equal = [x for x in arr if x == pivot]
        more = [x for x in arr if x > pivot]
        return quick_sort(less) + equal + quick_sort(more)

size = 5000000
d = [random.randint(1, 100000) for _ in range(size)]

print("ソート前:", *d[:10])
d = quick_sort(d)
print("ソート後:", *d[:10])
