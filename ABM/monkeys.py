"""
This file handles the demographic submodel for the Guizhou golden monkey population (birth, death, aging, etc.).
"""

from families import *

male_migration_list = []
new_family_counter = [0]
new_male_family_counter = [0]
old_family_ids = {}
new_families_dict = {}
new_male_families_dict = {}

class Monkey(Agent):
    #  while Family agents move on the visualization grid, Monkey agents follow demographic-based actions
    #  such as being born, aging, mating, dying, etc. in a different but related submodel
    def __init__(self, unique_id, model, gender, age, age_category, family, last_birth_interval,
                 mother):
        super().__init__(unique_id, model)
        self.age = age
        self.gender = gender
        self.age_category = age_category  # ages 0-1, 3-7, etc.
        self.family = family  # family ID
        self.last_birth_interval = last_birth_interval  # only really applies to females who give birth
        self.mother = mother

    def step(self):
        # Aging
        self.check_age_category()  # changes the monkey's age category if they have just aged to a threshold #
        self.age += (1 / 73)

        # Check if an individual is a mother of recently dead infant, and count time since last birth
        if self.unique_id in reproductive_female_list:
            if self.unique_id not in random_mother_list:
                random_mother_list.append(self.unique_id)
            self.check_recent_death_infant()
            self.last_birth_interval += 1 / 73

        # Check if male subgroup needs to break off of main group
        if self.unique_id in male_migration_list:
            new_family_list = new_male_families_dict[new_male_family_counter[-1]]
            for new_male_family in new_family_list:  # extract from list; there should only be 1 value
                self.migrate_to_new_family(new_male_family)
            male_migration_list.remove(self.unique_id)
            if self.unique_id in male_subgroup_list:
                male_subgroup_list.remove(self.unique_id)


        # if a family group is too large, it splits into two
        if self.family.family_size > 46 and self.family.split_flag == 0:  # start splitting/create new family
            new_family_counter.append(new_family_counter[-1] + 1)
            self.family.split_flag = new_family_counter[-1]  # old family split_flag
            old_family_ids.setdefault(self.family.unique_id, []).append(new_family_counter[-1])
            new_family = self.create_new_family()
            new_families_dict.setdefault(new_family_counter[-1], []).append(new_family)

        # if a family group is splitting, monkeys within it are flagged to migrate out
        if self.family.split_flag != 0 and self.family.family_size >= 24:  # join new family/migration
            new_family_id_list = old_family_ids[self.family.unique_id]
            for new_family_id in new_family_id_list:  # extract from list; there should only be 1 value
                new_family_list = new_families_dict[new_family_id]
            for new_family in new_family_list:  # extract from list; there should only be 1 value
                self.migrate_to_new_family(new_family)

        # if a family group is splitting, it stops splitting when the number of individuals is low enough
        if self.family.split_flag != 0 and self.family.family_size < 24:  # stop splitting; remain in family
            self.family.split_flag = 0

        # Birth from the mother's perspective
        if (49 < self.model.step_in_year < 55) \
                and (self.gender == 1 and random.uniform(8, 9) <= self.age <= 25):
            if self.last_birth_interval >= 2:
                self.family.family_size += 1
                self.birth(self.family, self.unique_id)
                self.last_birth_interval = 0

        # Death
        chance = random.uniform(0, 1)  # random decimal # between 0 and 1
        # Currently uses an exponential formula that considers death events as cumulative and dependent.
        # In other words, once a death occurs, it can no longer occur that year.
        # The model runs in time-steps of 5 days each, so there are 73 mortality checks per year.
        # the current formula uses: chance that a monkey does NOT die^73 = survival rate in one year
        # this gives a lower result than a similar formula that considers [yearly mortality rate]/73
        # formula may be changed later
        if self.age <= 1 and chance <= 0.00305:  # 1 - 0.9966; 80% survival; see below
            self.death()
            demographic_structure_list[0] -= 1
            recent_death_infant.append(self.mother)
            # 0.9993^73 = 95% chance to survive each year with ticks every 5 days
            # 0.9987^73 = 91% chance to survive each year with ticks every 5 days
            # 0.99778^73 = 85% chance to survive first year with ticks every 5 days, or 15% yearly mortality
            # 0.99695^73 = 80% chance to survive first year with ticks every 5 days, or 20% yearly mortality
            # 0.9966^73 = 78% chance to survive first year with ticks every 5 days, or 22% yearly mortality

            # if a monkey dies, mother can give birth again the following season
        elif 1 < self.age < 10 and chance <= 0.00043:  # 0.00043 = 1 - 0.99958; 95% survival; see below
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
        elif 10 < self.age <= 30 and self.gender == 0 and chance <= 0.00222:  # 0.00222 = 1 - 0.99778; 85% survival
            # We want a 3:1 male to female ratio, so females will less likely to die and males will be more likely
            self.death()
            if 10 < self.age <= 25:
                demographic_structure_list[4] -= 1
            elif 25 < self.age < 30:
                demographic_structure_list[5] -= 1
                # 0.99778^73 = 85% chance to survive each year with ticks every 5 days
                # 0.9987^73 = 91% chance to survive each year with ticks every 5 days
        elif 10 < self.age <= 30 and self.gender == 1 and chance <= 0.000415:  # 0.000415 = 1 - 0.999585; 97% survival
            self.death()
            if 10 < self.age <= 25:
                demographic_structure_list[4] -= 1
            elif 25 < self.age < 30:
                demographic_structure_list[5] -= 1
                # 0.99778^73 = 85% chance to survive each year with ticks every 5 days
                # 0.9987^73 = 91% chance to survive each year with ticks every 5 days
        elif self.age > 30 and chance <= 0.01245:  # 1 - 0.98755; 40% survival; see below
            self.death()
            demographic_structure_list[5] -= 1
            # 0.99778^73 = 85% chance to survive each year with ticks every 5 days
            # 0.99607^73 = 75% chance to survive each year with ticks every 5 days
            # 0.98755^73 = 40% chance to survive each year with ticks every 5 days

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
                    if self.unique_id not in male_subgroup_list:
                        male_subgroup_list.append(self.unique_id)

            elif self.age_category == 5 and self.gender == 1:  # female becomes too old to give birth
                if self.unique_id in reproductive_female_list:
                    reproductive_female_list.remove(self.unique_id)

    def check_recent_death_infant(self):
        # allow mothers who have recently lost an infant to give birth again in a short period
        if self.unique_id in recent_death_infant:
            self.last_birth_interval = random.uniform(2, 2.4)
            recent_death_infant.remove(self.unique_id)

    def birth(self, parent_family, mother_id):
        # birth from the agent-perspective of the mother agent; creates a new monkey individual
        last = self.model.monkey_id_count
        family = parent_family
        gender = random.randint(0, 1)
        age = 0
        age_category = 0
        if gender == 1:
            last_birth_interval = random.uniform(-10,-7)
            female_list.append(last + 1)
        else:
            last_birth_interval = -9999
            male_maingroup_list.append(last + 1)
        mother = mother_id
        if mother == 0 or mother == '0':
            mother = random.choice(random_mother_list)
        new_monkey = Monkey(last + 1, self.model, gender, age, age_category, family, last_birth_interval,
                            mother)
        new_monkey.family.list_of_family_members.append(new_monkey.unique_id)
        self.model.schedule.add(new_monkey)
        self.model.number_of_monkeys += 1
        self.model.monkey_id_count += 1
        self.model.monkey_birth_count += 1
        demographic_structure_list[0] += 1

    def death(self):
        # death from the perspective of a monkey agent
        self.family.family_size -= 1
        if self.family.family_size == 0:  # if this individual is the last member in their family--for all-male groups
            global_family_id_list.remove(self.family)
            self.model.number_of_families -= 1
            self.model.grid.remove_agent(self.family)
            self.model.schedule.remove(self.family)
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
        self.model.schedule.remove(self)


    def create_new_family(self):
        # a new family group forms when the size of the original group reaches < 45 members
        # this is done from the self perspective, but nothing happens to the individual besides the group forming
        from model import global_family_id_list
        new_family_id = int(global_family_id_list[-1] + 1)  # the new family_id is the latest id + 1
        global_family_id_list.append(new_family_id)
        saved_position = self.family.current_position
        split_flag = 0  # 0 for new family; new families do not start splitting by default
        family_type = 'traditional'
        new_family = Family(new_family_id, self.model, self.family.current_position, 1, [self.unique_id],
                            family_type, saved_position, split_flag)
        self.model.grid.place_agent(new_family, self.family.current_position)
        self.model.schedule.add(new_family)
        self.model.number_of_families += 1
        return new_family

    def migrate_to_new_family(self, new_family):
        # removes and adds self to certain lists, and changes self attributes, to migrate self to a new family
        # this occurs when a male is migrating to an all-male group or a bigger family is splitting into two
        self.family.family_size -= 1
        if self.unique_id in self.family.list_of_family_members:
            self.family.list_of_family_members.remove(self.unique_id)
        self.family = new_family
        self.family.list_of_family_members.append(self.unique_id)
        self.family.family_size += 1
