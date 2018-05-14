from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from agents import Red, Orange, Yellow, Green, Blue, Purple, Black, Gray, Monkey
from model import Movement

# should match the same width and height as in model.py
width = 104
height = 104

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

    elif type(agent) is Monkey:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "white"
        portrayal["r"] = 3
        portrayal["Layer"] = 1

    return portrayal

# monkey_movement_chart = {"Label": "Golden Monkey", "Color": "purple"}

agent_slider = UserSettableParameter('slider', "Number of Agents", 10, 10, 30, 1)

canvas = CanvasGrid(movement_portrayal, width, height)
# chart_count = ChartModule([monkey_movement_chart])
model_params = {"strategy": "switch", "num_monkey": agent_slider}

server = ModularServer(Movement, [canvas], "Movement", model_params) # deleted ', chart_count' after canvvas
server.launch()