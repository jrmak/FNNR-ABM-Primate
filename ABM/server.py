# !/usr/bin/python

# Running server.py runs the visualization; running graph.py shows the plots and writes the Excel file
# The visualization shows family agents as moving pixels; the graphs display the aging of monkey agents

from CanvasGridVisualization import CanvasGrid  #, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from model import *

# grid should be a square
width = Movement._readASCII(Movement, vegetation_file)[2]  # width = height in this case, even if ASCII file isn't
height = Movement._readASCII(Movement, vegetation_file)[2]

def movement_portrayal(agent):

    if agent is None:
        return

    portrayal = {"Shape": "rect", "Filled": "true", "w": 1, "h": 1, "Layer": 0}

# for elevation-based grid only
# portrayal["Color"] = str(type(agent).__name__.lower())

    if type(agent) is Bamboo:
        portrayal["Color"] = "Green"  # 0.8
    elif type(agent) is Coniferous:
        portrayal["Color"] = "DarkGreen"  # 1
    elif type(agent) is Broadleaf:
        portrayal["Color"] = "ForestGreen"  # 1
    elif type(agent) is Mixed:
        portrayal["Color"] = "LimeGreen"  # 1
    elif type(agent) is Lichen:
        portrayal["Color"] = "GreenYellow"  # 0.8
    elif type(agent) is Deciduous:
        portrayal["Color"] = "LightGreen"  # 1
    elif type(agent) is Shrublands:
        portrayal["Color"] = "YellowGreen"  # 0.8
    elif type(agent) is Clouds:
        portrayal["Color"] = "White"  # 0-1 random
    elif type(agent) is Farmland:
        portrayal["Color"] = "Dark Red"  # 0

    if type(agent) is Family and agent.family_type == 'traditional':
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "darkgoldenrod"
        portrayal["r"] = int(height / 30)
        portrayal["Layer"] = 1

    elif type(agent) is Family and agent.family_type == 'all_male':
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "tan"
        portrayal["r"] = int(height / 30)
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