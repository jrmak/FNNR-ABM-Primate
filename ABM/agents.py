# !/usr/bin/python

from mesa.agent import Agent
import random

demographic_structure_list = [0] * 6  # each index represents an age category count: 0-1, 1-3, 3-7, 7-10, 10-25, 25+
recent_death_infant = []  # lists ids of mothers who can give birth soon after their infant has died early
random_mother_list = []  # for assigning random 'rebirth'-ready mothers for the first-generation infants to die
male_maingroup_list = []  # lists ids of all males in the main group
male_subgroup_list = []  # lists ids of all males in the all-male subgroup broken off from the main group
female_list = []  # lists ids of all females
reproductive_female_list = [0]  # lists ids of all females aged 10-25
moved_list = []  # records all points moved to; used for calculating heatmap


class Family(Agent):
    # the pixel that represents each group of monkeys with the same family id.
    # it moves on the visualization grid, unlike individual monkey agents.
    # it is currently not important in the demographic model, just the visualization model.
    def __init__(self, unique_id, model, pos, family_size, list_of_family_members, family_type):
        super().__init__(unique_id, model)
        self.pos = pos
        self.family_size = family_size
        self.list_of_family_members = list_of_family_members
        self.family_type = family_type

    def step(self):
        # movement rules for each pixel-agent at each step
        load_dict = {}
        empty_masterdict = self.model.saveLoad(load_dict, 'masterdict_elevation', 'load')
        neig = self.model.grid.get_neighborhood(self.pos, True, False)  # gets neighboring pixels
        selfposlist = list(self.pos)
        newneig = []

        # below sets movement behaviors for monkeys outside of mating season
        from model import filename  # can't import at the beginning - import statement must be here
        cell_height = self.model._readASCII(filename)[1]
        # sets position for pixels to move to - every step (5 days), they move some grids in a chosen direction
        for neighbor in neig:  # this block of code dictates that multiple grids are traveled per step
            neighbor = list(neighbor)
            direction_east = selfposlist[0] - neighbor[0]  # if positive, direction is east; if negative, west
            direction_north = selfposlist[1] - neighbor[1]  # if positive, direction is north; if negative, south
            # direction_east and direction_north are always either -1, 0, or 1
            if selfposlist[0] < cell_height * 0.6:  # if the position isn't too far, it can potentially go east or west
                neighbor[0] += direction_east * random.randint(int(cell_height * 0.05), int(cell_height * 0.1))

            if selfposlist[1] < cell_height * 0.7 and selfposlist[0] > cell_height * 0.3:  # or north and south
                neighbor[1] += direction_north * random.randint(int(cell_height * 0.05), int(cell_height * 0.1))
            elif selfposlist[1] < cell_height * 0.7 and selfposlist[0] < cell_height * 0.3:
                neighbor[1] += direction_north

            neighbor = tuple(neighbor)
            newneig.append(neighbor)
        pos = self.neighbor_choice(newneig, empty_masterdict)  # this function determines where to move (which neighbor)


        if 16 < self.model.step_in_year < 25 or  46 < self.model.step_in_year < 55:  # head to Yangaoping for Apr/Sept
            # April: steps 19-25
            # September: steps 49-55
            pos = self.move_to_yangaoping(self.pos, cell_height)

        if 28 < self.model.step_in_year < 31 or 58 < self.model.step_in_year < 61: # head back to rest of reserve
            self.move_to(pos)  # moves to chosen direction/neighbor
            pos = self.move_from_yangaoping(self.pos, cell_height)

        self.move_to(pos)  # moves to chosen direction/neighbor
        moved_list.append(pos)
        if self.family_size == 0:
            self.model.grid._remove_agent(self.pos, self)  # if everyone in a family dies, the pixel is removed

    def move_to_yangaoping(self, pos, height):
        # moves towards northeast portion of reserve
        pos = list(pos)
        northchoice = random.randint(int(height * 0.8), int(height * 0.85))  # numbers determined by proportion to grid
        eastchoice = random.randint(int(height * 0.6), int(height * 0.7))
        if pos[0] < eastchoice:  # if the current position is not too close to the edge of the grid,
            pos[0] += random.randint(int(height * 0.1), int(height * 0.2))  # move around 6-8 spaces (for 87x100) east
        if pos[1] < northchoice:
            pos[1] += random.randint(int(height * 0.1), int(height * 0.2)) # and also north
        else:
            if pos[0] > random.uniform(height * 0.7, height * 0.8):
                pos[0] = random.randint(int(height * 0.6), int(height * 0.65))
            if pos[1] > random.uniform(height * 0.7, height * 0.8):
                pos[1] = random.randint(int(height * 0.6), int(height * 0.75))
        pos = tuple(pos)
        return pos

    def move_from_yangaoping(self, pos, height):
        # moves away from northeast portion of reserve
        pos = list(pos)
        southchoice = random.uniform(int(height * 0.2), int(height * 0.3))
        westchoice = random.uniform(int(height * 0.2), int(height * 0.3))
        if pos[0] > westchoice:
            pos[0] -= random.randint(int(height * 0.1), int(height * 0.2))
        if pos[1] > southchoice:
            pos[1] -= random.randint(int(height * 0.1), int(height * 0.2))
        else:
            pass
            if pos[0] < height * 0.3:  # 29
                pos[0] = random.randint(int(height * 0.3), int(height * 0.4))
            if pos[1] < height * 0.3:
                pos[1] = random.randint(int(height * 0.3), int(height * 0.4))
        pos = tuple(pos)
        return pos


    def neighbor_choice(self, neighborlist, neighbordict):
        # agent chooses a neighbor to move to based on weights
        choicelist = []
        # picks a weighted neighbor to move to
        from model import setting
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

        # sets weights - elevation only - adjustable
        for color in neighborcolor:
            if setting == 'elevation':
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

            elif setting == 'maxent':
            # sets weight for maxent
                if color == 'Shade1':  # lowest maxent suitability/darkest shade of grey (black)
                    weight = 0.01
                elif color == 'Shade2':
                    weight = 0.1
                elif color == 'Shade3':
                    weight = 1
                elif color == 'Shade4':
                    weight = 5
                elif color == 'Shade5':
                    weight = 10
                elif color == 'Shade6':
                    weight = 15
                elif color == 'Shade7':  # highest maxent suitability/lightest shade of grey (white)
                    weight = 20
                elif color == 'Shade8':  # -9999 values; represents boundaries outside of FNNR
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

    #  while Family agents move on the visualization grid, Monkey agents follow demographic-based actions
    #  such as being born, aging, mating, dying, etc. in a different submodel

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
            self.age += (1/73)  # every step is 5 days, or 1/73rd of a year
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
            # Currently uses an exponential formula that considers death events as cumulative and dependent.
            # In other words, once a death occurs, it can no longer occur that year.
            # The model runs in time-steps of 5 days each, so there are 73 mortality checks per year.
            # the current formula uses: chance that a monkey does NOT die^73 = survival rate in one year
            # this gives a lower result than a similar formula that considers [yearly mortality rate]/73
            # formula may be changed later
            if self.age <= 1 and chance <= 0.0007: # 0.0007 = 1 - 0.9993; see below
                self.death()
                demographic_structure_list[0] -= 1
                recent_death_infant.append(self.mother)
                # 0.9993^73 = 95% chance to survive each year with ticks every 5 days
                # 0.9987^73 = 91% chance to survive each year with ticks every 5 days
                # 0.99778^73 = 85% chance to survive first year with ticks every 5 days, or 15% yearly mortality
                # 0.99695^73 = 80% chance to survive first year with ticks every 5 days, or 20$ yearly mortality
                # if a monkey dies, mother can give birth again the following season
            elif 1 < self.age < 10 and chance <= 0.00043:  # 0.00043 = 1 - 0.99958; see below
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
            elif 10 < self.age <= 30 and chance <= 0.0013:  # 0.0013 = 1 - 0.9987; see below
                self.death()
                if 10 < self.age <= 25:
                    demographic_structure_list[4] -= 1
                elif 25 < self.age < 30:
                    demographic_structure_list[5] -= 1
                # 0.99778^73 = 85% chance to survive each year with ticks every 5 days
                # 0.9987^73 = 91% chance to survive each year with ticks every 5 days
            elif self.age > 30 and chance <= 0.00222:  # 0.00222 = 1 - 0.99778; see below
                self.death()
                demographic_structure_list[5] -= 1
                # 0.99778^73 = 85% chance to survive each year with ticks every 5 days
                # 0.99607^73 = 75% chance to survive each year with ticks every 5 days
            else:
                pass

        else:
            print('schedule')
            pass

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

    def birth(self, parent_pos, new_family_size, parent_family, mother_id, list_of_family):
        # birth from the agent-perspective of the new monkey agent
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
        # male subgroup forms a new family and shows up in the visualization under a new, differently-colored pixel
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