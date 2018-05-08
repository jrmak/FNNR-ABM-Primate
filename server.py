from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from agents import Red, Yellow, Green, Black, Monkey
from model import Movement

# should match the same width and height as in model.py
width = 29
height = 32

def movement_portrayal(agent):

    if agent is None:
        return

    portrayal = {"Shape": "rect", "Filled": "true", "w": 0.8, "h": 0.8, "Layer": 0}

    if type(agent) is Red:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "red"
        portrayal["r"] = 1
        portrayal["Layer"] = 0

    elif type(agent) is Green:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "green"
        portrayal["r"] = 1
        portrayal["Layer"] = 0

    elif type(agent) is Yellow:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "yellow"
        portrayal["r"] = 1
        portrayal["Layer"] = 0

    elif type(agent) is Black:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "black"
        portrayal["r"] = 1
        portrayal["Layer"] = 0

    elif type(agent) is Monkey:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "blue"
        portrayal["r"] = 1
        portrayal["Layer"] = 1

    return portrayal

monkey_movement_chart = {"Label": "Golden Monkey", "Color": "purple"}

agent_slider = UserSettableParameter('slider', "Number of Agents", 1, 2, 10, 1)

canvas = CanvasGrid(movement_portrayal, width, height)
chart_count = ChartModule([monkey_movement_chart])
model_params = {"strategy": "switch", "num_monkey": agent_slider}

server = ModularServer(Movement, [canvas, chart_count], "Movement", model_params)
server.launch()