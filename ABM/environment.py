# this module is similar to symbology -> classification in ArcMap

from mesa.agent import Agent

class Environment(Agent):

    def __init__(self, unique_id, model, pos=None):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass
        # will add seasonal variations to environment later, if vegetation data is imported

# environmental pixels for Maxent-value-based grid; each shade represents a suitability category
# Maxent values range from 0-1, with a number closer to 1 representing higher suitability for monkeys

class Shade1(Environment):

    lower_bound = 0.000170539
    upper_bound = 0.040741642

class Shade2(Environment):

    lower_bound = 0.040741642
    upper_bound = 0.132026623

class Shade3(Environment):

    lower_bound = 0.132026623
    upper_bound = 0.257120857

class Shade4(Environment):

    lower_bound = 0.257120857
    upper_bound = 0.392357867

class Shade5(Environment):

    lower_bound = 0.392357867
    upper_bound = 0.527594877

class Shade6(Environment):

    lower_bound = 0.527594877
    upper_bound = 0.662831886

class Shade7(Environment):

    lower_bound = 0.662831886
    upper_bound = 1

class Shade8(Environment):

    lower_bound = -10000
    upper_bound = -9998

# environmental pixels for elevation-based grid; each color represents an elevation category (in meters)

class Red(Environment):

    lower_bound = 1899
    upper_bound = 3000

class Orange(Environment):

    lower_bound = 1699
    upper_bound = 1900

class Yellow(Environment):

    lower_bound = 1499
    upper_bound = 1700

class Green(Environment):

    lower_bound = 1299
    upper_bound = 1500

class Blue(Environment):

    lower_bound = 1099
    upper_bound = 1300

class Purple(Environment):

    lower_bound = 899
    upper_bound = 1100

class Black(Environment):

    lower_bound = 0
    upper_bound = 900

class Gray(Environment):

    lower_bound = -10000
    upper_bound = -9998


# vegetation

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


# human pixels

class Household(Environment):
    pass

class Farm(Environment):
    pass