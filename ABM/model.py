# !/usr/bin/python

from mesa.model import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from environment import *
from agents import *
import pickle

global_family_id_list = []
vegetation_file = 'agg_veg60.txt'  # change this filename to another file in the same directory as needed
elevation_file = 'agg_dem_87100.txt'
household_file = 'hh_ascii400.txt'
farm_file = 'farm_ascii300.txt'
pes_file = 'pes_ascii200.txt'
forest_file = 'forest_ascii200.txt'

masterdict = {}

class Movement(Model):

    def __init__(self, width = 0, height = 0, torus = False,
                 time = 0, step_in_year = 0,
                 number_of_families = 10, number_of_monkeys = 0, monkey_birth_count = 0,
                 monkey_death_count = 0, monkey_id_count = 0):
        # change the # of families here for graph.py, but use server.py to change # of families in movement model
        # torus = False means monkey movement can't 'wrap around' edges
        super().__init__()
        self.width = width
        self.height = height
        self.time = time
        self.step_in_year = step_in_year  # 1-73; each step is 5 days, and 5 * 73 = 365 days in a year
        self.number_of_families = number_of_families
        self.number_of_monkeys = number_of_monkeys  # total, not in each family
        self.monkey_birth_count = monkey_birth_count
        self.monkey_death_count = monkey_death_count
        self.monkey_id_count = monkey_id_count

        # generate land
        gridlist = self._readASCII(vegetation_file)[0]  # list of all coordinate values; see readASCII function below
        gridlist2 = self._readASCII(elevation_file)[0]  # list of all coordinate values; see readASCII function below
        gridlist3 = self._readASCII(household_file)[0]  # list of all coordinate values; see readASCII function below
        gridlist4 = self._readASCII(pes_file)[0]  # list of all coordinate values; see readASCII function below
        gridlist5 = self._readASCII(farm_file)[0]  # list of all coordinate values; see readASCII function below
        gridlist6 = self._readASCII(forest_file)[0]  # list of all coordinate values; see readASCII function below

        # width = self._readASCII(vegetation_file)[1] + 5 # width as listed at the beginning of the ASCII file
        # height = self._readASCII(vegetation_file)[2] + 5 # height as listed at the beginning of the ASCII file
        width = 85
        height = 100

        self.starting_grid = MultiGrid(width, height, torus)  # creates environmental grid, sets schedule

        self.schedule = RandomActivation(self)  # Mesa: Random vs. Staged Activation
        # similar to NetLogo's Ask Agents - determines order (or lack of) in which each agents act

        empty_masterdict = {'Bamboo': [], 'Coniferous': [], 'Broadleaf': [], 'Mixed': [], 'Lichen': [],
                            'Deciduous': [], 'Shrublands': [], 'Clouds': [], 'Farmland': [], 'Outside_FNNR': [],
                            'Elevation_Out_of_Bound': [], 'Household': [], 'PES': [], 'Farm': [], 'Forest': []}

        """
        for x in [Elevation_Out_of_Bound]:
            self._populate(empty_masterdict, gridlist2, x, width, height)
        for x in [Household]:
            self._populate(empty_masterdict, gridlist3, x, width, height)
        for x in [PES]:
            self._populate(empty_masterdict, gridlist4, x, width, height)
        for x in [Farm]:
            self._populate(empty_masterdict, gridlist5, x, width, height)
        for x in [Forest]:
            self._populate(empty_masterdict, gridlist6, x, width, height)
        for x in [Bamboo, Coniferous, Broadleaf, Mixed, Lichen, Deciduous, Shrublands, Clouds, Farmland, Outside_FNNR]:
            self._populate(empty_masterdict, gridlist, x, width, height)
        self.saveLoad(empty_masterdict, 'masterdict_veg', 'save')
        self.saveLoad(self.starting_grid, 'grid_veg', 'save')
        self.saveLoad(self.schedule, 'schedule_veg', 'save')
        """
        """ Lines 62-76 are commented out using Lines 61 and 77, but they must be re-enabled if a new environmental grid
         is put in. Otherwise, the model will load a 'pickled', or saved, environment from the disk. """



        load_dict = {}  # placeholder for model parameters, leave this here even though it does nothing
        empty_masterdict = self.saveLoad(load_dict, 'masterdict_veg', 'load')
        self.starting_grid = self.saveLoad(self.starting_grid, 'grid_veg', 'load')
        self.schedule = self.saveLoad(self.schedule, 'schedule_veg', 'load')
        # when loading, the first parameter actually isn't used

        masterdict = empty_masterdict
        self.grid = self.starting_grid

        startinglist = masterdict['Broadleaf'] + masterdict['Mixed'] + masterdict['Deciduous']
        for coordinate in masterdict['Elevation_Out_of_Bound'] + masterdict['Household'] + masterdict['PES']    \
                + masterdict['Farm'] + masterdict['Forest']:
            if coordinate in startinglist:
                startinglist.remove(coordinate)

        for i in range(self.number_of_families):  # the following code block create families
            pos = random.choice(startinglist)
            from agents import Family
            family_size = random.randint(25, 45)  # sets family size for each group
            family_id = i
            list_of_family_members = []
            family_type = 'traditional'  # as opposed to an all-male subgroup
            family = Family(family_id, self, pos, family_size, list_of_family_members, family_type)
            self.grid.place_agent(family, pos)
            self.schedule.add(family)
            global_family_id_list.append(family_id)

            for monkey_family_member in range(family_size):   # creates the amount of monkeys indicated earlier
                id = self.number_of_monkeys + 1
                gender = random.randint(0, 1)
                if gender == 1:  # gender = 1 is female, gender = 0 is male
                    female_list.append(id)
                    last_birth_interval = random.uniform(0, 3)
                else:
                    male_maingroup_list.append(id)  # as opposed to the all-male subgroup
                    last_birth_interval = -9999  # males will never give birth
                mother = 0  # no parent check for first generation
                death_flag = 0
                choice = random.random()  # 0 - 1 float - age is determined randomly based on weights
                if choice <= 0.11:  # 11% of starting monkey population
                    age = random.uniform(0, 1)  # are randomly aged befween
                    age_category = 0  # ages 0-1
                    demographic_structure_list[0] += 1
                elif 0.11 < choice <= 0.27:  # 16% of starting monkey population
                    age = random.uniform(1, 3)  # are randomly aged befween
                    age_category = 1  # ages 1-3
                    demographic_structure_list[1] += 1
                elif 0.27 < choice <= 0.42:  # 15% of starting monkey population
                    age = random.uniform(3, 7)  # are randomly aged befween
                    age_category = 2  # ages 3-7
                    demographic_structure_list[2] += 1
                elif 0.42 < choice <= 0.62:  # 11% of starting monkey population
                    age = random.uniform(7, 10)  # are randomly aged befween
                    age_category = 3  # ages 7-10
                    demographic_structure_list[3] += 1
                elif 0.62 < choice <= 0.96:  # 34% of starting monkey population
                    age = random.uniform(10, 25)  # are randomly aged befween
                    age_category = 4  # ages 10-25
                    demographic_structure_list[4] += 1
                    if gender == 1:
                        if id not in reproductive_female_list:
                            reproductive_female_list.append(id)
                    # starting representation of male defection/gender ratio
                    structure_convert = random.random()
                    if structure_convert > 0.25:
                        gender = 1  # 75% of those aged 10-25 are female
                        if id not in reproductive_female_list:
                            reproductive_female_list.append(id)
                elif 0.96 < choice:  # 4% of starting monkey population
                    age = random.uniform(25, 30)  # are randomly aged between
                    age_category = 5  # ages 25-30
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
        if self.step_in_year > 73:
            self.step_in_year = 1  # start new year
        self.schedule.step()

    def _readASCII(self, text):
        # reads in a text file that determines the environmental grid setup
        f = open(text, 'r')
        body = f.readlines()
        width = body[0][-4:]  # last 4 characters of line that contains the 'width' value
        height = body[1][-5:]
        abody = body[6:]  # ASCII file with a header
        f.close()
        abody = reversed(abody)
        cells = []
        for line in abody:
            cells.append(line.split(" "))
        return [cells, int(width), int(height)]


    def _populate(self, masterdict, grid, land_type, width, height):
        # places land tiles on the grid - connects color/land cover category with ASCII file values
        counter = 0  # sets agent ID - not currently used
        for y in range(height):  # for each pixel,
            for x in range(width):
                value = float(grid[y][x])  # value from the ASCII file for that coordinate/pixel, e.g. 1550 elevation
                pos = x, y
                land = land_type(counter, self)
                if land_type.__name__ == 'Elevation_Out_of_Bound':
                    if (value < land_type.lower_bound or value > land_type.upper_bound) and value != -9999:
                        # if elevation is not 1000-2200, but is within the bounds of the FNNR, mark as 'elevation OOB'
                        self.starting_grid.place_agent(land, pos)
                        self.schedule.add(land)
                        masterdict[land.__class__.__name__].append(pos)
                        counter += 1
                elif land_type.__name__ == 'Household' or 'PES' or 'Farm' or 'Forest'   \
                        and self.model.grid.is_cell_empty == True:
                    if land_type.type == value:
                        self.starting_grid.place_agent(land, pos)
                        self.schedule.add(land)
                        masterdict[land.__class__.__name__].append(pos)
                        counter += 1
                else:  # vegetation background
                    if land_type.type == value and self.model.grid.is_cell_empty == True:
                        self.starting_grid.place_agent(land, pos)
                        self.schedule.add(land)
                        masterdict[land.__class__.__name__].append(pos)
                        counter += 1

    def saveLoad(self, grid_dict, name, option):
        if option == "save":
            f = open(name, 'wb')
            pickle.dump(grid_dict, f)
            f.close()
            'data saved'
        elif option == "load":
            f = open(name, 'rb')
            new_grid_dict = pickle.load(f)
            return new_grid_dict
        else:
            print('Invalid saveLoad option')
