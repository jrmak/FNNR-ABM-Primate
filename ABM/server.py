from mesa.visualization.modules import CanvasGrid  #, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from agents import Red, Orange, Yellow, Green, Blue, Purple, Black, Gray, Family
from model import Movement

# should be a square
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

    elif type(agent) is Family and agent.family_type == 'traditional':
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "white"
        portrayal["r"] = 3
        portrayal["Layer"] = 1

    elif type(agent) is Family and agent.family_type == 'all_male':
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "aqua"
        portrayal["r"] = 3
        portrayal["Layer"] = 1

    return portrayal

# monkey_movement_chart = {"Label": "Golden Monkey", "Color": "purple"}

agent_slider = UserSettableParameter('slider', "Number of Families", 5, 1, 20, 1)

canvas_width = 700
canvas_height = 700
canvas = CanvasGrid(movement_portrayal, width, height, canvas_width, canvas_height)
# chart_count = ChartModule([monkey_movement_chart])
model_params = {"number_of_families": agent_slider}

server = ModularServer(Movement, [canvas], "FNNR: an ABM of Guizhou Golden Monkey Movement", model_params)
        # deleted ', chart_count' after canvvas


server.launch()