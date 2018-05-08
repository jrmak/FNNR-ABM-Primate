from mesa.model import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random
from agents import Yellow, Red, Green, Black

masterdict = {}  # master dictionary
# keys: Black, Red, Yellow, Green land classifications, from least to most suitable
# values: grid coordinates that belong to that land type

class Movement(Model):

    number_of_black = 0
    number_of_red = 0
    number_of_yellow = 0
    number_of_green = 0

    def __init__(self, width=29, height=32, torus=False, seed=42,
                 strategy=None, num_monkey=0):
        # 29 x 32 because that's the size of my Maxent output
        # seed can be changed
        # torus = False means monkey movement can't 'wrap around' edges
        super().__init__(seed=seed)
        self.number_of_monkeys = num_monkey

        self.grid = MultiGrid(width, height, torus)

        self.schedule = RandomActivation(self)
        data = {"Monkey": lambda m: m.number_of_monkeys}
        self.datacollector = DataCollector(data)

        # generate land
        self._populate(Yellow)
        self._populate(Green)
        self._populate(Red)
        self._populate(Black)

        # create monkey agents
        for i in range(self.number_of_monkeys):
            pos = (random.randint(0,28), random.randint(0,31))
            from agents import Monkey
            monkey = Monkey(i, self)
            self.grid.place_agent(monkey, pos)
            self.schedule.add(monkey)

    def step(self):
        # necessary; tells model to move forward
        self.schedule.step()
        self.datacollector.collect(self)

    def readASCII(text):
        # reads in a text file that determines the environmental grid setup
        # currently unused; grid is randomly generated
        f = open(text, 'r')
        abody = f.readlines()  # [6:] if this was an actual ASCII file with a header
        f.close()
        cells = []  # list of cities
        for line in abody:
            cells.append(line.split(" "))
        # print(cells)
        return cells

    # gridlist = readASCII('maxent.txt')
    # Later, might import Maxent output to environmental grid

    def _populate(self, land_type):
        #places land tiles on the grid
        prefix = "number_of_{}"
        counter = 0
        while counter < land_type.seed * (self.grid.width * self.grid.height):
            pos = self.grid.find_empty()
            # generate land randomly for now, but later, import Maxent output to grid
            # for x, y in range(32), range(29)
            # pos = gridlist[x-1][y-1].index()
            # #  pos = x, y
            land = land_type(counter, self)
            self.grid.place_agent(land, pos)
            self.schedule.add(land)
            land_name = land_type.__name__.lower()
            attr_name = prefix.format(land_name)
            val = getattr(self, attr_name)
            val += 1
            setattr(self, attr_name, val)
            counter += 1

# matplotlib inline

import pandas as pd
import matplotlib.pyplot as plt

from tqdm import tqdm_notebook
from model import Movement

time = 250

def show(result, strategy):

    with plt.style.context("fivethirtyeight"):
        ax = result.plot(kind="line", figsize=(8,5))
        ax.set_xlabel("Run")
        ax.set_ylabel("Population size")
        ax.set_title("Evolution of monkey population with '{}' strategy".format(strategy))

# as the model develops, different strategies, or scenarios, will be used

def run(time, **kwargs):

    result = {"Monkey": []}
    model = Movement(**kwargs)

    progress = tqdm_notebook(total = time)
    for t in range(time):

        result["Monkey"].append(model.number_of_monkeys)
        model.step()

        progress.update()

    progress.close()

    return pd.DataFrame(result)

strategy = "switch"
result = run(time, strategy = strategy)

show(result, strategy)