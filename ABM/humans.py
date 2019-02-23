# !/usr/bin/python
"""
This document imports human data from the Excel file containing Shuang's survey results and determines behavior for human agents.
"""

from mesa.agent import Agent
from fnnr_config_file import college_likelihood
import random
import math
import os

single_male_list = []
married_male_list = []
human_birth_list = []
human_death_list = []
human_avoidance_dict = {}  # sets coordinate positions the monkeys should not step on, because humans are on it.
# Neighboring cells of human activity may also be added to this list.
birth_flag_list = []
marriage_flag_list = []
human_demographic_structure_list = [0] * 20

# 169 = household IDs, 170 = 169 + 1 indices (+ 1 is for the 0th index)
# 170 indices total; not all are used; these are just to store values for each household
hh_migration_flag = [0] * 170  # 1 if the head of household out-migrates, 0 if not or if returned
num_labor_list = [0] * 170  # number of laborers in each household; index is hh #; 0th index is always 0
human_marriage_list = [0] * 170
head_of_household_list = [0] * 170
former_hoh_list = [0] * 170
hh_size_list = [0] * 170
total_migration_list = [0] * 170
total_re_migration_list = [0] * 170
first_step_income_list = [0] * 170

run = 1  # do not change this; it will automatically search for the first number-as-string not taken
while os.path.isfile(os.getcwd() + '\\' + 'fnnr_human_log_file' + str(run) + '.txt'):
    # if folder exists in current directory, loop up until it finds a unique number
    run += 1
