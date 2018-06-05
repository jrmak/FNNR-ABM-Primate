import random

from mesa.agent import Agent
from maxent import Maxent

demographic_structure_list = [0] * 6
recent_death_infant = []
random_mother_list = []
male_maingroup_list = []
male_subgroup_list = []
female_list = []
reproductive_female_list = [0]

class Family(Agent):
    # the pixel that represents each group of monkeys with the same family id.
    # it moves on the visualization grid, unlike individual monkey agents.
    def __init__(self, unique_id, model, pos, family_size, list_of_family_members, family_type):
        super().__init__(unique_id, model)
        self.pos = pos
        self.family_size = family_size
        self.list_of_family_members = list_of_family_members
        self.family_type = family_type

    def step(self):
        # movement
        from model import masterdict  # can't do this at the beginning
        neig = self.model.grid.get_neighborhood(self.pos, True, False)  # gets neighboring pixels
        poslist = list(self.pos)
        newneig = []
        try:
            for neighbor in neig:
                neighbor = list(neighbor)
                direction_east = poslist[0] - neighbor[0]
                direction_north = poslist[1] - neighbor[1]
                if poslist[0] < 100:
                    neighbor[0] += direction_east * 5
                if poslist[1] < 100:
                    neighbor[1] += direction_north * 5
                neighbor = tuple(neighbor)
                newneig.append(neighbor)
            pos = self.neighbor_choice(newneig, masterdict)
            self.move_to(pos)
        except:
            pass
        if 14 < self.model.step_in_year < 25 or  44 < self.model.step_in_year < 55:
            pos = self.head_to_yangaoping(self.pos)  # chooses from weighted choice
            self.move_to(pos)  # moves to chosen neighboring pixel

        if self.family_size == 0:
            self.model.grid._remove_agent(self.pos, self)

    def head_to_yangaoping(self, pos):
        # moves towards northeast portion of reserve
        pos = list(pos)
        topchoice = random.randint(45, 75)
        eastchoice = random.randint(45, 80)
        if pos[0] < eastchoice:
            pos[0] += 5
        if pos[1] < topchoice:
            pos[1] += 5
        else:
            pass
            if pos[0] > 104:
                pos[0] = 99
            if pos[1] > 104:
                pos[1] = 99
        pos = tuple(pos)
        return pos

    def neighbor_choice(self, neighborlist, neighbordict):
        # agent chooses a neighbor to move to based on weights
        choicelist = []
        # picks a weighted neighbor to move to

        color = None
        weight = None
        neighborcolor = []
        for ng in neighborlist:
            if color != None:
                neighborcolor.append(color)
            for nposlist in neighbordict.values():
                for n in nposlist:
                    if ng == n:
                        color = list(neighbordict.keys())[list(neighbordict.values()).index(nposlist)]
        if color != None:
            neighborcolor.append(color)

        # sets weights
        for color in neighborcolor:
            if color == 'Red':  # elevation 1900+
                weight = 1
            elif color == 'Orange':  # elevation 1700-1900
                weight = 11
            elif color == 'Yellow':  # elevation 1500-1700
                weight = 5
            elif color == 'Green':  # elevation 1300-1500
                weight = 10
            elif color == 'Blue':  # elevation 1100-1300
                weight = 7
            elif color == 'Purple':  # elevation 900-1100
                weight = 1
            elif color == 'Black':  # elevation 900-
                weight = 0.1
            elif color == 'Gray':  # elevation -9999, outside FNNR
                weight = 0
            choicelist.append(weight)
        if choicelist != [] and choicelist != [0, 0, 0, 0, 0, 0, 0, 0]:
            try:
                # this takes care of edges
                while len(choicelist) < 8:
                    choicelist.append(0)

                # random choice plays a role, but each neighbor choice is affected by weights
                # the next few dozen lines determine which weighted % category the random choice falls into
                chance = random.uniform(0, 1)
                oldsum = 0
                newsum = choicelist[1] / sum(choicelist)
                if oldsum < chance < newsum:
                    direction = neighborlist[1]  # north neighbor
                oldsum = newsum
                newsum += choicelist[6] / sum(choicelist)
                if oldsum < chance < newsum:
                    direction = neighborlist[6]  # south neighbor
                oldsum = newsum
                newsum += choicelist[3] / sum(choicelist)
                if oldsum < chance < newsum:
                    direction = neighborlist[3]  # west neighbor
                oldsum = newsum
                newsum += choicelist[4] / sum(choicelist)
                if oldsum < chance < newsum:
                    direction = neighborlist[4]  # east neighbor
                oldsum = newsum
                newsum += choicelist[0] / sum(choicelist)
                if oldsum < chance < newsum:
                    direction = neighborlist[0]  # northwest neighbor
                oldsum = newsum
                newsum += choicelist[2] / sum(choicelist)
                if oldsum < chance < newsum:
                    direction = neighborlist[2]  # northeast neighbor
                oldsum = newsum
                newsum += choicelist[3] / sum(choicelist)
                if oldsum < chance < newsum:
                    direction = neighborlist[5]  # southwest neighbor
                oldsum = newsum
                newsum += choicelist[7] / sum(choicelist)
                if oldsum < chance < newsum:
                    direction = neighborlist[7]  # southeast neighbor
                return direction
            except:
                pass

    def move_to(self, pos):
        if pos != None:
            self.model.grid.move_agent(self, pos)

