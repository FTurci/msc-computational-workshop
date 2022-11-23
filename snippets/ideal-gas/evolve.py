def evolve(r,v,dt):
    """
    Time evolution of the particle positions.

    The particles are inside a box [[0,L],[0,L]]"""

    rnew = r +v*dt
    # inter-particle collisions
    collisions(r,v,collision_radius2)
    # wall collisions
    test0,testL= r<=0, r>=L
    r[test0]*=-1
    v[test0]*=-1
    r[testL]=2*L-r[testL]
    v[testL]*=-1
    return r,v
