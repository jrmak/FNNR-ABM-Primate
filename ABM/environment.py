# this module is similar to symbology -> classification in ArcMap

from mesa.agent import Agent

class Environment(Agent):

    def __init__(self, unique_id, model, pos = None, elevation = None):
        super().__init__(unique_id, model)
        self.pos = pos
        self.elevation = elevation
    def step(self):
        pass

class Bamboo(Environment):
    type = 1


class Coniferous(Environment):
    type = 2


class Broadleaf(Environment):
    type = 3


class Mixed(Environment):
    type = 4


class Lichen(Environment):
    type = 5


class Deciduous(Environment):
    type = 6


class Shrublands(Environment):
    type = 7


class Clouds(Environment):
    type = 8


class Farmland(Environment):
    type = 9


class Outside_FNNR(Environment):
    type = -9999


# human pixels

class Household(Environment):
    type = 10

class Farm(Environment):
    type = 11

class PES(Environment):
    type = 12

class Forest(Environment):
    type = 13

# elevation

class Elevation_Out_of_Bound(Environment):
    lower_bound = 1000
    upper_bound = 2200