class Monkey(Family):

    def __init__(self, unique_id, model, pos, family_size, list_of_family_members, family_type,
                 gender, age, age_category, family_id, last_birth_interval, mother, death_flag):
        super().__init__(unique_id, model, pos, family_size, list_of_family_members, family_type)
        self.gender = gender
        self.age = age
        self.age_category = age_category
        self.family_id = family_id
        self.last_birth_interval = last_birth_interval
        self.mother = mother
        self.death_flag = death_flag

    def step(self):

        if self.death_flag == 0:

            # Aging
            self.age += (1/73)
            self.check_age_category()

            # Check if mother of recently dead infant and count time since last birth
            if self.unique_id in reproductive_female_list:
                if self.unique_id not in random_mother_list:
                    random_mother_list.append(self.unique_id)
                self.check_recent_death_infant()
                self.last_birth_interval += 1/73

            # Check if male subgroup needs to break off of main group
            self.create_male_subgroup()

            # Birth
            if (18 < self.model.step_in_year < 25) or (48 < self.model.step_in_year < 55)   \
                and (self.gender == 1 and 10 <= self.age <= 25):
                if self.last_birth_interval >= 3:
                    self.family_size += 1
                    self.birth(self.pos, self.family_size, self.family_id, self.unique_id, self.list_of_family_members)
                    self.last_birth_interval = 0

            # Death
            chance = random.uniform(0, 1)
            # formula may be fixed later
            if self.age <= 1 and chance <= 0.00305:
                self.death()
                demographic_structure_list[0] -= 1
                recent_death_infant.append(self.mother)
                # 0.99695^73 = 80% chance to survive first year with ticks every 5 days
                # if a monkey dies, mother can give birth again the following season
            elif 1 < self.age < 10 and chance <= 0.0007:
                self.death()
                if 1 < self.age <= 3:
                    demographic_structure_list[1] -= 1
                elif 3 < self.age <= 7:
                    demographic_structure_list[2] -= 1
                elif 7 < self.age <= 10:
                    demographic_structure_list[3] -= 1
                # 0.9993^73 = 95% chance to survive each year with ticks every 5 days
            elif 10 < self.age <= 30 and chance <= 0.0013:
                self.death()
                if 10 < self.age <= 25:
                    demographic_structure_list[4] -= 1
                elif 25 < self.age < 30:
                    demographic_structure_list[5] -= 1
                # 0.9987^73 = 91% chance to survive each year with ticks every 5 days
            elif self.age > 30 and chance <= 0.00393:
                self.death()
                demographic_structure_list[5] -= 1
                # 0.99607^73 = 75% chance to survive each year with ticks every 5 days

        else:
            pass

    def check_age_category(self):
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
                reproductive_female_list.remove(self.unique_id)

    def check_recent_death_infant(self):
        if self.unique_id in recent_death_infant:
            self.last_birth_interval = random.uniform(2, 2.5)
            recent_death_infant.remove(self.unique_id)

    def birth(self, parent_pos, new_family_size, parent_family, mother_id, list_of_family):
        # birth from the perspective of a new monkey agent
        last = self.model.monkey_id_count
        pos = parent_pos
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
        death_flag = 0
        new_monkey = Monkey(last + 1, self.model, pos, family_size, list_of_family_members, family_type,
                            gender, age, age_category, family_id, last_birth_interval, mother, death_flag)
        self.model.schedule.add(new_monkey)
        self.model.number_of_monkeys += 1
        self.model.monkey_id_count += 1
        self.model.monkey_birth_count += 1
        demographic_structure_list[0] += 1

    def death(self):
        # death from the perspective of a monkey agent
        self.death_flag = 1
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
        # breaks off
        if len(male_subgroup_list) > random.randint(10, 15):
            from model import global_family_id_list
            new_family_id = int(global_family_id_list[-1] + 1)
            global_family_id_list.append(new_family_id)
            family_type = 'all_male'
            male_family = Family(new_family_id, self.model, self.pos, len(male_subgroup_list), male_subgroup_list,
                                 family_type)
            self.model.grid.place_agent(male_family, self.pos)
            self.model.schedule.add(male_family)
            del male_subgroup_list[:]


# environmental pixels

class Red(Maxent):

    min_elev = 1899
    max_elev = 3000

class Orange(Maxent):

    min_elev = 1699
    max_elev = 1900

class Yellow(Maxent):

    min_elev = 1499
    max_elev = 1700

class Green(Maxent):

    min_elev = 1299
    max_elev = 1500

class Blue(Maxent):

    min_elev = 1099
    max_elev = 1300

class Purple(Maxent):

    min_elev = 899
    max_elev = 1100

class Black(Maxent):

    min_elev = 0
    max_elev = 900

class Gray(Maxent):

    min_elev = -10000
    max_elev = -9998
