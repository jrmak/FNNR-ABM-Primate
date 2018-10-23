# !/usr/bin/python

from mesa.model import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from monkeys import *
from environment import *
from humans import _readCSV, Human, Resource
from resource_dict import resource_dict
import pickle


"""
Runs the main model.
It creates the agents and defines their attributes.
It also sets up the environmental grid using imported vegetation, elevation, and resource layers.
Then every step, it calls for agents to act.
"""

global_family_id_list = []
household_list = [2, 3, 5, 6, 8, 9, 11, 14, 15, 16, 17, 19, 22, 25, 27, 30, 31, 32, 34, 35, 36, 39, 41, 42, 43, 46,
                 47, 48, 49, 53, 54, 55, 57, 63, 64, 71, 72, 85, 100, 101, 102, 103, 104, 108, 113, 118, 120, 121,
                 123, 128, 129, 131, 132, 134, 135, 136, 137, 138, 140, 141, 142, 143, 144, 145, 146, 148, 149, 150,
                 151, 153, 154, 155, 157, 159, 161, 163, 165, 166, 167, 169]
vegetation_file = 'agg_veg60.txt'  # change these filenames to another file in the same directory as needed
elevation_file = 'agg_dem_87100.txt'
household_file = 'hh_ascii400.txt'
farm_file = 'farm_ascii300.txt'
pes_file = 'pes_ascii200.txt'
forest_file = 'forest_ascii200.txt'
# If any of the above .txt input environmental files are changed, change the run_type of the model to 'first_run',
# then back to 'normal_run' on any subsequent runs

masterdict = {}
resource_dict = {}

