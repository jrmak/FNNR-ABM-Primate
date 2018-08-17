# !/usr/bin/python

"""
Graphs a line "walk" from a list of traveled coordinates.
Note: Only works when number_of_families = 1 is set in model.py's Model parameters--otherwise, lines will
inaccurately connect separate agents' movements together
"""

from random import choice
from matplotlib import pyplot as plt
import numpy as np

def readCSVInt(text):
    # reads in a .csv file.
    # separate from _readASCII in model.py, which reads .asc files.
    cells = []
    f = open(text, 'r')
    body = f.readlines()
    for line in body[2:]:
        cells.append(line.strip("\n").replace(" ","").split(","))
    return cells

tuple_excel_walk = []
excel_walk = readCSVInt('abm_export_density_plot_single1.csv')
for x in excel_walk:
    tuple_excel_walk.append(tuple(x))

new_walk = tuple_excel_walk
intx = []
inty = []
for coordinate in new_walk:
    intx.append(int(coordinate[0]))
    inty.append(int(coordinate[1]))
plt.plot(np.array(intx), np.array(inty))
plt.title('Random Walk - 5 Agents, 1 Year, 1 Trial, With Humans')
plt.xlim(0, 85)
plt.ylim(0, 100)
plt.xticks(np.arange(0, 85, 10))
plt.yticks(np.arange(0, 100, 10))
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
