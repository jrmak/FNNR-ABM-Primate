from mesa.model import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agents import *

masterdict = {'Red':[], 'Orange':[], 'Yellow':[], 'Green':[], 'Blue':[],
              'Purple':[], 'Black':[], 'Gray':[]}  # master dictionary
# dictionary keys: land suitability (or elevation, etc.) categorized by color
# dictionary values: grid coordinates that belong to that land type


class Movement(Model):

    number_of_black = 0
    number_of_red = 0
    number_of_orange = 0
    number_of_yellow = 0
    number_of_green = 0
    number_of_blue = 0
    number_of_purple = 0
    number_of_gray = 0

    def __init__(self, width = 89, height = 104, torus = False,
                 time = 0, number_of_families = 10, number_of_monkeys = 0, monkey_birth_count = 0,
                 monkey_death_count = 0):
        # seed can be changed
        # torus = False means monkey movement can't 'wrap around' edges
        super().__init__()
        self.time = time
        self.number_of_families = number_of_families
        self.number_of_monkeys = number_of_monkeys
        self.monkey_birth_count = monkey_birth_count
        self.monkey_death_count = monkey_death_count

        self.grid = MultiGrid(width, height, torus)

        self.schedule = RandomActivation(self)

        self.datacollector = DataCollector({"Monkey": lambda m: m.number_of_monkeys})
        self.datacollector2 = DataCollector({"Monkey": lambda m: m.monkey_birth_count})
        self.datacollector3 = DataCollector({"Monkey": lambda m: m.monkey_death_count})
        self.datacollector4 = DataCollector({"Monkey": lambda m: demographic_structure_list})

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

        """
        # create monkey agents - early version, each pixel = 1 monkey, no families
        for i in range(self.number_of_monkeys):
            # pos = (random.randint(0,88), random.randint(0,103))
            superlist = masterdict['Red'] + masterdict['Orange'] + masterdict['Yellow'] + masterdict['Green'] \
                                                 + masterdict['Blue'] + masterdict['Purple']
            pos = random.choice(superlist)
            from agents import Monkey
            monkey = Monkey(i, self)
            self.grid.place_agent(monkey, pos)
            self.schedule.add(monkey)
        """

        # create monkey agents - each pixel represents a family group of 25-45 monkeys

        superlist = masterdict['Red'] + masterdict['Orange'] + masterdict['Yellow'] + masterdict['Green'] \
                    + masterdict['Blue'] + masterdict['Purple']

        if self.time == 0:  # only do this on the first step
            for i in range(self.number_of_families):
                pos = random.choice(superlist)
                from agents import Family
                family_size = random.randint(25, 45)
                family_id = i
                family = Family(family_id, self, pos, family_size)
                self.grid.place_agent(family, pos)
                self.schedule.add(family)

                from agents import Monkey
                for monkey_id in range(family_size):
                    gender = random.randint(0, 1)
                    if gender == 1:
                        last_birth_interval = random.randint(0, 3)
                    else:
                        last_birth_interval = 0
                    mother = 0  # no parent check for first generation
                    choice = random.random()  # 0 - 1 float
                    if choice <= 0.11:
                        age = random.uniform(0, 1)
                        age_category = 0
                        demographic_structure_list[0] += 1
                    elif 0.11 < choice <= 0.27:
                        age = random.uniform(1, 3)
                        age_category = 1
                        demographic_structure_list[1] += 1
                    elif 0.27 < choice <= 0.42:
                        age = random.uniform(3, 7)
                        age_category = 2
                        demographic_structure_list[2] += 1
                    elif 0.42 < choice <= 0.62:
                        age = random.uniform(7, 10)
                        age_category = 3
                        demographic_structure_list[3] += 1
                    elif 0.62 < choice <= 0.96:
                        age = random.uniform(10, 25)
                        age_category = 4
                        demographic_structure_list[4] += 1
                        # starting representation of male defection
                        structure_convert = random.random()
                        if structure_convert > 0.25:
                            gender = 1
                    elif 0.96 < choice:
                        age = random.uniform(25, 30)
                        age_category = 5
                        demographic_structure_list[5] += 1
                        gender = 1

                    monkey = Monkey(monkey_id, self, pos, family_size, gender, age, age_category, family_id,
                                    last_birth_interval, mother)

                    self.number_of_monkeys += 1
                    self.schedule.add(monkey)


    def step(self):
        # necessary; tells model to move forward
        self.time += (1/73)
        self.schedule.step()
        self.datacollector.collect(self)
        self.datacollector2.collect(self)
        self.datacollector3.collect(self)
        self.datacollector4.collect(self)

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
        return cells

    def _populate(self, grid, land_type):
        # places land tiles on the grid
        prefix = "number_of_{}"
        counter = 0  # sets agent ID
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


model = Movement()
time = 3
for t in range(time):
    model.step()