import numba as nb
import numpy as np

@nb.njit( (nb.double[:,:], nb.double[:,:], nb.double) )
def collisions(r,v,collision_radius2):
    """Resolve pairwise collisions"""
    N = len(r)
    for i in range(N-1):
        for j in range(i+1,N):
            dr2 = ((r[i]-r[j])**2).sum()
            if dr2<collision_radius2:
                # collision rule for equal masses
                v[i] = v[i] - np.dot(v[i]-v[j],r[i]-r[j])/dr2*(r[i]-r[j])
                v[j] = v[j] - np.dot(v[j]-v[i],r[j]-r[i])/dr2*(r[j]-r[i])
