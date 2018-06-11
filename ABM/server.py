# !/usr/bin/python

# Running server.py runs the visualization; running graph.py shows the plots and writes the Excel file
# The visualization shows family agents as moving pixels; the graphs display the aging of monkey agents

from CanvasGridVisualization import CanvasGrid  #, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from model import *

# grid should be a square
width = Movement._readASCII(Movement, filename)[2]  # width = height in this case, even if ASCII file isn't
height = Movement._readASCII(Movement, filename)[2]

def movement_portrayal(agent):

    if agent is None:
        return

    portrayal = {"Shape": "rect", "Filled": "true", "w": 1, "h": 1, "Layer": 0}

    if type(agent) is Red:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "red"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 0

    elif type(agent) is Orange:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "orange"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 0

    elif type(agent) is Yellow:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "yellow"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 0

    elif type(agent) is Green:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "green"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 0

    elif type(agent) is Blue:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "blue"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 0

    elif type(agent) is Purple:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "purple"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 0

    elif type(agent) is Black:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "black"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 0

    elif type(agent) is Gray:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "gray"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 0

    elif type(agent) is Family and agent.family_type == 'traditional':
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "white"
        portrayal["r"] = int(height / 25)
        portrayal["Layer"] = 1

    elif type(agent) is Family and agent.family_type == 'all_male':
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "aqua"
        portrayal["r"] = int(height / 25)
        portrayal["Layer"] = 1

    return portrayal

# monkey_movement_chart = {"Label": "Golden Monkey", "Color": "purple"}

agent_slider = UserSettableParameter('slider', "Number of Families", 10, 1, 20, 1)
# note: add more later

canvas_width = 700
canvas_height = 700

canvas = CanvasGrid(movement_portrayal, width, height, canvas_width, canvas_height)
# chart_count = ChartModule([monkey_movement_chart])
model_params = {"number_of_families": agent_slider}

server = ModularServer(Movement, [canvas], "FNNR: an ABM of Guizhou Golden Monkey Movement", model_params)
        # deleted ', chart_count' after canvas


server.launch()