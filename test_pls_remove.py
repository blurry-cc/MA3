from MA3 import * 
n = 10**6
d = 11 


t0 = pc()
avg = sphere_volume_parallel1(n, d, 2)
t = pc() 


print(t-t0)