class Movement(Model):

    def __init__(self, width = 0, height = 0, torus = False,
                 time = 0, step_in_year = 0,
                 number_of_families = 1, number_of_monkeys = 0, monkey_birth_count = 0,
                 monkey_death_count = 0, monkey_id_count = 0, grid_type = 'with_humans', run_type = 'normal_run'):
        # change the # of families here for graph.py, but use server.py to change # of families in the movement model
        # torus = False means monkey movement can't 'wrap around' edges
        super().__init__()
        self.width = width
        self.height = height
        self.time = time # time increases by 1/73 (decimal) each step
        self.step_in_year = step_in_year  # 1-73; each step is 5 days, and 5 * 73 = 365 days in a year
        self.number_of_families = number_of_families
        self.number_of_monkeys = number_of_monkeys  # total, not in each family
        self.monkey_birth_count = monkey_birth_count
        self.monkey_death_count = monkey_death_count
        self.monkey_id_count = monkey_id_count
        self.grid_type = grid_type   # string 'with_humans' or 'without_humans'
        self.run_type = run_type  # string with 'normal_run' or 'first_run'

        # width = self._readASCII(vegetation_file)[1] # width as listed at the beginning of the ASCII file
        # height = self._readASCII(vegetation_file)[2] # height as listed at the beginning of the ASCII file
        width = 85
        height = 100

        self.grid = MultiGrid(width, height, torus)  # creates environmental grid, sets schedule
        # MultiGrid is a Mesa function that sets up the grid; options are between SingleGrid and MultiGrid
        # MultiGrid allows you to put multiple layers on the grid

        self.schedule = RandomActivation(self)  # Mesa: Random vs. Staged Activation
        # similar to NetLogo's Ask Agents - determines order (or lack of) in which each agents act

        empty_masterdict = {'Outside_FNNR': [], 'Elevation_Out_of_Bound': [], 'Household': [], 'PES': [], 'Farm': [],
                            'Forest': [], 'Bamboo': [], 'Coniferous': [], 'Broadleaf': [], 'Mixed': [], 'Lichen': [],
                            'Deciduous': [], 'Shrublands': [], 'Clouds': [], 'Farmland': []}

        # generate land
        if self.run_type == 'first_run':
            gridlist = self._readASCII(vegetation_file)[0]  # list of all coordinate values; see readASCII function below
            gridlist2 = self._readASCII(elevation_file)[0]  # list of all elevation values
            gridlist3 = self._readASCII(household_file)[0]  # list of all household coordinate values
            gridlist4 = self._readASCII(pes_file)[0]  # list of all PES coordinate values
            gridlist5 = self._readASCII(farm_file)[0]  # list of all farm coordinate values
            gridlist6 = self._readASCII(forest_file)[0]  # list of all managed forest coordinate values
            # The '_populate' function below builds the environmental grid.
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
            self.saveLoad(self.grid, 'grid_veg', 'save')
            self.saveLoad(self.schedule, 'schedule_veg', 'save')

        # Pickling below
        load_dict = {}  # placeholder for model parameters, leave this here even though it does nothing

        if self.grid_type == 'with_humans':
            empty_masterdict = self.saveLoad(load_dict, 'masterdict_veg', 'load')
            self.grid = self.saveLoad(self.grid, 'grid_veg', 'load')

        if self.grid_type == 'without_humans':
            empty_masterdict = self.saveLoad(load_dict, 'masterdict_without_humans', 'load')
            self.grid = self.saveLoad(load_dict, 'grid_without_humans', 'load')
        masterdict = empty_masterdict

        startinglist = masterdict['Broadleaf'] + masterdict['Mixed'] + masterdict['Deciduous']
        # Agents will start out in high-probability areas.
        for coordinate in masterdict['Elevation_Out_of_Bound'] + masterdict['Household'] + masterdict['PES']    \
            + masterdict['Farm'] + masterdict['Forest']:
                if coordinate in startinglist:
                    startinglist.remove(coordinate)  # the original starting list includes areas that monkeys
                                                     # cannot start in

        # Creation of resources (yellow dots in simulation)
        # These include Fuelwood, Herbs, Bamboo, etc., but right now resource type and frequency are not used
        if self.grid_type == 'with_humans':
            for line in _readCSV('hh_survey.csv')[1:]:  # see 'hh_survey.csv'
                hh_id_match = line[0]
                resource_name = line[1]  # frequency is monthly; currently not-used
                frequency = float(line[2]) / 6 # divided by 6 for 5-day frequency, as opposed to 30-day (1 month)
                y = int(line[5])
                x = int(line[6])
                resource = Resource(_readCSV('hh_survey.csv')[1:].index(line),
                                    self, (x, y), hh_id_match, resource_name, frequency)
                self.grid.place_agent(resource, (int(x), int(y)))
                resource_dict.setdefault(hh_id_match, []).append(resource)

        # Creation of humans (brown dots in simulation)
        human_id = 0
        for line in _readCSV('household.csv')[1:]:
            hh_id = line[0]  # household ID for that human
            starting_position = (int(line[4]), int(line[3]))
            try:
                resource = random.choice(resource_dict[hh_id])  # random resource point for human
                resource_position = resource.position
                resource_frequency = resource.frequency
                # to travel to, among the list of resource points reported by that household; may change later
                # to another randomly-picked resource
            except KeyError:
                resource_position = starting_position  # some households don't collect resources
            human_id += 1
            resource_check = 0
            age = random.randint(15, 59)
            gender = random.choice([1, 2])
            if age > 19 and random.random() > 0.60:
                marriage = 1
            else:
                marriage = 0
            human = Human(human_id, self, starting_position, hh_id, age,
                          resource_check, starting_position, resource_position,
                          resource_frequency, gender, education, work_status,
                          marriage, past_hh_id, migration_status)
            if self.grid_type == 'with_humans':
                self.grid.place_agent(human, starting_position)
                self.schedule.add(human)

        # Creation of monkey families (moving agents in the visualization)
        for i in range(self.number_of_families):  # the following code block create families
            starting_position = random.choice(startinglist)
            saved_position = starting_position
            from families import Family
            family_size = random.randint(25, 45)  # sets family size for each group--random integer
            family_id = i
            list_of_family_members = []
            family_type = 'traditional'  # as opposed to an all-male subgroup
            split_flag = 0  # binary: 1 means its members start migrating out to a new family
            family = Family(family_id, self, starting_position, family_size, list_of_family_members, family_type,
                            saved_position, split_flag)
            self.grid.place_agent(family, starting_position)
            self.schedule.add(family)
            global_family_id_list.append(family_id)

            # Creation of individual monkeys (not in the visualization submodel, but for the demographic submodel)
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
                    age = random.uniform(3, 7)  # are randomly aged between
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
                        last_birth_interval = random.uniform(0, 3.25)
                        if id not in reproductive_female_list:
                            reproductive_female_list.append(id)
                elif 0.96 < choice:  # 4% of starting monkey population
                    age = random.uniform(25, 30)  # are randomly aged between
                    age_category = 5  # ages 25-30
                    demographic_structure_list[5] += 1
                    gender = 1
                monkey = Monkey(id, self, gender, age, age_category, family, last_birth_interval, mother
                                )
                self.number_of_monkeys += 1
                self.monkey_id_count += 1
                list_of_family_members.append(monkey.unique_id)
                self.schedule.add(monkey)

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
                land_grid_coordinate = x, y
                land = land_type(counter, self)
                if land_type.__name__ == 'Elevation_Out_of_Bound':
                    if (value < land_type.lower_bound or value > land_type.upper_bound) and value != -9999:
                        # if elevation is not 1000-2200, but is within the bounds of the FNNR, mark as 'elevation OOB'
                        self.grid.place_agent(land, land_grid_coordinate)
                        masterdict[land.__class__.__name__].append(land_grid_coordinate)
                        counter += 1
                elif land_type.__name__ == 'Forest':
                    if land_type.type == value:
                        self.grid.place_agent(land, land_grid_coordinate)
                        masterdict[land.__class__.__name__].append(land_grid_coordinate)
                        counter += 1
                elif land_type.__name__ == 'PES':
                    if land_type.type == value:
                        self.grid.place_agent(land, land_grid_coordinate)
                        masterdict[land.__class__.__name__].append(land_grid_coordinate)
                        counter += 1
                elif land_type.__name__ == 'Farm':
                    if land_type.type == value:
                        self.grid.place_agent(land, land_grid_coordinate)
                        masterdict[land.__class__.__name__].append(land_grid_coordinate)
                        counter += 1
                elif land_type.__name__ == 'Household':
                    if land_type.type == value:
                        self.grid.place_agent(land, land_grid_coordinate)
                        masterdict[land.__class__.__name__].append(land_grid_coordinate)
                        counter += 1
                else:  # vegetation background
                    if land_type.type == value:
                        self.grid.place_agent(land, land_grid_coordinate)
                        masterdict[land.__class__.__name__].append(land_grid_coordinate)
                        counter += 1

    def saveLoad(self, pickled_file, name, option):
        """ This function pickles an object, which lets it be loaded easily later.
        I haven't figured out how to utilize pickle to pickle class objects (if possible). """
        if option == "save":
            f = open(name, 'wb')
            pickle.dump(pickled_file, f)
            f.close()
        elif option == "load":
            f = open(name, 'rb')
            new_pickled_file = pickle.load(f)
            return new_pickled_file
        else:
            print('Invalid saveLoad option')
