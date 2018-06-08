# !/usr/bin/python

from mesa.model import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agents import *

masterdict = {'Red':[], 'Orange':[], 'Yellow':[], 'Green':[], 'Blue':[],
              'Purple':[], 'Black':[], 'Gray':[]}  # master dictionary for elevations and colors; unneeded with maxent
global_family_id_list = []
filename = 'aggregated_dem.txt'

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

    def __init__(self, width = 0, height = 0, torus = False,
                 time = 0, step_in_year = 0,
                 number_of_families = 10, number_of_monkeys = 0, monkey_birth_count = 0,
                 monkey_death_count = 0, monkey_id_count = 0):
        # torus = False means monkey movement can't 'wrap around' edges
        super().__init__()
        self.width = width
        self.height = height
        self.time = time
        self.step_in_year = step_in_year  # 1-73
        self.number_of_families = number_of_families
        self.number_of_monkeys = number_of_monkeys
        self.monkey_birth_count = monkey_birth_count
        self.monkey_death_count = monkey_death_count
        self.monkey_id_count = monkey_id_count

        # generate land
        gridlist = self._readASCII(filename)[0]
        width = self._readASCII(filename)[1]
        height = self._readASCII(filename)[2]

        self.grid = MultiGrid(width, height, torus)

        self.schedule = RandomActivation(self)

        self.datacollector = DataCollector({"Monkey": lambda m: m.number_of_monkeys})
        self.datacollector2 = DataCollector({"Monkey": lambda m: m.monkey_birth_count})
        self.datacollector3 = DataCollector({"Monkey": lambda m: m.monkey_death_count})
        self.datacollector4 = DataCollector({"Monkey": lambda m: demographic_structure_list})

        self._populate(gridlist, Red, width, height)
        self._populate(gridlist, Orange, width, height)
        self._populate(gridlist, Yellow, width, height)
        self._populate(gridlist, Green, width, height)
        self._populate(gridlist, Blue, width, height)
        self._populate(gridlist, Purple, width, height)
        self._populate(gridlist, Black, width, height)
        self._populate(gridlist, Gray, width, height)

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

        superlist = masterdict['Orange'] + masterdict['Yellow'] + masterdict['Green'] \
                    + masterdict['Blue']

        if self.time == 0:  # only do this on the first step
            for i in range(self.number_of_families):
                pos = random.choice(superlist)
                from agents import Family
                family_size = random.randint(25, 45)
                family_id = i
                list_of_family_members = []
                family_type = 'traditional'
                family = Family(family_id, self, pos, family_size, list_of_family_members, family_type)
                self.grid.place_agent(family, pos)
                self.schedule.add(family)
                global_family_id_list.append(family_id)

                for monkey_family_member in range(family_size):   # actually creates the amount of monkeys indicated earlier
                    id = self.number_of_monkeys + 1
                    gender = random.randint(0, 1)
                    if gender == 1:
                        female_list.append(id)
                        last_birth_interval = random.uniform(0, 3)
                    else:
                        male_maingroup_list.append(id)
                        last_birth_interval = -9999
                    mother = 0  # no parent check for first generation
                    death_flag = 0
                    choice = random.random()  # 0 - 1 float - age is determined randomly based on weights
                    if choice <= 0.11:
                        age = random.uniform(0, 1)  # the parameters indicate the age range
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
                        if gender == 1:
                            if id not in reproductive_female_list:
                                reproductive_female_list.append(id)
                        # starting representation of male defection
                        structure_convert = random.random()
                        if structure_convert > 0.25:
                            gender = 1
                            if id not in reproductive_female_list:
                                reproductive_female_list.append(id)
                    elif 0.96 < choice:
                        age = random.uniform(25, 30)
                        age_category = 5
                        demographic_structure_list[5] += 1
                        gender = 1
                    monkey = Monkey(id, self, pos, family_size, list_of_family_members, family_type,
                                    gender, age, age_category, family_id, last_birth_interval, mother,
                                    death_flag)

                    self.number_of_monkeys += 1
                    self.monkey_id_count += 1
                    self.schedule.add(monkey)
                    list_of_family_members.append(monkey.unique_id)


    def step(self):
        # necessary; tells model to move forward
        self.time += (1/73)
        self.step_in_year += 1
        if self.step_in_year == 73:
            self.step_in_year = 0  # start new year
        self.schedule.step()
        self.datacollector.collect(self)
        self.datacollector2.collect(self)
        self.datacollector3.collect(self)
        self.datacollector4.collect(self)

    def _readASCII(self, text):
        # reads in a text file that determines the environmental grid setup
        # currently unused; grid is randomly generated
        f = open(text, 'r')
        body = f.readlines()
        width = body[0][-4:]  # last 3 characters of line: 870
        height = body[1][-5:]
        #height = str(f.readlines()[0])[-4:]  # last 4 characters of line: 1000
        abody = body[6:]  # ASCII file with a header
        f.close()
        abody = reversed(abody)
        cells = []  # list of cities
        for line in abody:
            cells.append(line.split(" "))
        return [cells, int(width), int(height)]

    def _populate(self, grid, land_type, width, height):
        # places land tiles on the grid
        prefix = "number_of_{}"
        counter = 0  # sets agent ID
        for y in range(height):
            for x in range(width):
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