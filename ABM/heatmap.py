# !/usr/bin/python

# Creates a heatmap visualization of positions that the family-pixel agents move to
# Shown with other graphs when graph.py is run

import numpy
import matplotlib.pyplot as plt
from agents import moved_list

xlist = []
ylist = []

# Create data
for item in moved_list:
    if type(item) is tuple:
        x = item[0]
        xlist.append(x)
        y = item[1]
        ylist.append(y)
    else:
        pass

# Create heatmap
print(len(xlist), len(ylist))
heatmap, xedges, yedges = numpy.histogram2d(xlist, ylist, bins=50)
extent = [0, 100, 0, 100]

# Plot heatmap
plt.clf()
plt.title('Cumulative Monkey Position Heatmap')
plt.ylabel('y')
plt.xlabel('x')
plt.imshow(heatmap, extent=extent, origin = 'lower')
