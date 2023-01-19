import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import numba as nb

def initialise(N,L,T):
    r = np.random.uniform(0,L,size=(N,2))
    v = np.random.uniform(-1,1,r.shape)
    # scale the velocity so that the kinetic energy reflects the equipartition theorem
    random_T = (0.5*(v**2).mean())
    scale = T/random_T
    v *= np.sqrt(scale)
    return r,v


def evolve(r,v,L,dt,radius):
    r = r + dt*v
    collisions(r,v,radius,dt)
    # integreate a second time step to avoid a re-collision
    r = r + dt*v
    # reflection at boundaries
    test_at_0 = r<=0
    test_at_L = r>=L
    v[test_at_0]*=-1
    v[test_at_L]*=-1
    return r,v

@nb.njit( (nb.double[:,:], nb.double[:,:], nb.double,nb.double) )
def collisions(r,v,collision_radius,dt):
    """Resolve pairwise collisions"""
    N = len(r)
    collision_radius2=collision_radius*collision_radius
    for i in range(N-1):
        for j in range(i+1,N):
            dr2 = ((r[i]-r[j])**2).sum()
            if dr2<collision_radius2 :
                # collision rule for equal masses
                v[i] = v[i] - np.dot(v[i]-v[j],r[i]-r[j])/dr2*(r[i]-r[j])
                v[j] = v[j] - np.dot(v[j]-v[i],r[j]-r[i])/dr2*(r[j]-r[i])


def theory(ax,T,lo=0,hi=5):
    x= np.linspace(lo,hi,100)
    y =  x/T*np.exp(-x**2/(2*T))
    ax.plot(x,y)


# initalise the parameters
N = 625
L = 250
T = 1.0
dt = 0.5
#collision radius
radius = 0.75
bins = np.linspace(0,5,64)

# initalise the posiitons and the vewlocities
r,v = initialise(N,L, T)

fig,ax= plt.subplots(1,2,figsize=(6,3))
# plot points
pts, = ax[0].plot(r[:,0], r[:,1],'o',ms=1)
#plot histogram

normv = np.linalg.norm(v,axis=1)
hist = ax[1].hist(normv, bins=bins,density=True)
theory(ax[1],T)

ax[0].set_xlim(0,L)
ax[1].set_ylim(0,L)
ax[1].set_xlim(0,max(np.linalg.norm(v,axis=1)))
ax[1].set_ylim(0,1)

ax[0].axis('equal')

def animate(i,):
    global r,v, all_v #we want to modify the values of the two arrays **outside** the function
    r,v = evolve(r,v,L,dt,radius)
    print(i)
    pts.set_data(r[:,0],r[:,1])
    ax[1].cla()
    normv = np.linalg.norm(v,axis=1)
    ax[1].hist(normv, bins=bins,density=True)
    theory(ax[1],T)
    ax[0].axis('equal')
    ax[0].set_xlim(-1,L+1)
    ax[0].set_ylim(-1,L+1)
    ax[1].set_ylim(0,1)
    return pts

from matplotlib import animation
anim = animation.FuncAnimation(fig, animate,  interval=1)
plt.show()
# anim.to_jshtml()
# with open("anim.html","w") as fout:
#     fout.write(anim.to_jshtml())