human_log = 'fnnr_human_log_file' + str(run) + '.txt'

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
    def __init__(self, unique_id, model, current_position, hh_id, age, resource_check,
                 home_position, resource_position, resource_frequency, gender, education, work_status,
                 marriage, past_hh_id, mig_years, migration_status, gtgp_part, non_gtgp_area,
                 migration_network, mig_remittances, income_local_off_farm,
                 last_birth_time, death_rate, age_category, children, birth_plan):
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
        self.children = children
        self.birth_plan = birth_plan

        self.current_position = self.home_position

    def step(self):
        # human aging/demographic behavior
        if self.model.time == 1/73:  # first step list populating
            if self.migration_status == 0 and self.hh_id != 'Migrated':
                if first_step_income_list[self.hh_id] == 0:
                    from land import household_income_list
                    household_income_list[self.hh_id] += float(self.income_local_off_farm)
                    first_step_income_list[self.hh_id] = 1
                if self.work_status == 1 and head_of_household_list[self.hh_id] == 0:
                    head_of_household_list[self.hh_id] = self.unique_id
            if self.migration_status == 1:
                total_migration_list[self.past_hh_id] = 1
            if self.migration_status == 0:
                hh_size_list[self.hh_id] += 1
                if self.work_status == 1:
                    num_labor_list[self.hh_id] += 1
                if self.gender == 1 and self.marriage == 1 and self.unique_id not in married_male_list:
                    married_male_list.append(self.unique_id)
            if int(self.age) > 20 and self.gender == 1 and self.marriage != 1 and self.hh_id != 'Migrated' \
                    and [self.unique_id, self.hh_id] not in single_male_list:
                single_male_list.append([self.unique_id, self.hh_id])
            # local_income_off_farm added first step once per household
            if self.hh_id != 'Migrated':
                self.hoh_check()

        if self.migration_status == 0 and self.hh_id != 'Migrated':
            self.age_check()
            self.hoh_check()
            if self.hh_id not in [1, 18, 40, 45, 51, 79, 81, 89, 91, 109, 133, 139, 148, 160, 168]:
                self.movement()
                pass

            if 15 < self.age < 59 and random.random() < 1/73:  # event check happens once a year
                self.migration_check()  # minors don't migrate

        elif self.migration_status == 1 and random.random() < 1/73:  # event check happens once a year:
            self.re_migration_check()

        if random.random() < 1/73:
            self.marriage_check()
            self.death_check()

        self.age += 1/73
        self.check_age_category()
        self.last_birth_time += 1/73

        if 20 < int(self.age) < 45 and self.gender == 2 and self.marriage == 1 and self.migration_status == 0\
                and random.random() < 1/73:
            self.birth_check()

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
            if len(human_avoidance_dict) > self.model.number_of_humans * 9:  # 8 neighbors/9 cells, so 94 * 9 instances per step
                human_avoidance_dict.clear() # reset the list every step (once it hits a length of 372 * 9)

            if self.resource_check == 0 and self.resource_position is not None and self.resource_position != '':
                # if the human does not have the resource, head towards it
                if self.resource_frequency == 0:
                    from model import resource_dict
                    resource = random.choice(resource_dict[self.hh_id])  # randomly choose resource
                    self.resource_frequency = resource.frequency
                    self.resource_position = resource.position
                while self.current_position != self.resource_position:
                    self.move_to_point(self.resource_position, self.resource_frequency)
                    human_neighboring_grids = self.model.grid.get_neighborhood(self.current_position, True, False)
                    for human_neighbor in human_neighboring_grids:
                        if self.resource_frequency > 6:
                            human_avoidance_dict.setdefault((human_neighbor), ((self.resource_frequency - 6) / 6))

            else:
                while self.current_position != self.home_position:
                    self.move_to_point(tuple(self.home_position), self.resource_frequency)  # else, head home
                if self.current_position[0] == list(self.home_position)[0] and self.current_position[1] == list(self.home_position)[1]:
                    # if you are back home, go out and collect resources again
                    self.resource_check = 0
                    from model import resource_dict
                    resource = random.choice(resource_dict[self.hh_id])  # randomly choose resource
                    self.resource_frequency = resource.frequency
                    self.resource_position = resource.position

    def age_check(self):
        """Check working and education age, as well as age-based death rates"""
        # check working status
        if 15 <= float(self.age) < 59:
            if self.work_status == 5 or self.work_status == 6:
                self.work_status = 1
                num_labor_list[self.hh_id] += 1
        else:
            self.work_status = 6

        # check education status; measured in years of education
        if 7 <= int(self.age) <= 19:
            if random.random() < 0.9:
                self.education += 1
                self.work_status == 5
                # most adults in the FNNR did not get a full 12-13 years of education

        # check age-based death rates
        if self.age <= 6:
           self.death_rate = 0.00745 * 0.5
        elif 6 < self.age <= 13:
            self.death_rate = 0.0009 * 0.5
        elif 13 < self.age <= 16:
            self.death_rate = 0.00131 * 0.5
        elif 16 < self.age <= 21:
            self.death_rate = 0.00196 * 0.5
        elif 21 < self.age <= 60:
            self.death_rate = 0.001291 * 0.5
        elif 60 < self.age:
            self.death_rate = 0.05354 * 0.5
        # These rates are changeable later.

        if 16 < self.age <= 20 and random.random() < (0.0192 * college_likelihood) and self.migration_status == 0\
            and random.random() < ((1/73) / 4):
            # person out-migrates to college and does not return
            log = open(human_log, 'a+')
            log.writelines('College, ' + 'Step ' + str(int(self.model.time * 73)) + ': Agent,' + str(self.unique_id)
                           + ',' + str(self.age) + ',' + str(self.gender) + ',' + 'went to college')
            log.writelines('\n')
            log.close()
            self.migration_status = 2
            self.education += 4
            hh_size_list[self.hh_id] -= 1
            total_migration_list[self.hh_id] += 1
            self.hh_id = 'Migrated'
            if self.unique_id in head_of_household_list:
                try:
                    head_of_household_list[self.hh_id] = 0
                except TypeError:  # head of household migrated
                    head_of_household_list[self.past_hh_id] = 0
            self.model.number_of_humans -= 1
            if self.work_status == 1:
                try:
                    num_labor_list[self.hh_id] -= 1
                except TypeError:
                    num_labor_list[self.past_hh_id] -= 1
                self.work_status = 6
            if self.unique_id in former_hoh_list:
                try:
                    former_hoh_list[self.hh_id] = 0
                except TypeError:
                    former_hoh_list[self.past_hh_id] = 0
            human_demographic_structure_list[self.age_category] -= 1
            self.model.schedule.remove(self)
            if self in self.model.grid:
                self.model.grid.remove_agent(self)

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
                log = open(human_log, 'a+')
                log.writelines('Aging, ' + 'Step ' + str(int(self.model.time * 73)) + ': Agent,' + str(self.unique_id)
                               + ',' + str(self.age) + ',' + str(self.gender) + ',' + 'aged to age category' + ','
                               + str(self.age_category + 1))
                log.writelines('\n')
                log.close()
                human_demographic_structure_list[(self.age_category)] -= 1
                human_demographic_structure_list[(self.age_category + 1)] += 1
                self.age_category += 1
                if self.age_category == 6 and self.work_status == 1:
                    try:
                        num_labor_list[self.hh_id] -= 1
                    except TypeError:
                        num_labor_list[self.past_hh_id] -= 1
                    self.work_status = 6
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
                log = open(human_log, 'a+')
                log.writelines('Aging, ' + 'Step ' + str(int(self.model.time * 73)) + ': Agent,' + str(self.unique_id)
                               + ',' + str(self.age) + ',' + str(self.gender) + ',' + 'aged to age category' + ','
                               + str(self.age_category + 1))
                log.writelines('\n')
                log.close()
                human_demographic_structure_list[(self.age_category)] -= 1
                human_demographic_structure_list[(self.age_category + 1)] += 1
                self.age_category += 1
                if self.age_category == 6 and self.work_status == 1:
                    try:
                        num_labor_list[self.hh_id] -= 1
                    except TypeError:
                        num_labor_list[self.past_hh_id] -= 1
                    self.work_status = 6

    def hoh_check(self):
        """Activated when the head of household has migrated or retires"""

        if self.age >= 59 and self.unique_id in head_of_household_list:
            head_of_household_list[self.hh_id] = 0

        if self.work_status == 1 and head_of_household_list[self.hh_id] == 0:
            head_of_household_list[self.hh_id] = self.unique_id
            if former_hoh_list[self.hh_id] != 0:
                self.resource_frequency = self.resource_frequency * 0.5

        elif self.age >= 59 or self.age < 15 and num_labor_list[self.hh_id] == 0\
                and head_of_household_list[self.hh_id] == 0:
            head_of_household_list[self.hh_id] = self.unique_id
            self.work_status = 1
            self.resource_frequency = self.resource_frequency * 0.25


    def birth_check(self):
        """Adds children to reserve"""
        if self.children < self.birth_plan:
            if self.last_birth_time >= random.uniform(1, 4):
                last = self.model.human_id_count
                log = open(human_log, 'a+')
                log.writelines('Birth, ' + 'Step ' + str(int(self.model.time * 73)) + ': Agent,' + str(self.unique_id) +
                ',' + str(self.age) + ',' + str(self.gender) + ',' + ' gave birth to Agent,' + str(last + 1))
                log.writelines('\n')
                log.close()
                self.children += 1
                # build more attributes
                age = 0
                gender = random.choice([1, 2])
                education = 0
                work_status = 6
                marriage = 6
                children = 0
                if gender == 1:
                    age_category = 0
                    birth_plan = 0
                elif gender == 2:
                    age_category = 10
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
                ind = Human(last + 1, self.model, self.current_position, self.hh_id, age, self.resource_check,
                                      self.home_position, self.resource_position, self.resource_frequency, gender,
                                      education, work_status, marriage, self.past_hh_id, self.mig_years,
                                      self.migration_status, self.gtgp_part, self.non_gtgp_area,
                                      self.migration_network, self.mig_remittances, self.income_local_off_farm,
                                      self.last_birth_time, self.death_rate, age_category, children, birth_plan)
                self.model.grid.place_agent(ind, self.home_position)
                self.model.schedule.add(ind)
                self.model.number_of_humans += 1
                self.model.human_id_count += 1
                hh_size_list[self.hh_id] += 1
                human_birth_list.append(last + 1)
                if ind.gender == 1:
                    human_demographic_structure_list[0] += 1
                elif ind.gender == 2:
                    human_demographic_structure_list[10] += 1

    def death_check(self):
        """Small chance of dying every step; chance increases if over 65, see age_check()"""
        if random.random() < self.death_rate:
            log = open(human_log, 'a+')
            log.writelines('Death, ' + 'Step ' + str(int(self.model.time * 73)) + ': Agent,' + str(self.unique_id)
                           + ',' + str(self.age) + ',' + str(self.gender) + ',' + 'died')
            log.writelines('\n')
            log.close()
            if self.unique_id in head_of_household_list:
                try:
                    head_of_household_list[self.hh_id] = 0
                except TypeError:  # head of household migrated
                    head_of_household_list[self.past_hh_id] = 0
            self.model.number_of_humans -= 1
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
#        if random.random() < 0.0001055:
        if random.random() < 0.00767:
            marriage_flag_list.append(1)
        if random.uniform(20, 30) < int(self.age) < 45 and int(self.gender) == 2 and int(self.marriage) != 1 \
                and marriage_flag_list != [] and self.migration_status == 0:  # marriage occurs
            # marriage late is set low because this is a 5-day rate
            # the yearly marriage rate is 0.00767, or 0.767%
            # x^73 = 0.999233 = marriage rate for 5 days
            log = open(human_log, 'a+')
            log.writelines('Marriage, ' + 'Step ' + str(int(self.model.time * 73)) + ': Agent,' + str(self.unique_id)
                           + ',' + str(self.age) + ',' + str(self.gender) + ',' + ' got married to Agent #,'
                           + str(single_male_list[0][0]))
            log.writelines('\n')
            log.close()
            self.marriage = 1
            hh_size_list[self.hh_id] -= 1
            self.hh_id = single_male_list[0][1]  # male's hh_id
            hh_size_list[self.hh_id] += 1
            married_male_list.append(single_male_list[0][0])  # male's unique_id
            marriage_flag_list.remove(1)
            human_marriage_list[self.hh_id] += 1

    def migration_check(self):
        """Describes out-migration process and probability"""

        from land import non_gtgp_part_list, gtgp_part_list, non_gtgp_area_list

        self.non_gtgp_area = non_gtgp_area_list[self.hh_id]

        if num_labor_list[self.hh_id] != 0:
            non_gtgp_land_per_labor = self.non_gtgp_area / num_labor_list[self.hh_id]
        else:
            non_gtgp_land_per_labor = 0
        if self.hh_id in non_gtgp_part_list:
            self.gtgp_part = 0
        elif self.hh_id in gtgp_part_list:
            self.gtgp_part = 1
        self.mig_remittances = self.mig_remittances * 1.03  # yearly inflation
        self.income_local_off_farm = self.income_local_off_farm * 1.03  # yearly inflation
        prob = math.exp(2.07 - 0.00015 * float(self.income_local_off_farm) + 0.67 * float(num_labor_list[self.hh_id])
               + 4.36 * float(self.migration_network) - 0.58 * float(non_gtgp_land_per_labor)
               + 0.27 * float(self.gtgp_part) - 0.13 * float(self.age) + 0.07 * float(self.gender)
               + 0.17 * float(self.education) + 0.88 * float(self.marriage) +
               1.39 * float(self.work_status) + 0.001 * float(self.mig_remittances))  # Shuang's formula
        mig_prob = (prob / (prob + 1) / 45)  # / 45 for ages 15-59; migration is a lifetime, not yearly, probability
        if random.random() < mig_prob and hh_size_list[self.hh_id] >= 2:  # out-migration occurs
            log = open(human_log, 'a+')
            log.writelines('Migration, ' + 'Step ' + str(int(self.model.time * 73)) + ': Agent,' + str(self.unique_id)
                           + ',' + str(self.age) + ',' + str(self.gender) + ',' + 'migrated out')
            log.writelines('\n')
            log.close()
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
            total_migration_list[self.hh_id] += 1
            self.work_status = 6
            self.hh_id = 'Migrated'
            if self in self.model.grid:
                self.model.grid.remove_agent(self)

    def re_migration_check(self):
        """Describes re-migration process and probability following out-migration"""
        if self.migration_status == 1:
            prob = math.exp(-1.2 + 0.06 * float(self.age) - 0.08 * self.mig_years)
            re_mig_prob = (prob / (prob + 1) / 45) # 45 for ages 15-59; migration is a lifetime, not yearly, probability
            self.mig_years += 1
            if random.random() < re_mig_prob:  # re-migration occurs
                log = open(human_log, 'a+')
                log.writelines('Re-migration, ' + 'Step ' + str(int(self.model.time * 73)) + ': Agent,' + str(self.unique_id)
                               + ',' + str(self.age) + ',' + str(self.gender) + ',' + 're-migrated')
                log.writelines('\n')
                log.close()
                self.migration_status = 0
                self.hh_id = self.past_hh_id
                self.mig_years = 0
                from land import household_income_list
                household_income_list[self.past_hh_id] -= self.mig_remittances
                hh_size_list[self.hh_id] += 1
                hh_migration_flag[self.hh_id] = 0
                if self.hh_id not in total_re_migration_list:
                    total_re_migration_list[self.hh_id] += 1
                if self.unique_id in former_hoh_list:
                    self.resource_frequency = self.resource_frequency * 2
                    if self.age < 59 and head_of_household_list[self.hh_id] == 0:
                        head_of_household_list[self.hh_id] = self.unique_id
                if 15 < int(self.age) < 59:
                    self.work_status = 1
                    num_labor_list[self.hh_id] += 1
                total_migration_list[self.hh_id] -= 1


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
        current_position = list(self.current_position)  # changes tuple into a list to edit; content remains the same

        if current_position[0] < destination[0]:  # if the current position is away from Yaogaoping,
            current_position[0] = current_position[0] + 1  # move it closer
        elif current_position[0] == destination[0]:
            pass
        else:
            current_position[0] = current_position[0] - 1

        if current_position[1] < destination[1]:
            current_position[1] = current_position[1] + 1
        elif current_position[1] == destination[1]:
            pass
        else:
            current_position[1] = current_position[1] - 1
        current_position = tuple(current_position)
        self.move_to(current_position)
        self.current_position = current_position

        human_avoidance_dict.setdefault((current_position[0], current_position[1]), frequency / 6)

        if current_position[0] == destination[0] and current_position[1] == destination[1]:
            self.resource_check = 1

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
