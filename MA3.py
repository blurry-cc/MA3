""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
import numpy as np # for exc 1.2
import functools # for exc 1.2 

#random.seed(42) # make results reproducible

def approximate_pi(n): 
    nc_x, nc_y = [], []
    ns_x, ns_y = [], []

    for _ in range(n): 
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x**2 + y**2 < 1: 
            nc_x.append(x)
            nc_y.append(y)
        else: # then outside circle 
            ns_x.append(x)
            ns_y.append(y)

    plt.scatter(nc_x, nc_y, c='red') #plot points inside circle in red
    plt.scatter(ns_x, ns_y, c='blue')
    plt.savefig(f'approx-pi_{n}')

    return round(4*len(nc_x)/n, 6) #len(nc_x) = len(nc_y) = n.o. of points inside circle. 

def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    # d is the number of dimensions of the sphere 

    points = [(2*np.random.uniform(size=d) - 1) for _ in range(n)] # list containing n arrays, of which elements are on (-1, 1)
    inside = list(filter(lambda x: np.sum(np.square(x)) < 1, points)) # where x is an element (numpy array) of points 

    nd = len(inside) # amount of points inside the sphere

    return (2**d)*(nd/n)  # approximation of sphere volume, when r = 1 (else multiply by r^d)

def hypersphere_exact(d): #Ex2, real value
    # d is the number of dimensions of the sphere 
    return m.pi**(d/2)/m.gamma(1 + d/2)

#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=10):
      #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    with future.ProcessPoolExecutor() as ex: 
        p = [ex.submit(sphere_volume, n, d) for _ in range(np)]
        results = [f.result() for f in p]
        
    return mean(results)

#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    partial = n//np # split the job 
    with future.ProcessPoolExecutor() as ex: 
        p = [ex.submit(sphere_volume, partial, d) for _ in range(np)] # np processes of smaller size 
        results = [f.result() for f in p] # put all results in a list 

    return mean(results) # average the results. the average of np processes of size n//np should be approximately
                        # equal to 1 process of size n. 
    
def main():
    #Ex1
    print("Testing old approximate pi.")
    dots = [1000, 10000, 100000]
    for n in dots:
        print(approximate_pi(n))
    # #Ex2
    # n = 100000
    # d = 2
    # sphere_volume(n,d)
    # print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)} m^{d} ")

    # n = 100000
    # d = 11
    # sphere_volume(n,d)
    # print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)} m^{d} ")

    # #Ex3
    # n = 100000
    # d = 11
    # print("Testing excercise 3\n")
    # start = pc()
    # for y in range (10):
    #     sphere_volume(n,d)
    # stop = pc()
    # print(f"Ex3: Sequential time of {d} and {n}: {round(stop-start, 3)} seconds\n")
    # print("What is parallel time?")
    # start = pc() 
    # sphere_volume_parallel1(n, d)
    # stop = pc()
    # print(f"Parallel time of {d} and {n}: {round(stop-start, 3)} seconds\n")
    # print("Test complete.")

    # #Ex4
    # n = 1000000
    # d = 11
    # print("Testing excercise 4")
    # start = pc()
    # sphere_volume(n,d)
    # stop = pc()
    # print(f"Ex4: Sequential time of {d} and {n}: {round(stop-start, 3)} seconds")
    # print("What is parallel time?")
    # start = pc() 
    # sphere_volume_parallel2(n, d)
    # stop = pc() 
    # print(f"Ex4: Parallell time of {d} and {n}: {round(stop-start,3)} seconds")
    # print("Test complete")
    
    

if __name__ == '__main__':
	main()
