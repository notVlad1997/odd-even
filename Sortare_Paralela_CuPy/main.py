import time

import cupy as cp
from memory_profiler import profile

cp.random.seed(169)

fp = open('memory_profiler.log', 'w+')
@profile(stream=fp)
def oddEvenSort(arr):
    n = len(arr)
    is_sorted = False

    while not is_sorted:
        is_sorted = True

        even_indices = cp.arange(0, n - 1, 2)
        swap_mask = arr[even_indices] > arr[even_indices + 1]
        if cp.any(swap_mask):
            is_sorted = False
            arr[even_indices[swap_mask]], arr[even_indices[swap_mask] + 1] = arr[even_indices[swap_mask] + 1], arr[
                even_indices[swap_mask]]

        odd_indices = cp.arange(1, n - 1, 2)
        swap_mask = arr[odd_indices] > arr[odd_indices + 1]
        if cp.any(swap_mask):
            is_sorted = False
            arr[odd_indices[swap_mask]], arr[odd_indices[swap_mask] + 1] = arr[odd_indices[swap_mask] + 1], arr[
                odd_indices[swap_mask]]

    return arr


if __name__ == "__main__":
    for j in range(7, 18):
        N = pow(2, j)
        arr = cp.random.randint(10000000, size=N)  # Using cupy for random array generation

        startTime = time.time()
        sorted_arr = oddEvenSort(arr)
        endTime = time.time()

        print(f'{j}: {endTime - startTime} seconds')
