from bokeh.io import show
from bokeh.models import ColumnDataSource
from bokeh.palettes import Viridis3
from bokeh.plotting import figure, curdoc
from bokeh.layouts import row

import numpy as np
from matplotlib import animation
import numba as nb

# PHYSICS - mostly identical to matplotlib version
##########################################################################################
def initialise(N,L,T):

    return r,v


def evolve(r,v,L,dt,radius):

    return r,v

@nb.njit( (nb.double[:,:], nb.double[:,:], nb.double,nb.double) )
def collisions(r,v,collision_radius,dt):
   


def theory(T,lo=0,hi=5):
    x= np.linspace(lo,hi,100)
    y =  x/T*np.exp(-x**2/(2*T))
    return x,y
##########################################################################################


# Parameters
##########################################################################################
N = 625
L = 250
T = 1.0
dt = 0.5
radius = 0.75
bins = np.linspace(0.01,5,64)
r,v = initialise(N,L, T)
########################################################################################## 


### Bokeh code ###

# DATASOURCES
##########################################################################################
# Create the ColumnDataSource for the particle positions and velocities
source = ColumnDataSource(data=dict(x=r[:,0], y=r[:,1], vx=v[:,0], vy=v[:,1]))
# Create datasource for histogram
pdf, edges = np.histogram(np.linalg.norm(v,axis=1),bins,density=True)
print(pdf)
histo = ColumnDataSource(data=dict(left=edges[:-1], right=edges[1:], pdf = pdf ))
##########################################################################################

# FIGURES
##########################################################################################
# Create the figure for the particle positions
particles = figure(
    width=400, #pixels
    height=400,
    x_range=(0, L),
    y_range=(0, L))

distribution = figure(width=400,height=400,y_range=(0,1))
##########################################################################################

# INITIALISE PLOTS
##########################################################################################
# Plot the particles as circles
particles.circle(x='x', y='y', source=source, color=Viridis3[0], radius=radius)
# Create the plot for the distribution
# plot theoretical curve
xt,yt = theory(T)
distribution.line(x=xt,y=yt)
# barplot for teh histogram
distribution.quad(top='pdf', bottom=0, left='left', right='right',
         fill_color="skyblue", line_color="white",source=histo, fill_alpha=0.5)
##########################################################################################

#LAYOUT
##########################################################################################
# Create the layout
layout = row(particles,distribution)
##########################################################################################

#ANIMATION
##########################################################################################
def animate():
    global r,v
    r,v = evolve(r,v,L,dt,radius)
    pdf, edges = np.histogram(np.linalg.norm(v,axis=1),bins,density=True)
    # Update sources 
    source.data = dict(x=r[:,0], y=r[:,1], vx=v[:,0], vy=v[:,1])
    histo.data = dict(left=edges[:-1],right=edges[1:], pdf = pdf )

# Add a callback to update the data periodically
curdoc().add_periodic_callback(animate, 1)
curdoc().add_root(layout)
##########################################################################################