import random

from mesa.agent import Agent
from maxent import Maxent

demographic_structure_list = [0] * 6
recent_death_infant = []
random_mother_list = []

class Family(Agent):
    # the pixel that represents each group of monkeys with the same family id.
    # it moves on the visualization grid, unlike individual monkey agents.
    def __init__(self, unique_id, model, pos, family_size):
        super().__init__(unique_id, model)
        self.pos = pos
        self.family_size = family_size

    def step(self):
        # movement
        from model import masterdict  # can't do this at the beginning
        neig = self.model.grid.get_neighborhood(self.pos, True, False)
        pos = self.neighbor_choice(neig, masterdict)
        # pos = random.choice(neig)
        self.move_to(pos)

        if self.family_size == 0:
            self.model.grid._remove_agent(self.pos, self)

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
        for color in neighborcolor:
            if color == 'Red':  # elevation 1900+
                weight = 1
            elif color == 'Orange':  # elevation 1700-1900
                weight = 11
            elif color == 'Yellow':  # elevation 1500-1700
                weight = 1
            elif color == 'Green':  # elevation 1300-1500
                weight = 4
            elif color == 'Blue':  # elevation 1100-1300
                weight = 10
            elif color == 'Purple':  # elevation 900-1100
                weight = 3
            elif color == 'Black':  # elevation 900-
                weight = 1
            elif color == 'Gray':  # elevation -9999, outside FNNR
                weight = 0
            choicelist.append(weight)
        if choicelist != [] and choicelist != [0, 0, 0, 0, 0, 0, 0, 0]:
            try:
                # the below takes care of edges
                while len(choicelist) < 8:
                    choicelist.append(0)
                # random choice plays a role, but is affected by weights
                chance = random.uniform(0, 1)
                oldsum = 0
                newsum = choicelist[1] / sum(choicelist)
                if oldsum < chance < newsum:
                    direction = neighborlist[1]
                oldsum = newsum
                newsum += choicelist[6] / sum(choicelist)
                if oldsum < chance < newsum:
                    direction = neighborlist[6]
                oldsum = newsum
                newsum += choicelist[3] / sum(choicelist)
                if oldsum < chance < newsum:
                    direction = neighborlist[3]
                oldsum = newsum
                newsum += choicelist[4] / sum(choicelist)
                if oldsum < chance < newsum:
                    direction = neighborlist[4]
                oldsum = newsum
                newsum += choicelist[0] / sum(choicelist)
                if oldsum < chance < newsum:
                    direction = neighborlist[0]
                oldsum = newsum
                newsum += choicelist[2] / sum(choicelist)
                if oldsum < chance < newsum:
                    direction = neighborlist[2]
                oldsum = newsum
                newsum += choicelist[3] / sum(choicelist)
                if oldsum < chance < newsum:
                    direction = neighborlist[3]
                oldsum = newsum
                newsum += choicelist[7] / sum(choicelist)
                if oldsum < chance < newsum:
                    direction = neighborlist[7]
                return direction
            except:
                pass

    def move_to(self, pos):
        if pos != None:
            self.model.grid.move_agent(self, pos)

    def assign_family(self, member_id):
        self.member = member_id
        member_id.family_id = self.unique_id

class Monkey(Family):

    def __init__(self, unique_id, model, pos, family_size, gender, age, age_category, family_id,
                 last_birth_interval, mother):
        super().__init__(unique_id, model, pos, family_size)
        self.gender = gender
        self.age = age
        self.age_category = age_category
        self.family_id = family_id
        self.last_birth_interval = last_birth_interval
        self.mother = mother

    def step(self):

        # to-do list:
        # ! screenshot and print elevation legend
        # ! modify height and width of grid to be mutable

        # Aging
        self.check_age_category()

        if (self.gender == 1 and 10 <= self.age <= 25):
            random_mother_list.append(self.unique_id)

        # Check if mother of recently dead infant
        if (self.gender == 1 and 10 <= self.age <= 25):
            self.check_recent_death_infant()

        # Birth
        if (self.gender == 1 and 10 <= self.age <= 25):
            if self.last_birth_interval >= 3:
                self.family_size += 1
                self.birth(self.pos, self.family_size, self.family_id, self.unique_id)
                self.last_birth_interval = 0

        # Death
        chance = random.uniform(0, 1)
        if self.age <= 1 and chance <= 0.00305:
            self.death()
            recent_death_infant.append(self.mother)
            # 0.99695^73 = 80% chance to survive first year with ticks every 5 days
            # later add: find mother for immediate rebirthing
        elif 1 < self.age < 8 and chance <= 0.0007:
            self.death()
            # 0.9993^73 = 95% chance to survive each year with ticks every 5 days
        elif 8 < self.age < 10 and chance <= 0.0013:
            self.death()
            # 0.9987^73 = 91% chance to survive each year with ticks every 5 days
        elif 10 < self.age < 25 and chance <= 0.00025:
            self.death()
            # 0.99975^73 = 98% chance to survive each year with ticks every 5 days
        elif self.age > 25 and chance <= 0.0039:
            self.death()
            # 0.9961^73 = 75% chance to survive each year with ticks every 5 days
        elif self.age > 30 and chance <= 0.0218:
            self.death()
            # 0.9782^73 = 20% chance to survive each year with ticks every 5 days

        self.age += (1/73)
        self.last_birth_interval += 1/73

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

    def check_recent_death_infant(self):
        if self.unique_id in recent_death_infant:
            self.last_birth_interval = 2.2
            recent_death_infant.remove(self.unique_id)

    def birth(self, parent_pos, new_family_size, parent_family, mother_id):
        # birth from the perspective of a new monkey agent
        last = self.model.number_of_monkeys
        pos = parent_pos
        family_size = new_family_size
        gender = random.randint(0, 1)
        age = 0
        age_category = 0
        family_id = parent_family
        last_birth_interval = 0
        mother = mother_id
        if mother == 0:
            mother = random.choice(random_mother_list)
        new_monkey = Monkey(last + 1, self.model, pos, family_size, gender, age, age_category, family_id,
                            last_birth_interval, mother)
        self.model.schedule.add(new_monkey)
        self.model.number_of_monkeys += 1
        self.model.monkey_birth_count += 1

    def death(self):
        # death from the perspective of a monkey agent
        self.model.schedule.remove(self)
        self.model.number_of_monkeys -= 1
        self.model.monkey_death_count += 1


# environmental pixels

class Red(Maxent):

    seed = 0.005
    min_elev = 1899
    max_elev = 3000

class Orange(Maxent):

    seed = 0.005
    min_elev = 1699
    max_elev = 1900

class Yellow(Maxent):

    seed = 0.01
    min_elev = 1499
    max_elev = 1700

class Green(Maxent):

    seed = 0.01
    min_elev = 1299
    max_elev = 1500

class Blue(Maxent):

    seed = 0.01
    min_elev = 1099
    max_elev = 1300

class Purple(Maxent):

    seed = 0.01
    min_elev = 899
    max_elev = 1100

class Black(Maxent):

    seed = 0.001
    min_elev = 0
    max_elev = 900

class Gray(Maxent):

    seed = 0.001
    min_elev = -10000
    max_elev = -9998
