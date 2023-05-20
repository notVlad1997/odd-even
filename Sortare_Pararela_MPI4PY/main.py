# Python Program to implement
# Odd-Even / Brick Sort
import time
import numpy
from numpy import random
from memory_profiler import profile
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # processId of the current process
size = comm.Get_size()  # total number of processes in the communicator

random.seed(169)

#fp = open('memory_profiler.log', 'w+')


#@profile(stream=fp)
def oddEvenSort(arr, n):
    sort = True
    isSorted = False
    while isSorted is False:
        isSorted = True
        for i in range(1, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                isSorted = False
                sort = False
        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                isSorted = False
                sort = False
    comm.send(sort, dest=0)
    if sort is False:
        comm.send(arr.copy(), dest=0)


arr = [0]
for j in range(7, 18):
    if rank == 0:
        N = pow(2, j)
        arr = random.randint(300, size=N)
        startTime = time.time()
        isSorted = False
        start = 2
        while isSorted is False:
            isSorted = True
            isSort = True
            intervals = size * 2 - 1
            for i in range(start, intervals - 1, 2):
                begin = int(N / (intervals - 1)) * (i - 1) + min(N % (intervals - 1), i - 1)
                begin2 = int(N / (intervals - 1)) * i + min(N % (intervals - 1), i)
                end = begin2 + int(N / (intervals - 1)) - 1 * int(N % (intervals - 1) < i)
                # print(begin, " ", end)
                data = numpy.array(arr[begin:end].copy())
                comm.send(data, dest=int(i / 2) + (2 - start))
                isSort = comm.recv(source=int(i / 2) + (2 - start))
                if isSort is False:
                    isSorted = False
                    arr[begin:end] = comm.recv(source=int(i / 2) + (2 - start))
            if start == 1:
                data = numpy.array([-2])
                comm.send(data, dest=size - 1)
                start = 2
            else:
                start = 1
        for i in range(1, size):
            data = numpy.array([-1])
            comm.send(data, dest=i)
            # comm.barrier()
        endTime = time.time()
        print(f'{j}:{endTime - startTime} secunde')

    else:
        data = comm.recv(source=0)
        while data[0] != -1:
            if data[0] != -2:
                oddEvenSort(data, len(data))
            data = comm.recv(source=0)
