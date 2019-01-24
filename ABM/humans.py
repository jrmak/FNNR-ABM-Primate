# !/usr/bin/python
"""
This document imports human data from the Excel file containing Shuang's survey results and determines behavior for human agents.
"""

from mesa.agent import Agent
import random
import math
import decimal

single_male_list = []
married_male_list = []
human_birth_list = []
human_marriage_list = []
human_death_list = []
human_avoidance_list = []  # sets coordinate positions the monkeys should not step on, because humans are on it.
# Neighboring cells of human activity may also be added to this list.
birth_flag_list = []
marriage_flag_list = []
labor_list = []
human_demographic_structure_list = [0] * 20

# 169 = household IDs, 170 = 169 + 1 indices (+ 1 is for the 0th index)
# 170 indices total; not all are used; these are just to store values for each household
hh_migration_flag = [0] * 170  # 1 if the head of household out-migrates, 0 if not or if returned
num_labor_list = [0] * 170  # number of laborers in each household; index is hh #; 0th index is always 0
head_of_household_list = [0] * 170
former_hoh_list = [0] * 170
hh_size_list = [0] * 170
total_migration_list = [0] * 170
total_re_migration_list = [0] * 170


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
                 marriage, past_hh_id, mig_years, migration_status, gtgp_part, non_gtgp_area,
                 migration_network, mig_remittances, income_local_off_farm,
                 last_birth_time, death_rate, age_category):
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
        self.gtgp_part = gtgp_part
        self.non_gtgp_area = non_gtgp_area
        self.migration_network = migration_network
        self.mig_remittances = mig_remittances
        self.income_local_off_farm = income_local_off_farm
        self.last_birth_time = last_birth_time
        self.death_rate = death_rate
        self.age_category = age_category

        if self.migration_status == 0 and self.hh_id != 'Migrated':
            if self.work_status == 1 and head_of_household_list[self.hh_id] == 0:
                head_of_household_list[self.hh_id] = self.unique_id

    def step(self):
        # human aging/demographic behavior
        if self.model.time == 1/73:  # first step list populating
            if self.age > 15 and self.migration_status == 0:  # event check happens once a year
                self.migration_check()  # minors don't migrate
            if self.migration_status == 1:
                total_migration_list[self.past_hh_id] = 1
            if self.migration_status == 0:
                hh_size_list[self.hh_id] += 1
                if self.work_status == 1:
                    num_labor_list[self.hh_id] += 1
                    labor_list.append(self.unique_id)
                if self.gender == 1 and self.marriage == 1 and self.unique_id not in married_male_list:
                    married_male_list.append(self.unique_id)
            # local_income_off_farm added first step once per household
            if self.hh_id != 'Migrated':
                self.hoh_check()
                if self.unique_id in head_of_household_list:
                    from land import household_income_list
                    household_income_list[self.hh_id] += float(self.income_local_off_farm)

        if self.migration_status == 0:
            self.age_check()
            self.hoh_check()
            self.marriage_check()
            self.birth_check()
            self.death_check()
            self.movement()

            if self.age > 15 and random.random() < 1/73:  # event check happens once a year
                self.migration_check()  # minors don't migrate

        elif self.migration_status == 1 and random.random() < 1/73:  # event check happens once a year:
            self.re_migration_check()

        self.age += 1 / 73
        self.check_age_category()
        self.last_birth_time += 1 / 73

        # every step, perform a single/married male check
        # since marriage happens from the female's point of view
        if int(self.age) > 20 and self.gender == 1 and self.marriage != 1 and self.migration_status == 0\
                and [self.unique_id, self.hh_id] not in single_male_list:
            single_male_list.append([self.unique_id, self.hh_id])

        if self.unique_id in married_male_list:
            if [self.unique_id, self.hh_id] in single_male_list:
                single_male_list.remove([self.unique_id, self.hh_id])
            self.marriage = 1

        random.shuffle(single_male_list)

    def movement(self):
    # human movement and resource collection behavior only occurs with 1 gatherer per household
        if self.unique_id in head_of_household_list:
            if len(human_avoidance_list) > 372 * 9:  # 372 humans, 8 neighbors/9 cells, so 94 * 9 instances per step
                del human_avoidance_list[:]  # reset the list every step (once it hits a length of 372 * 9)
            load_dict = {}
            masterdict = self.model.saveLoad(load_dict, 'masterdict_veg', 'load')
            current_position = list(self.current_position)  # changes tuple into a list to edit; content remains the same
            if self.current_position not in masterdict['Forest'] + masterdict['Household'] + masterdict['PES']  \
                + masterdict['Farm'] + masterdict['Elevation_Out_of_Bound'] + human_avoidance_list + \
                    masterdict['Outside_FNNR']:
                human_avoidance_list.append(self.current_position)
            human_neighboring_grids = self.model.grid.get_neighborhood(self.current_position, True, False)
            for human_neighbor in human_neighboring_grids:
                 human_avoidance_list.append(human_neighbor)
            if self.resource_check == 0 and self.resource_position is not None and self.resource_position != '':
                # if the human does not have the resource, head towards it
                try:
                    if self.resource_frequency == 0:
                        from model import resource_dict
                        resource = random.choice(resource_dict[self.hh_id])  # randomly choose resource
                        self.resource_frequency = resource.frequency
                        self.resource_position = resource.position
                    self.move_to_point(self.resource_position, self.resource_frequency)
                except:
                    # print('Error moving', self.resource_position)
                    pass
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
            if self.work_status == 0:
                self.work_status = 1
                num_labor_list[self.hh_id] += 1
                labor_list.append(self.unique_id)
            if self.work_status == 1 and self.unique_id not in labor_list:
                labor_list.append(self.unique_id)
        else:
            self.work_status = 0

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
            self.death_rate = 0.001443  # 5-day death rate
        # The average death rate in China is 7.3 per 1,000 people/year, or 0.0073 (Google).
        # However, death rates should be higher for the elderly, or else the population structure will skew.
        # I set death rates for those over age 65 to be 10% per year--0.9 yearly survival rate.
        # The survival rate for each 5-day step is compounded 73 times, so x^73 = 0.9.
        # 0.998557 is the 5-day survival rate, and 1 - x is the 5-day death rate.
        else:
            self.death_rate = 0.00000425
        # I wanted people to have a 98% chance of reaching age 65 (death rate is lower if not elderly).
        # If a 'check' is every 5 days, 73 checks/year * 65 years = 4,745 checks.
        # x^4745 = 0.98; the 5-day survival rate is 0.99999575, and 1 - x is the 5-day death rate.

        # These rates are changeable later.

    def check_age_category(self):
        # sorts humans in the right age category as they age
        if int(self.gender) == 1:
            if (0 < self.age <= 10 and self.age_category == 0) or \
                    (10 < self.age <= 20 and self.age_category == 1) or \
                    (20 < self.age <= 30 and self.age_category == 2) or \
                    (30 < self.age <= 40 and self.age_category == 3) or \
                    (40 < self.age <= 50 and self.age_category == 4) or \
                    (50 < self.age <= 60 and self.age_category == 5) or \
                    (60 < self.age <= 70 and self.age_category == 6) or \
                    (70 < self.age <= 80 and self.age_category == 7) or \
                    (80 < self.age <= 90 and self.age_category == 8) or \
                    (self.age > 90 and self.age_category == 9):
                        pass
            else:
                human_demographic_structure_list[(self.age_category)] -= 1
                human_demographic_structure_list[(self.age_category + 1)] += 1
                self.age_category += 1
        elif self.gender != 1:
            if (0 < self.age <= 10 and self.age_category == 10) or \
                    (10 < self.age <= 20 and self.age_category == 11) or \
                    (20 < self.age <= 30 and self.age_category == 12) or \
                    (30 < self.age <= 40 and self.age_category == 13) or \
                    (40 < self.age <= 50 and self.age_category == 14) or \
                    (50 < self.age <= 60 and self.age_category == 15) or \
                    (60 < self.age <= 70 and self.age_category == 16) or \
                    (70 < self.age <= 80 and self.age_category == 17) or \
                    (80 < self.age <= 90 and self.age_category == 18) or \
                    (self.age > 90 and self.age_category == 19):
                        pass
            else:
                human_demographic_structure_list[(self.age_category)] -= 1
                human_demographic_structure_list[(self.age_category + 1)] += 1
                self.age_category += 1

    def hoh_check(self):
        # designates the oldest working person of a household as its gatherer
        # removes all others from the gatherer (head of household list)

        if self.age >= 59 and self.unique_id in head_of_household_list:
            head_of_household_list[self.hh_id] = 0

        if self.work_status == 1 and head_of_household_list[self.hh_id] == 0:
            head_of_household_list[self.hh_id] = self.unique_id
            if former_hoh_list[self.hh_id] != 0:
                self.resource_frequency = self.resource_frequency * 0.5

        if self.age >= 59 or self.age < 15 and num_labor_list[self.hh_id] == 0\
                and head_of_household_list[self.hh_id] == 0:
            head_of_household_list[self.hh_id] = self.unique_id
            self.work_status = 1
            self.resource_frequency = self.resource_frequency * 0.25

    def birth_check(self):
        """Small chance of giving birth every step if female, married, and under 55"""
        if random.random() < 0.00017:  # 0.0121, or 1.21%, is the yearly birth rate.
            birth_flag_list.append(1)
            # This makes the birth rate for every 5 days (73 'checks' a year) 0.00017%,
            # because 1 - 0.0121 = 0.9879; 98.79% is the chance of not giving birth that year.
            # 0.99983 ^73 = 0.9879 are the 5-day chances compounded 73 times, and 1 - 0.99983 = 0.00017.
            # or you could use the yearly birth rate and have birth_check only occur randomly
            # around once a year.
        if birth_flag_list != [] and self.gender == 2 and self.marriage == 1 and self.age < 55:
            if self.last_birth_time >= 2:  # 2 years is the set birth interval; can modify
                self.last_birth_time = 0  # reset counter
                if birth_flag_list != []:
                    birth_flag_list.remove(1)
                last = self.model.number_of_humans
                # build more attributes
                age = 0
                gender = random.choice([1, 2])
                education = 0
                work_status = 0
                marriage = 0
                if gender == 1:
                    age_category = 0
                elif gender == 2:
                    age_category = 10
                ind = Human(last + 1, self.model, self.current_position, self.hh_id, age, self.resource_check,
                                      self.home_position, self.resource_position, self.resource_frequency, gender,
                                      education, work_status, marriage, self.past_hh_id, self.mig_years,
                                      self.migration_status, self.gtgp_part, self.non_gtgp_area,
                                      self.migration_network, self.mig_remittances, self.income_local_off_farm,
                                      self.last_birth_time, self.death_rate, age_category)
                self.model.schedule.add(ind)
                self.model.number_of_humans += 1
                hh_size_list[self.hh_id] += 1
                human_birth_list.append(last + 1)
                if ind.gender == 1:
                    human_demographic_structure_list[0] += 1
                elif ind.gender == 2:
                    human_demographic_structure_list[10] += 1

    def death_check(self):
        """Small chance of dying every step; chance increases if over 65, see age_check()"""
        chance = random.random()
        if decimal.Decimal(chance) < decimal.Decimal(self.death_rate):
            if self.unique_id in head_of_household_list:
                try:
                    head_of_household_list[self.hh_id] = 0
                except TypeError:  # head of household migrated
                    head_of_household_list[self.past_hh_id] = 0
            self.model.number_of_humans -= 1
            if self.unique_id in labor_list:
                labor_list.remove(self.unique_id)
            if self.work_status == 1:
                try:
                    num_labor_list[self.hh_id] -= 1
                except TypeError:
                    num_labor_list[self.past_hh_id] -= 1
            if self.unique_id in former_hoh_list:
                try:
                    former_hoh_list[self.hh_id] = 0
                except:
                    former_hoh_list[self.past_hh_id] = 0
            if [self.unique_id, self.hh_id] in single_male_list:
                single_male_list.remove([self.unique_id, self.hh_id])
            if self.unique_id in married_male_list:
                married_male_list.remove(self.unique_id)
            human_death_list.append(self.unique_id)
            try:
                hh_size_list[self.hh_id] -= 1
            except:
                hh_size_list[self.past_hh_id] -= 1
            human_demographic_structure_list[self.age_category] -= 1

            self.model.schedule.remove(self)
            if self in self.model.grid:
                self.model.grid.remove_agent(self)

    def marriage_check(self):
        if random.random() < 0.000096:
            marriage_flag_list.append(1)
        if int(self.age) > 20 and int(self.gender) == 2 and int(self.marriage) != 1 \
                and marriage_flag_list != [] and hh_size_list[self.hh_id] > 1:  # marriage occurs
            # marriage late is set low because this is a 5-day rate
            # the yearly marriage rate is 0.007, or 0.7%
            self.marriage = 1
            self.past_hh_id = self.hh_id
            hh_size_list[self.hh_id] -= 1
            self.hh_id = single_male_list[0][1]  # male's hh_id
            hh_size_list[self.hh_id] += 1
            married_male_list.append(single_male_list[0][0])  # male's unique_id
            marriage_flag_list.remove(1)
            if self.hh_id not in human_marriage_list:
                human_marriage_list.append(self.hh_id)


    def migration_check(self):
        """Describes out-migration process and probability"""

        from land import non_gtgp_part_list, gtgp_part_list, non_gtgp_area_list

        self.non_gtgp_area = non_gtgp_area_list[self.hh_id]

        if num_labor_list[self.hh_id] != 0:
            non_gtgp_land_per_labor = self.non_gtgp_area / num_labor_list[self.hh_id]
        else:
            non_gtgp_land_per_labor = 0
        try:
            remittance = random.normalvariate(1200, 16000)
        # 1200 is the mean, and 400^2 is the st. dev. according to the original pseudocode, but this seems strange
        except:
            remittance = 0
        if remittance < 0:
            remittance = 0
        self.mig_remittances = float(remittance)
        if self.hh_id in non_gtgp_part_list:
            self.gtgp_part = 0
        elif self.hh_id in gtgp_part_list:
            self.gtgp_part = 1
        prob = math.exp(2.07 - 0.00015 * float(self.income_local_off_farm) + 0.67 * float(num_labor_list[self.hh_id])
               + 4.36 * float(self.migration_network) - 0.58 * float(non_gtgp_land_per_labor)
               + 0.27 * float(self.gtgp_part) - 0.13 * float(self.age) + 0.07 * float(self.gender)
               + 0.17 * float(self.education) + 0.88 * float(self.marriage) +
               1.39 * float(self.work_status) + 0.001 * float(self.mig_remittances))  # Shuang's formula
        mig_prob = prob / (prob + 1)
        if random.random() < mig_prob and hh_size_list[self.hh_id] >= 2:  # out-migration occurs
            if hh_migration_flag[self.hh_id] == 0:  # only one migrant allowed per household at a time
                hh_size_list[self.hh_id] -= 1
                self.past_hh_id = self.hh_id
                self.migration_status = 1
                from land import household_income_list
                household_income_list[self.past_hh_id] += self.mig_remittances
                if self.unique_id in head_of_household_list:
                    head_of_household_list[self.past_hh_id] = 0
                    former_hoh_list[self.hh_id] = self.unique_id
                    self.resource_frequency = self.resource_frequency * 0.5
                hh_migration_flag[self.hh_id] = 1
                if self.work_status == 1:
                    num_labor_list[self.hh_id] -= 1
                if self.unique_id in labor_list:
                    labor_list.remove(self.unique_id)
                if self.hh_id not in total_migration_list:
                    total_migration_list[self.hh_id] = 1
                self.work_status = 0

                self.hh_id = 'Migrated'

    def re_migration_check(self):
        """Describes re-migration process and probability following out-migration"""
        if self.hh_id == 'Migrated':
            self.mig_years += 1/73

            prob = math.exp(-1.2 + 0.06 * float(self.age) - 0.08 * self.mig_years)
            re_mig_prob = prob / (prob + 1)
            if random.random() < re_mig_prob:  # re-migration occurs
                self.migration_status = 0
                self.hh_id = self.past_hh_id
                self.mig_years = 0
                from land import household_income_list
                household_income_list[self.past_hh_id] -= self.mig_remittances
                hh_size_list[self.hh_id] += 1
                hh_migration_flag[self.hh_id] = 0
                if self.hh_id not in total_re_migration_list:
                    total_re_migration_list[self.hh_id] += 1
                if self.unique_id == former_hoh_list[self.hh_id]:
                    self.resource_frequency = self.resource_frequency * 2
                if 15 < int(self.age) < 59:
                    self.work_status = 1
                    num_labor_list[self.hh_id] += 1
                    labor_list.append(self.unique_id)
                total_migration_list[self.hh_id] = 0


    def move_to(self, pos):
        if pos != None:
            try:
                self.model.grid.move_agent(self, pos)
            except Exception as e:
                print(self.current_position, self.home_position)
                print(e)
            finally:
                self.current_position = self.home_position
                pass

    def move_to_point(self, destination, frequency):
        """Moves human agent to assigned point according to frequency"""
        # index 0 represents x, index 1 represents y
        if frequency > 1:
            x_towards = int(round((destination[0] - current_position[0]) / frequency))
            if x_towards > 1:
                x_towards -= 1
            y_towards = int(round((destination[1] - current_position[1]) / frequency))
            if y_towards > 1:
                y_towards -= 1
            current_position = list(self.current_position)
            if current_position[0] < destination[0]:  # if x is west
                current_position[0] = current_position[0] + x_towards
                x_change = int(frequency)
                if current_position[0] >= destination[0]:  # if this overshoots:
                    current_position[0] = destination[0]
            elif current_position[0] == destination[0]:
                pass  # don't move
            else:
                current_position[0] = current_position[0] - x_towards
                x_change = 0 - int(frequency)
                if current_position[0] <= destination[0]:  # if this overshoots:
                    current_position[0] = destination[0]
            if current_position[1] < destination[1]:
                current_position[1] = current_position[1] + y_towards
                y_change = int(frequency)
                if current_position[1] >= destination[1]:  # if this overshoots:
                    current_position[1] = destination[1]
            elif current_position[1] == destination[1]:
                pass
            else:
                current_position[1] = current_position[1] - y_towards
                y_change = 0 - int(frequency)
                if current_position[1] <= destination[1]:  # if this overshoots:
                    current_position[1] = destination[1]

            current_position = tuple(current_position)
            self.move_to(current_position)
            for i in list(range(1, int(frequency))):
                human_avoidance_list.append((current_position[0] + x_change, current_position[1] + y_change))
            self.current_position = current_position
            if current_position[0] == destination[0] and current_position[1] == destination[1]:
                self.resource_check = 1
        else:
            self.resource_frequency += self.resource_frequency / 6  # 6 * 5 days in a step = 30 days in a month
            # resource frequency is listed monthly in the source file
            # this indicates time passing each step until the gatherer can move

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
