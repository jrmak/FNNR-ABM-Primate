# !/usr/bin/python

# Running server.py runs the visualization; running graph.py shows the plots and writes the Excel file
# The visualization shows family agents as moving pixels; the graphs display the aging of monkey agents

from CanvasGridVisualization import CanvasGrid  #, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import *
from environment import *

# grid should be a square
width = Movement._readASCII(Movement, vegetation_file)[2]  # width = height in this case, even if ASCII file isn't
height = Movement._readASCII(Movement, vegetation_file)[2]  # index [2] returns 3rd argument of _readASCII's output

def movement_portrayal(agent):

    portrayal = {"Shape": "rect", "Filled": "true", "w": 1, "h": 1, "Layer": 0}

# for elevation-based grid only
# portrayal["Color"] = str(type(agent).__name__.lower())

    if type(agent) is Resource:
        portrayal["Color"] = "Yellow"
        portrayal["Shape"] = "circle"
        portrayal["r"] = int(height / 30)
        portrayal["Layer"] = 6

    elif type(agent) is Household:
        portrayal["Color"] = "#fafafa"  # 0
        portrayal["Layer"] = 5
    elif type(agent) is PES:
        portrayal["Color"] = "#a8a8a8"  # 0.2
        portrayal["Layer"] = 4
    elif type(agent) is Farm:
        portrayal["Color"] = "#545454"  # 0.05
        portrayal["Layer"] = 3
    elif type(agent) is Forest:
        portrayal["Color"] = "#000000"  # 0.2?
        portrayal["Layer"] = 2

    elif type(agent) is Elevation_Out_of_Bound:
        portrayal["Color"] = "tan"  # 0
        portrayal["Layer"] = 1

    elif type(agent) is Bamboo:
        portrayal["Color"] = "#BEF75C"  # 0.8
    elif type(agent) is Coniferous:
        portrayal["Color"] = "#8BED39"  # 1
    elif type(agent) is Broadleaf:
        portrayal["Color"] = "#38E009"  # 1
    elif type(agent) is Mixed:
        portrayal["Color"] = "#3EC74E"  # 1
    elif type(agent) is Lichen:
        portrayal["Color"] = "#37AB7E"  # 0.8
    elif type(agent) is Deciduous:
        portrayal["Color"] = "#1A93AB"  # 1
    elif type(agent) is Shrublands:
        portrayal["Color"] = "#22639C"  # 0.8
    elif type(agent) is Clouds:
        portrayal["Color"] = "#1D269C"  # 0-1 random
    elif type(agent) is Farmland:
        portrayal["Color"] = "#0C1078"  # 0
    elif type(agent) is Outside_FNNR:
        portrayal["Color"] = "#ffffff"  # 0

    if type(agent) is Human:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "brown"
        portrayal["r"] = int(height / 30)  # radius is based on height of landscape so that it remains the same total
        portrayal["Layer"] = 8  # size, no matter what the resolution (individual pixel size) of the landscape is

    if type(agent) is Family and agent.family_type == 'traditional':
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "darkgoldenrod"
        portrayal["r"] = int(height / 30)
        portrayal["Layer"] = 8

    elif type(agent) is Family and agent.family_type == 'all_male':
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "tan"
        portrayal["r"] = int(height / 30)
        portrayal["Layer"] = 8

    return portrayal

canvas_width = 700
canvas_height = 700

class MapLegend(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        # image created on MS Paint and uploaded to internet, but also featured in this folder for reference
        return ("<center><img src = 'http://i63.tinypic.com/21o30yg.png'></center>" + "<br>"
                + "<br><br></h3>")

text0 = MapLegend()
canvas = CanvasGrid(movement_portrayal, width, height, canvas_width, canvas_height)
# chart_count = ChartModule([monkey_movement_chart])

agent_slider = UserSettableParameter('slider', "Number of Families", 20, 1, 30, 1)
humans_choice = UserSettableParameter('choice', "Status of Humans in Reserve", 'with_humans',
                                      choices = ['with_humans', 'without_humans'])

model_params = {"number_of_families": agent_slider, "grid_type": humans_choice}

server = ModularServer(Movement, [canvas, text0], "FNNR: an ABM of Guizhou Golden Monkey Movement", model_params)
        # deleted ', chart_count' after canvas

server.launch()