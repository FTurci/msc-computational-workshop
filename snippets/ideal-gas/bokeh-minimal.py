import random

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show

# number of particles

N = 100

# size of box 

L = 1

# mass of particles 

m = 1

# temperature

T = 1



# calculate initial velocities based on temperature

v = (T/m)**0.5

# initialize positions and velocities of particles

positions = [random.uniform(0, L) for i in range(N)]
velocities = [random.uniform(-v, v) for i in range(N)]

# create a figure and plot the positions of the particles

p = figure(title='Ideal Gas Particles in a Box', x_range=(0, L), y_range=(-v, v))
p.scatter(positions, velocities, size=5, alpha=0.5)

# update the positions and velocities of the particles after each collision

def update_particles():
    global positions, velocities
    for i in range(N):
        # check if particle is at edge of box and change velocity accordingly
        if positions[i] + velocities[i] > L:
            velocities[i] = -velocities[i]
        elif positions[i] + velocities[i] < 0:
            velocities[i] = -velocities[i]
        else:
            positions[i] += velocities[i]

    # update the plot with new positions and velocities
    p.scatter(positions, velocities, size=5, alpha=0.5)

# run update function every 100 milliseconds

curdoc().add_periodic_callback(update_particles, 100)

# show the plot

show(p)