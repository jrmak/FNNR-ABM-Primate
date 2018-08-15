# !/usr/bin/python

"""
Graphs a line "walk" from a list of traveled coordinates.
Code from http://nbviewer.jupyter.org/gist/boarpig/92228a4d3e4653ccd0cd
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

def walk():
    place = [0, 0]
    directions = ((-1, 1), (0, 1), (1, 1),
             (-1, 0)        , (1, 0),
             (-1, -1), (0, -1), (1, -1))
    points = [(0, 0)]
    for i in range(100):
        direction = choice(directions)
        place[0] += direction[0]
        place[1] += direction[1]
        points.append(place[:])
    return points

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
