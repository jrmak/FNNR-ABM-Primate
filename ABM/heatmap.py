# !/usr/bin/python

# Creates a heatmap visualization of positions that the family-pixel agents move to
# Shown with other graphs when graph.py is run

import numpy
import matplotlib.pyplot as plt
from agents import moved_list

xlist = []
ylist = []
count_x = {}
count_y = {}
new_x = {}
new_y = {}

# Create data
for item in moved_list:
    if type(item) is tuple:
        x = item[0]
        count_x[x] = count_x.get(x, 0) + 1
        xlist.append(x)
        y = item[1]
        count_y[y] = count_y.get(y, 0) + 1
        ylist.append(y)

for key, value in sorted(count_x.items()):
     new_x.setdefault(key, []).append(value)

for key, value in sorted(count_y.items()):
     new_y.setdefault(key, []).append(value)

# Create heatmap
heatmap, xedges, yedges = numpy.histogram2d(xlist, ylist, bins = 40)
extent = [0, 100, 0, 100]

print(new_x)
print(new_y)

# Plot heatmap
plt.clf()
plt.title('Cumulative Monkey Position Heatmap')
plt.ylabel('y')
plt.xlabel('x')
plt.imshow(heatmap, extent=extent, origin = 'lower')
