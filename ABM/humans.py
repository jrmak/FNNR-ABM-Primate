"""
This document imports human data from the Excel file containing Shuang's survey results and determines behavior for human agents.
"""

from mesa.agent import Agent
import random
import math

single_male_list = []
married_male_list = []
human_avoidance_list = []  # sets coordinate positions the monkeys should not step on, because humans are on it.
# Neighboring cells of human activity may also be added to this list.
initial_migrants_list = []
household_migrants_list = []
out_migrants_list = []
re_migrants_list = []
birth_list = []
death_list = []
head_of_household_list = []

num_labor_list = [0] * 95  # 94 households, 94 + 1 indices (+ 1 is for the 0th index)
household_income_list = [0] * 95
income_local_off_farm_list = [0] * 95
household_remittances_list = [0] * 95
gtgp_part_list = [0] * 95

def _readCSV(text):
    # reads in a .csv file.
    # separate from _readASCII in model.py, which reads .asc files.
    cells = []
    f = open(text, 'r')
    body = f.readlines()
    for line in body:
        cells.append(line.split(","))
    return cells

class Human(Agent):
    # the pixel that represents each group of monkeys with the same family id.
    # it moves on the visualization grid, unlike individual monkey agents.
    # it is currently not important in the demographic model, just the visualization model.
    def __init__(self, unique_id, model, current_position, hh_id, age, resource_check,
                 home_position, resource_position, resource_frequency, gender, education, work_status,
                 marriage, past_hh_id, mig_years, migration_status, total_rice, total_dry, gtgp_rice, gtgp_dry,
                 migration_network, mig_remittances, income_local_off_farm, num_labor, hh_size,
                 last_birth_time):
        super().__init__(unique_id, model)
        self.current_position = current_position
        self.hh_id = hh_id
        self.age = age
        self.resource_check = resource_check
        self.home_position = home_position
        self.resource_position = resource_position
        self.resource_frequency = resource_frequency
        self.gender = gender
        self.education = education
        self.work_status = work_status
        self.marriage = marriage
        self.past_hh_id = past_hh_id
        self.mig_years = mig_years
        self.migration_status = migration_status
        self.total_rice = total_rice
        self.total_dry = total_dry
        self.gtgp_rice = gtgp_rice
        self.gtgp_dry = gtgp_dry
        self.migration_network = migration_network
        self.mig_remittances = mig_remittances
        self.income_local_off_farm = income_local_off_farm
        self.num_labor = num_labor
        self.hh_size = hh_size
        self.last_birth_time = last_birth_time

        # update code soon:
        # immi_marriage_rate = 0.03  # pre-set from pseudo-code

        self.total_rice = total_rice
        if self.total_rice in ['-3', '-4', -3, None]:
            self.total_rice = 0
        self.total_dry = total_dry
        if self.total_dry in ['-3', '-4', -3, None]:
            self.total_dry = 0
        self.gtgp_dry = gtgp_dry
        if self.gtgp_dry in ['-3', '-4', -3, None]:
            self.gtgp_dry = 0
        self.gtgp_rice = gtgp_rice
        if self.gtgp_rice in ['-3', '-4', -3, None]:
            self.gtgp_rice = 0

        if self.gtgp_rice != 0 or self.gtgp_dry != 0:
            gtgp_part_list.append(self.hh_id)

        # make sure hh_ids and individuals are matched


    def step(self):
        # human aging/demographic behavior

        if self.model.step == 0:
            pass
            # populate num_labor_list

        self.age_check()
        self.death_check()
        self.migration_check()
        self.re_migration_check()
        self.marriage_check()
        self.birth_check()
        self.age += 1 / 73
        self.last_birth_time += 1 / 73

        if int(self.age) > 20 and self.gender == 1 and self.marriage == 0\
                and self.unique_id not in single_male_list:
            single_male_list.append([self.unique_id, self.hh_id])

        if self.unique_id in married_male_list:
            if self.unique_id in single_male_list:
                single_male_list.remove(self.unique_id)
            self.marriage = 1

        random.shuffle(single_male_list)

        # human movement and resource collection behavior
        if len(human_avoidance_list) > 94 * 9:  # 94 households, 8 neighbors, so 94 * 9 instances per step
            del human_avoidance_list[:]  # reset the list every step (once it hits a length of 94 * 9)
        load_dict = {}
        masterdict = self.model.saveLoad(load_dict, 'masterdict_veg', 'load')
        current_position = list(self.current_position)  # changes tuple into a list to edit; content remains the same
        if self.current_position not in masterdict['Forest'] + masterdict['Household'] + masterdict['PES']  \
            + masterdict['Farm'] + masterdict['Elevation_Out_of_Bound'] + human_avoidance_list:
            human_avoidance_list.append(self.current_position)
        human_neighboring_grids = self.model.grid.get_neighborhood(self.current_position, True, False)
        for human_neighbor in human_neighboring_grids:
             human_avoidance_list.append(human_neighbor)
        if self.resource_check == 0: # if the human does not have the resource, head towards it
            self.move_to_point(self.resource_position, self.resource_frequency)
        else:
            self.move_to_point(tuple(self.home_position), self.resource_frequency)  # else, head home
            if current_position[0] == list(self.home_position)[0] and current_position[1] == list(self.home_position)[1]:
                # if you are back home, go out and collect resources again if frequency permits
                self.resource_check = 0
                try:
                    from model import resource_dict
                    resource = random.choice(resource_dict[self.hh_id])  # randomly choose resource
                    self.resource_frequency = resource.frequency
                    self.resource_position = resource.position
                    # print(self.resource_position, self.current_position, self.home_position)
                except KeyError:
                    pass  # this "pass" occurs because
                    # not all households collect resources

    def age_check(self):
        """Check working and education age, as well as age-based death rates"""
        # check working status
        if 15 <= float(self.age) < 59:
            self.workstatus = 1
        else:
            self.workstatus = 0

        if 15 <= float(self.age) < 59:
            head_of_household_list.append(self.unique_id)

        # check education status; measured in years of education
        if 7 <= int(self.age) <= 19:
            if random.random() > 0.1:
                self.education += 1
                # most adults in the FNNR did not get a full 12-13 years of education
        elif 19 < float(self.age) < 23 and self.migration_status == 1:
            if random.random() < 0.5:
                self.education += 1  # went to college and got further education
                # this is rare; in the household list, a few received beyond 12 years of education

        # check age-based death rates
        if self.age > 65:
            self.death_rate = 0.00000095  # 5-day death rate
        # The average death rate in China is 7.3 per 1,000 people/year (Google).
        # However, death rates should be higher for the elderly, or else the population structure will skew.
        # I set death rates for those over age 65 to be 15% per year--0.9985 yearly survival rate.
        # The survival rate for each 5-day step is compounded 73 times, so x^73 = 0.09985.
        # x is the 5-day survival rate, and 1 - x is the 5-day death rate.
        else:
            self.death_rate = 0.000047
        # I wanted people to have an 80% chance of reaching age 65.
        # If a 'check' is every 5 days, 73 * 65 = 4,745 checks.
        # x^4745 = 0.8; the 5-day survival rate is 0.999953, and 1 - x is the 5-day death rate.

        # These rates are changeable later. However, they produce a stable population.

    def birth_check(self):
        """Small chance of giving birth every step if married and under 50"""
        if self.gender == 2 and self.age < 55 and self.marriage == 1:
            if random.random() < 0.00017:  # 0.0121, or 1.21%, is the yearly birth rate.
                # This makes the birth rate for every 5 days (73 'checks' a year) 0.00017%,
                # because 1 - 0.0121 = 0.9879, 0.99983 ^73 = 0.9879, and 1 - 0.99983 = 0.0001
                if self.last_birth_time > 2:  # 2 years is the set birth interval; can modify
                    self.last_birth_time = 0  # reset counter
                    last = self.model.human_id_count
                    # build more attributes
                    mig_remittances = self.mig_remittances
                    income_local_off_farm = self.income_local_off_farm
                    num_labor = 0
                    last_birth_time = 0
                    ind = Human(last + 1, self.model, self.current_position, self.hh_id, age, self.resource_check,
                                          self.home_position, self.resource_position, self.resource_frequency, gender,
                                          education, work_status, marriage, past_hh_id, mig_years, migration_status,
                                          total_rice, total_dry, gtgp_rice, gtgp_dry, migration_network,
                                          mig_remittances, income_local_off_farm, num_labor, hh_size,
                                          last_birth_time)
                    ind.age = 0
                    ind.gender = choice([1, 2])
                    ind.education = 6
                    ind.work_status = 0
                    ind.marriage = 0
                    ind.migration_status = 0
                    self.model.schedule.add(ind)
                    self.model.human_id_count += 1

    def death_check(self):
        """Small chance of dying every step; increases if over 65"""
        if random.random() < self.death_rate:
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
        if self.unique_id in head_of_household_list:
            head_of_household_list.remove(self.unique_id)
        if self.unique_id in num_labor_list:
            num_labor_list.remove(self.unique_id)

    def marriage_check(self):
        if int(self.age) > 20 and int(self.gender) == 2 and int(self.marriage) == 0\
                and self.migration_status == 0:
                if random.random() < 0.00096:
                    # marriage late is set low because this is a 5-day rate
                    # the yearly marriage rate is 0.007, or 0.7%
                    self.marriage = 1
                    self.past_hh_id = self.hh_id
                    self.hh_id = single_male_list[0][1]  # male's hh_id
        if self.unique_id in married_male_list:
            self.marriage = 1
            # takes the first male off the single_male_list, which is shuffled every step
            married_male_list.append(single_male_list[0][0])
            single_male_list.remove(single_male_list[0])

    def migration_check(self):
        """Describes out-migration process and probability"""
        self.mig_flag = 0

        non_gtgp_area = (float(self.total_rice) + float(self.total_dry)) \
                        - (float(self.gtgp_dry) + float(self.gtgp_rice))

        if num_labor_list[self.hh_id] != 0:
            non_gtgp_land_per_labor = non_gtgp_area / num_labor_list[self.hh_id]
        else:
            non_gtgp_land_per_labor = 0

        remittance = random.normalvariate(1200, 16000)
        if remittance < 0:
            remittance = 0
        self.remittance = float(remittance)
        if self.hh_id in gtgp_part_list:
            gtgp_part = 1
        else:
            gtgp_part = 0
        if self.hh_id not in household_migrants_list and self.unique_id not in out_migrants_list:
            # print(income_local_off_farm, self.migration_network, self.gtgp_part, farm_work, self.remittance,
            #      non_gtgp_land_per_labor, self.education, self.remittance, farm_work)
            prob = math.exp(2.07 - 0.00015 * float(self.income_local_off_farm) + 0.67 * float(self.num_labor)
                       + 4.36 * float(self.migration_network) - 0.58 * float(non_gtgp_land_per_labor)
                       + 0.27 * float(gtgp_part) - 0.13 * float(self.age) + 0.07 * float(self.gender)
                       + 0.17 * float(self.education) + 0.88 * float(self.marriage) +
                       1.39 * float(self.work_status) + 0.001 * float(self.remittance))
            mig_prob = prob / (prob + 1)
            if random.random() < mig_prob and self.hh_size >= 2:  # out-migration occurs
                household_income_list[self.hh_id] = (household_income_list[self.hh_id]
                                                              + self.remittance)
                self.hh_size -= 1
                self.past_hh_id = self.hh_id
                self.workstatus = 4

                if 15 < self.age < 65 and self.num_labor > 1:
                    self.mig_flag = 1
                    num_labor_list[self.hh_id] -= 1
                    out_migrants_list.append(self.unique_id)
                    if self.unique_id in re_migrants_list:
                        re_migrants_list.remove(self.unique_id)

                self.hh_id = 'Migrated'

    def re_migration_check(self):
        """Describes re-migration process and probability following out-migration"""
        if self.hh_id == 'Migrated':
            self.mig_years += 1

            prob = exp(-1.2 + 0.06 * float(self.age) - 0.08 * self.mig_years)
            re_mig_prob = prob / (prob + 1)
            if random() < re_mig_prob:
                self.migration_status = 0
                self.hh_id = self.past_hh_id
                self.workstatus = 1
                self.mig_years = 0
                self.hh_size += 1
                hh_size_list[self.hh_id] += 1

                if 15 < int(self.age) < 65:
                    self.num_labor += 1
                    num_labor_list[self.hh_id] += 1

                self.mig_remittances = return_values(self.hh_row,
                                     'mig_remittances')  # remittances of initial migrant
                household_income_list[self.hh_id] = household_income_list[self.hh_id] \
                                                         - float(self.mig_remittances)
                household_remittances_list[self.hh_id] = household_remittances_list[self.hh_id]
                if self.unique_id in out_migrants_list:
                    out_migrants_list.remove(self.unique_id)
                    - float(self.mig_remittances)
            else:
                household_income_list[self.hh_id] = household_income_list[self.hh_id] \
                                                         - self.remittance
                household_remittances_list[self.hh_id] = household_remittances_list[self.hh_id] \
                                                                      - self.remittance


    def move_to(self, pos):
        if pos != None:
            self.model.grid.move_agent(self, pos)

    def move_to_point(self, destination, frequency):
        """Moves human agent to assigned point at the frequency speed"""
        # index 0 represents x, index 1 represents y
        if frequency > 1:
            current_position = list(self.current_position)
            if current_position[0] < destination[0]:
                current_position[0] = current_position[0] + int(frequency)
            elif current_position[0] == destination[0]:
                pass  # don't move
            else:
                current_position[0] = current_position[0] - int(frequency)
            if current_position[1] < destination[1]:
                current_position[1] = current_position[1] + int(frequency)
            elif current_position[1] == destination[1]:
                pass
            else:
                current_position[1] = current_position[1] - int(frequency)
            current_position = tuple(current_position)
            self.move_to(current_position)
            self.current_position = current_position
            if current_position[0] == destination[0] and current_position[1] == destination[1]:
                self.resource_check = 1
        else:
            self.resource_frequency += self.resource_frequency / 6

class Resource(Agent):
    # Resources are fuelwood, mushrooms, herbs, etc. (see 'type') that humans collect.
    # They are considered agents in case a future version of the model makes them limited (accounts for land change).
    def __init__(self, unique_id, model, position, hh_id_match, type, frequency):
        super().__init__(unique_id, model)
        self.position = position
        self.hh_id_match = hh_id_match
        self.type = type
        self.frequency = frequency

    def step(self):
        pass
