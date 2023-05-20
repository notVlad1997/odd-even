import time
from numpy import random
from memory_profiler import profile
import multiprocessing

random.seed(169)


fp = open('memory_profiler.log', 'w+')
@profile(stream=fp)
def oddEvenSort(arr, begin, end):
    n = len(arr)
    sort = True
    isSorted = False
    while isSorted is False:
        isSorted = True
        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                isSorted = False
                sort = False
        for i in range(1, n, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                isSorted = False
                sort = False
    return sort, begin, end, arr


if __name__ == "__main__":
    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)
    arr = [0]
    for j in range(7, 18):
        N = pow(2, j)
        arr = random.randint(10000000, size=N)
        startTime = time.time()
        isSorted = False
        start = 1
        while isSorted is False:
            isSorted = True
            isSort = True
            intervals = num_processes * 2 - 1
            results = []

            for i in range(start, intervals - 1, 2):
                begin = int((N+1) / (intervals - 1)) * (i - 1) + min((N+1) % (intervals - 1), i - 1)
                begin2 = int((N+1) / (intervals - 1)) * i + min((N+1) % (intervals - 1), i)
                end = begin2 + int((N+1) / (intervals - 1)) - 1 * int((N+1) % (intervals - 1) < i)
                data = arr[begin:end]
                results.append(pool.apply_async(oddEvenSort, (data, begin, end)))

            for i, result in enumerate(results):
                isSort, begin, end, sorted_arr = result.get()
                # print(isSort)
                if isSort is False:
                    isSorted = False
                    arr[begin:end] = sorted_arr

            if start == 1:
                start = 2
                isSorted = False
            else:
                start = 1

        endTime = time.time()
        print(f'{j}:{endTime - startTime} secunde')
    pool.close()
    pool.join()