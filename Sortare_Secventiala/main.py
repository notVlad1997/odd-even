# Python Program to implement
# Odd-Even / Brick Sort
from numpy import random
from memory_profiler import profile
import time


#@profile
def oddEvenSort(arr, n):
    isSorted = 0
    while isSorted == 0:
        isSorted = 1
        temp = 0
        for i in range(1, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                isSorted = 0

        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                isSorted = 0


n = 1
random.seed(169)
arr = [0]
for j in range(7, 17):
    size_of = n * j
    arr = random.randint(10000000, size=pow(2, j))
    start = time.time()
    oddEvenSort(arr, pow(2, j))
    end = time.time()
    print(f'{j}:{end - start} secunde')
    # for i in range(0, pow(2, j)):
    #     print(arr[i], end=' ')
    #print()
