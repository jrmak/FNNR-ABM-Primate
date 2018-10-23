"""
This document imports human data from the Excel file containing Shuang's survey results and determines behavior for human agents.
"""

from mesa.agent import Agent
import random

single_male_list = []
married_male_list
human_avoidance_list = []  # sets coordinate positions the monkeys should not step on, because humans are on it.
# Neighboring cells of human activity may also be added to this list.

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
                 marriage, past_hh_id, migration_status):
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
        self.marriage_status = marriage
        self.past_hh_id = past_hh_id
        self.migration_status = migration_status

        self.birth_rate = 0.00017  # 0.0121, or 1.21%, is the yearly birth rate.
        # This makes the birth rate for every 5 days (73 'checks' a year) 0.00017%,
        # because 1 - 0.0121 = 0.9879, 0.99983 ^73 = 0.9879, and 1 - 0.99983 = 0.00017
        self.birth_interval = 2
        self.birth_flag = 0
        self.death_flag = 0
        self.marriage_rate = 0.007
        self.marriage_flag = 0
        self.match_prob = 0.05  # pre-set from pseudo-code
        self.immi_marriage_rate = 0.03  # pre-set from pseudo-code

        # make sure hh_ids and individuals are matched


    def step(self):
        # human aging/demographic behavior
        self.age_check()
        self.death_check()
        # self.migration_check()
        # self.remigration_check
        self.marriage_check()
        self.marriage_match()
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

        shuffle(single_male_list)

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
        if self.age < 15:
            self.workstatus = 0
        elif 15 <= self.age < 59:
            self.workstatus = 1
        elif self.age >= 59:
            self.workstatus = 0

        if self.migration_status == 1:
            self.workstatus = 2  # 2 is not higher than 1 in this case; just a third value

        # check education status; measured in years of education
        if 7 <= int(self.age) <= 19:
            if random.random() > 0.1:
                self.education += 1
                # most adults in the FNNR did not get a full 12-13 years of education
        elif 19 < self.age < 23 and self.migration_status == 1:
            self.education += 1  # went to college and got further education

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
            if random() < self.birth_rate: # create new human agent
                if self.last_birth_time > float(self.birth_interval):
                    self.last_birth_time = 0  # reset counter
                    last = self.model.human_id_count
                    ind = IndividualAgent(last + 1, self.model, self.current_position, self.hh_id, age, self.resource_check,
                                          self.home_position, self.resource_position, self.resource_frequency, gender,
                                          education, work_status, marriage, past_hh_id, migration_status)
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
        if random() < self.death_rate:
            self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)

    def marriage_check(self):
        if int(self.age) > 20 and int(self.gender) == 2 and int(self.marriage) == 0\
                and self.migration_status == 0:
                if random.random() < self.marriage_rate:
                    # get married
                    self.marriage = 1
                    self.past_hh_id = self.hh_id
                    self.match_female()
        if self.individual_id in married_male_list or self.individual_id in married_male_list_2014:
            self.marriage = 1
            # takes the first male off the single_male_list, which is shuffled every step
            self.hh_id = single_male_list[0][1]  # male's hh_id
            married_male_list.append(single_male_list[0][0])
            single_male_list.remove(single_male_list[0])

    def migration_check(self):
        if self.

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
