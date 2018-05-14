from mesa.model import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random
from agents import Red, Orange, Yellow, Green, Blue, Purple, Black, Gray

masterdict = {'Red':[], 'Orange':[], 'Yellow':[], 'Green':[], 'Blue':[],
              'Purple':[], 'Black':[], 'Gray':[]}  # master dictionary
# keys: Black, Red, Yellow, Green land classifications, from least to most suitable
# values: grid coordinates that belong to that land type

class Movement(Model):

    number_of_black = 0
    number_of_red = 0
    number_of_orange = 0
    number_of_yellow = 0
    number_of_green = 0
    number_of_blue = 0
    number_of_purple = 0
    number_of_gray = 0

    def __init__(self, width=89, height=104, torus=False, seed=42,
                 strategy=None, num_monkey=10):
        # seed can be changed
        # torus = False means monkey movement can't 'wrap around' edges
        super().__init__(seed=seed)
        self.number_of_monkeys = num_monkey

        self.grid = MultiGrid(width, height, torus)

        self.schedule = RandomActivation(self)
        data = {"Monkey": lambda m: m.number_of_monkeys}
        self.datacollector = DataCollector(data)

        # generate land
        gridlist = self._readASCII('aggregated_dem.txt')

        self._populate(gridlist, Red)
        self._populate(gridlist, Orange)
        self._populate(gridlist, Yellow)
        self._populate(gridlist, Green)
        self._populate(gridlist, Blue)
        self._populate(gridlist, Purple)
        self._populate(gridlist, Black)
        self._populate(gridlist, Gray)

        # create monkey agents
        for i in range(self.number_of_monkeys):
            # pos = (random.randint(0,88), random.randint(0,103))
            superlist = masterdict['Red'] + masterdict['Orange'] + masterdict['Yellow'] + masterdict['Green'] \
                                                 + masterdict['Blue'] + masterdict['Purple'] + masterdict['Black']
            pos = random.choice(superlist)
            from agents import Monkey
            monkey = Monkey(i, self)
            self.grid.place_agent(monkey, pos)
            self.schedule.add(monkey)

    def step(self):
        # necessary; tells model to move forward
        self.schedule.step()
        self.datacollector.collect(self)

    def _readASCII(self, text):
        # reads in a text file that determines the environmental grid setup
        # currently unused; grid is randomly generated
        f = open(text, 'r')
        abody = f.readlines()[6:]  # ASCII file with a header
        f.close()
        abody = reversed(abody)
        cells = []  # list of cities
        for line in abody:
            cells.append(line.split(" "))
        # print(cells)
        return cells

    def _populate(self, grid, land_type):
        #places land tiles on the grid
        prefix = "number_of_{}"
        counter = 0
        while counter < land_type.seed * (self.grid.width * self.grid.height):
            #pos = self.grid.find_empty()
            # generate land randomly for now, but later, import Maxent output to grid
            for y in range(104):
                for x in range(89):
                    elev = int(round(float(grid[y][x])))  # .index()
                    pos = x, y
                    land = land_type(counter, self)
                    if land_type.min_elev < elev < land_type.max_elev:
                        self.grid.place_agent(land, pos)
                        self.schedule.add(land)
                        land_name = land_type.__name__.lower()
                        attr_name = prefix.format(land_name)
                        masterdict[land.__class__.__name__].append(pos)
                        val = getattr(self, attr_name)
                        val += 1
                        setattr(self, attr_name, val)
                        counter += 1

# matplotlib inline


import pandas as pd
from model import Movement
"""
import matplotlib.pyplot as plt

from tqdm import tqdm_notebook


def show(result, strategy):

    with plt.style.context("fivethirtyeight"):
        ax = result.plot(kind="line", figsize=(8,5))
        ax.set_xlabel("Run")
        ax.set_ylabel("Population size")
        ax.set_title("Evolution of monkey population with '{}' strategy".format(strategy))

# as the model develops, different strategies, or scenarios, will be used
"""

time = 250
def run(time, **kwargs):

    result = {"Monkey": []}
    model = Movement(**kwargs)

    # progress = tqdm_notebook(total = time)
    for t in range(time):

        result["Monkey"].append(model.number_of_monkeys)
        model.step()

        # progress.update()

    # progress.close()

    return pd.DataFrame(result)

strategy = "switch"
run(time, strategy = strategy)

# show(result, strategy)
