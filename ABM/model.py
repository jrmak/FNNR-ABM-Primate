# !/usr/bin/python

from mesa.model import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from monkeys import *
from environment import *
from humans import _readCSV, Human, Resource, human_demographic_structure_list
from land import Land
from fnnr_config_file import family_setting, human_setting, run_setting
import pickle


"""
Runs the main model.
It creates the agents and defines their attributes.
It also sets up the environmental grid using imported vegetation, elevation, and resource layers.
Then every step, it calls for agents to act.
"""

# NOTE: right now, the number of monkey families is set to 1 for model testing purposes (model runs faster).
# The actual number should be around 20. Change this in __init__() under Movement(Model).

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
                 number_of_families = family_setting, number_of_monkeys = 0, monkey_birth_count = 0,
                 monkey_death_count = 0, monkey_id_count = 0,
                 number_of_humans = 0, grid_type = human_setting, run_type = run_setting, human_id_count = 0):
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
        self.number_of_humans = number_of_humans
        self.grid_type = grid_type   # string 'with_humans' or 'without_humans'
        self.run_type = run_type  # string with 'normal_run' or 'first_run'
        self.human_id_count = human_id_count

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
                hh_id_match = int(line[0])
                resource_name = line[1]  # frequency is monthly; currently not-used
                frequency = float(line[2]) / 6 # divided by 6 for 5-day frequency, as opposed to 30-day (1 month)
                y = int(line[5])
                x = int(line[6])
                resource = Resource(_readCSV('hh_survey.csv')[1:].index(line),
                                    self, (x, y), hh_id_match, resource_name, frequency)
                self.grid.place_agent(resource, (int(x), int(y)))
                resource_dict.setdefault(hh_id_match, []).append(resource)
                if self.run_type == 'first_run':
                    self.saveLoad(resource_dict, 'resource_dict', 'save')

        # Creation of land parcels
        land_parcel_count = 0

        # individual land parcels in each household (non-gtgp and gtgp)
        for line in _readCSV('hh_land.csv')[2:]:  # exclude headers; for each household:
            age_1 = float(line[45])
            gender_1 = float(line[46])
            education_1 = float(line[47])
            hh_id = int(line[0])
            hh_size = 0  # calculate later

            total_rice = float(line[41])
            if total_rice in [-2, -3, -4]:
                total_rice = 0
            gtgp_rice = float(line[42])
            if gtgp_rice in [-2, -3, -4]:
                gtgp_rice = 0
            total_dry = float(line[43])
            if total_dry in [-2, -3, -4]:
                total_dry = 0
            gtgp_dry = float(line[44])
            if gtgp_dry in [-2, -3, -4]:
                gtgp_dry = 0
            # non_gtgp_area = float(total_rice) + float(total_dry) - float(gtgp_dry) - float(gtgp_rice)
            # gtgp_area = float(gtgp_dry) + float(gtgp_rice)

            for i in range(1,6):  # for each household, which has up to 5 each of possible non-GTGP and GTGP parcels:
                # non_gtgp_area = float(line[i + 47].replace("\"",""))
                # gtgp_area = float(line[i + 52].replace("\"",""))
                non_gtgp_area = float(total_rice) + float(total_dry) - float(gtgp_dry) - float(gtgp_rice)
                gtgp_area = float(gtgp_dry) + float(gtgp_rice)

                if gtgp_area in [-2, -3, -4]:
                    gtgp_area = 0
                if non_gtgp_area in [-2, -3, -4]:
                    non_gtgp_area = 0

                if non_gtgp_area > 0:
                    gtgp_enrolled = 0
                    non_gtgp_output = float(line[i].replace("\"",""))
                    pre_gtgp_output = 0
                    land_time = float(line[i + 25].replace("\"",""))  # non-gtgp travel time
                    plant_type = float(line[i + 10].replace("\"",""))  # non-gtgp plant type
                    land_type = float(line[i + 30].replace("\"",""))  # non-gtgp land type

                    if land_type not in [-2, -3, -4]:
                        land_parcel_count += 1
                        if non_gtgp_output in [-3, '-3', -4, '-4']:
                            non_gtgp_output = 0
                        if pre_gtgp_output in [-3, '-3', -4, '-4']:
                            pre_gtgp_output = 0
                        lp = Land(land_parcel_count, self, hh_id, gtgp_enrolled,
                                             age_1, gender_1, education_1,
                                             gtgp_dry, gtgp_rice, total_dry, total_rice,
                                             land_type, land_time, plant_type, non_gtgp_output,
                                             pre_gtgp_output, hh_size, non_gtgp_area, gtgp_area)
                        self.schedule.add(lp)

                if gtgp_area > 0:
                    gtgp_enrolled = 1
                    pre_gtgp_output = 0
                    non_gtgp_output = float(line[i].replace("\"",""))
                    land_time = float(line[i + 20].replace("\"",""))  # gtgp travel time
                    plant_type = float(line[i + 15].replace("\"",""))  # gtgp plant type
                    land_type = float(line[i + 35].replace("\"",""))  # gtgp land type
                    if land_type not in [-3, '-3', -4, '-4']:
                        land_parcel_count += 1
                        if non_gtgp_output in [-3, '-3', -4, '-4']:
                            non_gtgp_output = 0
                        if pre_gtgp_output in [-3, '-3', -4, '-4']:
                            pre_gtgp_output = 0
                        lp = Land(land_parcel_count, self, hh_id, gtgp_enrolled,
                                        age_1, gender_1, education_1,
                                        gtgp_dry, gtgp_rice, total_dry, total_rice,
                                        land_type, land_time, plant_type, non_gtgp_output,
                                        pre_gtgp_output, hh_size, non_gtgp_area, gtgp_area)
                        self.schedule.add(lp)

        # Creation of humans (brown dots in simulation)
        self.number_of_humans = 0
        self.human_id_count = 0
        line_counter = 0
        for line in _readCSV('hh_citizens.csv')[1:]:  # exclude headers; for each household:
            hh_id = int(line[0])
            line_counter += 1
            starting_position = (int(_readCSV('household.csv')[line_counter][4]), int(_readCSV('household.csv')[line_counter][3]))
            try:
                resource = random.choice(resource_dict[str(hh_id)])  # random resource point for human
                resource_position = resource.position
                resource_frequency = resource.frequency
                # to travel to, among the list of resource points reported by that household; may change later
                # to another randomly-picked resource
            except KeyError:
                resource_position = starting_position  # some households don't collect resources
                resource_frequency = 0
            hh_gender_list = line[1:10]
            hh_age_list = line[10:19]
            hh_education_list = line[19:28]
            hh_marriage_list = line[28:37]
            # creation of non-migrants
            for list_item in hh_age_list:
                if str(list_item) == '-3' or str(list_item) == '':
                    hh_age_list.remove(list_item)
            for x in range(len(hh_age_list) - 1):
                person = []
                for item in [hh_age_list, hh_gender_list, hh_education_list, hh_marriage_list]:
                    person.append(item[x])
                age = float(person[0])
                gender = int(person[1])
                education = int(person[2])
                marriage = int(person[3])
                if marriage != 1:
                    marriage = 6
                if 15 < age < 59:
                    work_status = 1
                elif 7 < age < 15:
                    work_status = 5
                else:
                    work_status = 6
                mig_years = 0
                migration_network = int(line[37])
                income_local_off_farm = int(line[57])
                resource_check = 0
                mig_remittances = int(line[48])
                past_hh_id = hh_id
                migration_status = 0
                death_rate = 0
                gtgp_part = 0
                non_gtgp_area = 0

                if str(gender) == '1':
                    if 0 < age <= 10:
                        age_category = 0
                    elif 10 < age <= 20:
                        age_category = 1
                    elif 20 < age <= 30:
                        age_category = 2
                    elif 30 < age <= 40:
                        age_category = 3
                    elif 40 < age <= 50:
                        age_category = 4
                    elif 50 < age <= 60:
                        age_category = 5
                    elif 60 < age <= 70:
                        age_category = 6
                    elif 70 < age <= 80:
                        age_category = 7
                    elif 80 < age <= 90:
                        age_category = 8
                    elif 90 < age:
                        age_category = 9
                elif str(gender) != "1":
                    if 0 < age <= 10:
                        age_category = 10
                    elif 10 < age <= 20:
                        age_category = 11
                    elif 20 < age <= 30:
                        age_category = 12
                    elif 30 < age <= 40:
                        age_category = 13
                    elif 40 < age <= 50:
                        age_category = 14
                    elif 50 < age <= 60:
                        age_category = 15
                    elif 60 < age <= 70:
                        age_category = 16
                    elif 70 < age <= 80:
                        age_category = 17
                    elif 80 < age <= 90:
                        age_category = 18
                    elif 90 < age:
                        age_category = 19
                children = 0
                if gender == 2:
                    if marriage == 1 and age < 45:
                        children = random.randint(0, 4)  # might already have kids
                    birth_plan_chance = random.random()
                    if birth_plan_chance < 0.03125:
                        birth_plan = 0
                    elif 0.03125 <= birth_plan_chance < 0.1875:
                        birth_plan = 1
                    elif 0.1875 <= birth_plan_chance < 0.5:
                        birth_plan = 2
                    elif 0.5 <= birth_plan_chance < 0.8125:
                        birth_plan = 3
                    elif 0.8125 <= birth_plan_chance < 0.96875:
                        birth_plan = 4
                    else:
                        birth_plan = 5
                elif gender != 2:
                    birth_plan = 0
                last_birth_time = random.uniform(0, 1)
                human_demographic_structure_list[age_category] += 1
                if str(person[0]) != '' and str(person[0]) != '-3' and str(person[1]) != '-3':  # sorts out all blanks
                    self.number_of_humans += 1
                    self.human_id_count += 1
                    human = Human(self.human_id_count, self, starting_position, hh_id, age,  # creates human
                                  resource_check, starting_position, resource_position,
                                  resource_frequency, gender, education, work_status,
                                  marriage, past_hh_id, mig_years, migration_status, gtgp_part,
                                  non_gtgp_area, migration_network, mig_remittances,
                                  income_local_off_farm, last_birth_time, death_rate, age_category, children,
                                  birth_plan)
                    if self.grid_type == 'with_humans':
                        self.grid.place_agent(human, starting_position)
                        self.schedule.add(human)

            # creation of migrant
            hh_migrants = line[38:43]  # age, gender, marriage, education of migrants
            if str(hh_migrants[0]) != '' and str(hh_migrants[0]) != '-3'\
                    and str(hh_migrants[1]) != '' and str(hh_migrants[1]) != '-3':  # if that household has any migrants, create migrant person
                self.number_of_humans += 1
                self.human_id_count += 1
                age = float(hh_migrants[0])
                gender = float(hh_migrants[1])
                education = int(hh_migrants[2])
                marriage = int(hh_migrants[3])
                mig_years = int(hh_migrants[4])
                if 15 < age < 59:
                    work_status = 1
                elif 7 < age < 15:
                    work_status = 5
                else:
                    work_status = 6
                past_hh_id = hh_id
                hh_id = 'Migrated'
                migration_status = 1
                migration_network = int(line[37])

                last_birth_time = random.uniform(0, 1)

                total_rice = float(line[43])
                gtgp_rice = float(line[44])
                total_dry = float(line[45])
                gtgp_dry = float(line[46])
                income_local_off_farm = float(line[57])
                if total_rice in ['-3', '-4', -3, None]:
                    total_rice = 0
                if total_dry in ['-3', '-4', -3, None]:
                    total_dry = 0
                if gtgp_dry in ['-3', '-4', -3, None]:
                    gtgp_dry = 0
                if gtgp_rice in ['-3', '-4', -3, None]:
                    gtgp_rice = 0
                if (gtgp_dry + gtgp_rice) != 0:
                    gtgp_part = 1
                else:
                    gtgp_part = 0
                non_gtgp_area = ((total_rice) + (total_dry)) \
                                - ((gtgp_dry) + (gtgp_rice))
                resource_check = 0
                mig_remittances = int(line[48])
                death_rate = 0
                if gender == 1:  # human male (monkeys are 0 and 1, humans are 1 and 2)
                    if 0 < age <= 10:
                        age_category = 0
                    elif 10 < age <= 20:
                        age_category = 1
                    elif 20 < age <= 30:
                        age_category = 2
                    elif 30 < age <= 40:
                        age_category = 3
                    elif 40 < age <= 50:
                        age_category = 4
                    elif 50 < age <= 60:
                        age_category = 5
                    elif 60 < age <= 70:
                        age_category = 6
                    elif 70 < age <= 80:
                        age_category = 7
                    elif 80 < age <= 90:
                        age_category = 8
                    elif 90 < age:
                        age_category = 9
                elif gender != 1:
                    if 0 < age <= 10:
                        age_category = 10
                    elif 10 < age <= 20:
                        age_category = 11
                    elif 20 < age <= 30:
                        age_category = 12
                    elif 30 < age <= 40:
                        age_category = 13
                    elif 40 < age <= 50:
                        age_category = 14
                    elif 50 < age <= 60:
                        age_category = 15
                    elif 60 < age <= 70:
                        age_category = 16
                    elif 70 < age <= 80:
                        age_category = 17
                    elif 80 < age <= 90:
                        age_category = 18
                    elif 90 < age:
                        age_category = 19
                children = 0
                if gender == 2:
                    if marriage == 1 and age < 45:
                        children = random.randint(0, 4)  # might already have kids
                    birth_plan_chance = random.random()
                    if birth_plan_chance < 0.03125:
                        birth_plan = 0
                    elif 0.03125 <= birth_plan_chance < 0.1875:
                        birth_plan = 1
                    elif 0.1875 <= birth_plan_chance < 0.5:
                        birth_plan = 2
                    elif 0.5 <= birth_plan_chance < 0.8125:
                        birth_plan = 3
                    elif 0.8125 <= birth_plan_chance < 0.96875:
                        birth_plan = 4
                    else:
                        birth_plan = 5
                elif gender != 2:
                    birth_plan = 0
                human_demographic_structure_list[age_category] += 1
                human = Human(self.human_id_count, self, starting_position, hh_id, age,  # creates human
                              resource_check, starting_position, resource_position,
                              resource_frequency, gender, education, work_status,
                              marriage, past_hh_id, mig_years, migration_status, gtgp_part, non_gtgp_area,
                              migration_network, mig_remittances, income_local_off_farm,
                              last_birth_time, death_rate, age_category, children, birth_plan)
                if self.grid_type == 'with_humans':
                    self.grid.place_agent(human, starting_position)
                    self.schedule.add(human)

        # Creation of monkey families (moving agents in the visualization)
        for i in range(self.number_of_families):  # the following code block creates families
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
                id = self.monkey_id_count
                gender = random.randint(0, 1)
                if gender == 1:  # gender = 1 is female, gender = 0 is male. this is different than with humans (1 or 2)
                    female_list.append(id)
                    last_birth_interval = random.uniform(0, 2)
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
                    if gender == 0:
                        if structure_convert < 0.6:
                            gender = 1
                            last_birth_interval = random.uniform(0, 3)
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
