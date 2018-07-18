# !/usr/bin/python

"""
This file runs the demographic submodel for the Guizhou golden monkey population (birth, death, aging, etc.).
"""
from families import *

class Monkey(Family):
    #  while Family agents move on the visualization grid, Monkey agents follow demographic-based actions
    #  such as being born, aging, mating, dying, etc. in a different submodel

    def __init__(self, unique_id, model, current_position, family_size, list_of_family_members, family_type,
                 saved_position, gender, age, age_category, family_id, last_birth_interval, mother, death_flag):
        super().__init__(unique_id, model, current_position, family_size, list_of_family_members, family_type,
                         saved_position)
        self.gender = gender
        self.age = age
        self.age_category = age_category
        self.family_id = family_id
        self.last_birth_interval = last_birth_interval
        self.mother = mother
        self.death_flag = death_flag

    def step(self):

        # Aging
        self.age += (1 / 73)  # every step is 5 days, or 1/73rd of a year
        self.check_age_category()

        # Check if mother of recently dead infant and count time since last birth
        if self.unique_id in reproductive_female_list:
            if self.unique_id not in random_mother_list:
                random_mother_list.append(self.unique_id)
            self.check_recent_death_infant()
            self.last_birth_interval += 1 / 73

        # Check if male subgroup needs to break off of main group
        if self.model.time < 5:  # Temporary fix: currently, the moving family agents do not consider age
            # in the visualization, because aging would have very little impact on their movement behavior.
            # This temporary fix simply prevents too many male subgroups from spawning if the model runs for
            # longer than a few years; normally, older monkeys would die out,
            # so there would not be too many all-male subgroups existing at a time.
            self.create_male_subgroup()

        # Birth
        if (18 < self.model.step_in_year < 25) or (48 < self.model.step_in_year < 55) \
                and (self.gender == 1 and 10 <= self.age <= 25):
            if self.last_birth_interval >= 3:
                self.family_size += 1
                self.birth(self.current_position, self.family_size, self.family_id, self.unique_id,
                           self.list_of_family_members)
                self.last_birth_interval = 0

        # Death
        chance = random.uniform(0, 1)  # random decimal # between 0 and 1
        # Currently uses an exponential formula that considers death events as cumulative and dependent.
        # In other words, once a death occurs, it can no longer occur that year.
        # The model runs in time-steps of 5 days each, so there are 73 mortality checks per year.
        # the current formula uses: chance that a monkey does NOT die^73 = survival rate in one year
        # this gives a lower result than a similar formula that considers [yearly mortality rate]/73
        # formula may be changed later
        if self.age <= 1 and chance <= 0.0007:  # 0.0007 = 1 - 0.9993; 95% survival; see below
            self.death()
            demographic_structure_list[0] -= 1
            recent_death_infant.append(self.mother)
            # 0.9993^73 = 95% chance to survive each year with ticks every 5 days
            # 0.9987^73 = 91% chance to survive each year with ticks every 5 days
            # 0.99778^73 = 85% chance to survive first year with ticks every 5 days, or 15% yearly mortality
            # 0.99695^73 = 80% chance to survive first year with ticks every 5 days, or 20$ yearly mortality
            # if a monkey dies, mother can give birth again the following season
        elif 1 < self.age < 10 and chance <= 0.00043:  # 0.00043 = 1 - 0.99958; 97% survival; see below
            self.death()
            if 1 < self.age <= 3:
                demographic_structure_list[1] -= 1
            elif 3 < self.age <= 7:
                demographic_structure_list[2] -= 1
            elif 7 < self.age <= 10:
                demographic_structure_list[3] -= 1
                # 0.99973^73 = 98% chance to survive each year with ticks every 5 days
                # 0.99958^73 = 97% chance to survive each year with ticks every 5 days
                # 0.9993^73 = 95% chance to survive each year with ticks every 5 days
        elif 10 < self.age <= 30 and chance <= 0.0013:  # 0.0013 = 1 - 0.9987; 91% survival; see below
            self.death()
            if 10 < self.age <= 25:
                demographic_structure_list[4] -= 1
            elif 25 < self.age < 30:
                demographic_structure_list[5] -= 1
                # 0.99778^73 = 85% chance to survive each year with ticks every 5 days
                # 0.9987^73 = 91% chance to survive each year with ticks every 5 days
        elif self.age > 30 and chance <= 0.00222:  # 0.00222 = 1 - 0.99778; 85% survival; see below
            self.death()
            demographic_structure_list[5] -= 1
            # 0.99778^73 = 85% chance to survive each year with ticks every 5 days
            # 0.99607^73 = 75% chance to survive each year with ticks every 5 days

    def check_age_category(self):
        # sorts monkeys in the right age category as they age; breaks some males off into all-male subgroup at age 10
        if (self.age <= 1 and self.age_category == 0) or \
                (1 < self.age <= 3 and self.age_category == 1) or \
                (3 < self.age <= 7 and self.age_category == 2) or \
                (7 < self.age <= 10 and self.age_category == 3) or \
                (10 < self.age <= 25 and self.age_category == 4) or \
                (self.age > 25 and self.age_category == 5):
            pass
        else:
            demographic_structure_list[(self.age_category)] -= 1
            demographic_structure_list[(self.age_category + 1)] += 1
            self.age_category += 1

            if self.age_category == 4 and self.gender == 1:
                if self.unique_id not in reproductive_female_list:
                    reproductive_female_list.append(self.unique_id)

            elif self.age_category == 4 and self.gender == 0:
                # that is, if a male has just turned 10 years old,
                # determine if he breaks off into an all-male subgroup
                male_subgroup_choice = random.uniform(0, 1)
                if male_subgroup_choice < 0.4:
                    male_maingroup_list.remove(self.unique_id)  # male defects from main group
                    self.family_id = 0
                    self.family_type = 'all_male'
                    if self.unique_id not in male_subgroup_list:
                        male_subgroup_list.append(self.unique_id)

            elif self.age_category == 5 and self.gender == 1:  # female becomes too old to give birth
                if self.unique_id in reproductive_female_list:
                    reproductive_female_list.remove(self.unique_id)

    def check_recent_death_infant(self):
        # allow mothers who have recently lost an infant to give birth again in a short period
        if self.unique_id in recent_death_infant:
            self.last_birth_interval = random.uniform(2, 2.5)
            recent_death_infant.remove(self.unique_id)

    def birth(self, parent_current_position, new_family_size, parent_family, mother_id, list_of_family):
        # birth from the agent-perspective of the new monkey agent
        last = self.model.monkey_id_count
        current_position = parent_current_position
        saved_position = current_position
        family_size = new_family_size
        gender = random.randint(0, 1)
        age = 0
        age_category = 0
        family_id = parent_family
        if gender == 1:
            last_birth_interval = random.uniform(0, 3)
            female_list.append(last + 1)
        else:
            last_birth_interval = -9999
            male_maingroup_list.append(last + 1)
        mother = mother_id
        list_of_family_members = list_of_family
        list_of_family_members.append(last + 1)  # last + 1 = unique id
        if mother == 0 or mother == '0':
            mother = random.choice(random_mother_list)
        family_type = 'traditional'
        death_flag = 0  # actually useless for now, will delete later
        new_monkey = Monkey(last + 1, self.model, current_position, family_size, list_of_family_members, family_type,
                            saved_position, gender, age, age_category, family_id, last_birth_interval, mother,
                            death_flag)
        self.model.schedule.add(new_monkey)
        self.model.number_of_monkeys += 1
        self.model.monkey_id_count += 1
        self.model.monkey_birth_count += 1
        demographic_structure_list[0] += 1

    def death(self):
        # death from the perspective of a monkey agent
        self.death_flag = 1  # actually useless for now, will delete later
        self.model.schedule.remove(self)
        self.model.number_of_monkeys -= 1
        self.model.monkey_death_count += 1
        if self.unique_id in female_list:
            female_list.remove(self.unique_id)
        if self.unique_id in male_maingroup_list:
            male_maingroup_list.remove(self.unique_id)
        if self.unique_id in reproductive_female_list:
            reproductive_female_list.remove(self.unique_id)
        if self.unique_id in random_mother_list:
            random_mother_list.remove(self.unique_id)

    def create_male_subgroup(self):
        # male subgroup forms a new family and shows up in the visualization under a new, differently-vegetationed pixel
        if len(male_subgroup_list) > random.randint(10, 15):
            from model import global_family_id_list
            new_family_id = int(global_family_id_list[-1] + 1)
            global_family_id_list.append(new_family_id)
            family_type = 'all_male'
            saved_position = self.current_position
            male_family = Family(new_family_id, self.model, self.current_position, len(male_subgroup_list),
                                 male_subgroup_list,
                                 family_type, saved_position)
            self.model.grid.place_agent(male_family, self.current_position)
            self.model.schedule.add(male_family)
            del male_subgroup_list[:]  # the list that builds up the male subgroup gets cleared each time once the new
            # all-male family is actually created (which is done when 10-15 males have joined)