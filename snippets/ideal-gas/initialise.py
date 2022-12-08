def initialise(N,L,T):
    r = np.random.uniform(0,L,size=(N,2))
    v = np.random.uniform(-1,1,r.shape)
    # scale the velocity so that the kinetic energy reflects the equipartition theorem
    random_T = (0.5*(v**2).mean())*2
    scale = T/random_T
    v *= np.sqrt(scale)
    return r,v
