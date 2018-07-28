# !/usr/bin/python

"""
This file determines behavior for family agents in the visualization grid.
"""

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
    def __init__(self, unique_id, model, current_position, family_size, list_of_family_members, family_type,
                 saved_position, split_flag):
        super().__init__(unique_id, model)
        self.current_position = current_position
        self.family_size = family_size
        self.list_of_family_members = list_of_family_members
        self.family_type = family_type
        self.saved_position = saved_position
        self.split_flag = split_flag

    def step(self):
        # movement rules for each pixel-agent at each step

        # loads environmental grid; it differs depending on whether or not human settlements are on the grid
        load_dict = {}
        if self.model.grid_type == 'with_humans':
            masterdict = self.model.saveLoad(load_dict, 'masterdict_veg', 'load')
        elif self.model.grid_type == 'without_humans':
            masterdict = self.model.saveLoad(load_dict, 'masterdict_without_humans', 'load')
        # print(self.model.grid_type)
        # Movement for families is defined below

        if 16 < self.model.step_in_year < 25 or 46 < self.model.step_in_year < 55:  # head to Yangaoping for Apr/Sept
            # April: steps 19-25
            # September: steps 49-55
            yangaoping = [random.randint(50, 70), random.randint(70, 90)]
            # The grid is drawn from the bottom, so even though it is currently 85 x 100,
            # these numbers are relatively high because they indicate the top right corner of the grid
            for i in range(random.randint(5, 10)):  # the monkeys move multiple pixels each step, not just one
                self.move_to_point(self.current_position, yangaoping)
                if self.current_position in masterdict['Elevation_Out_of_Bound'] or  \
                    self.current_position in masterdict['Outside_FNNR']:
                    # the movement formula may land the monkeys in territory where they cannot move.
                    # this territory is not very common, so if that occurs, the monkeys simply keep moving.
                    for i in range(random.randint(5, 10)):  # the monkeys move multiple pixels each step, not just one.
                        # the range is 5 because each step at the 85x100 resolution is approximately 300m in resolution.
                        # According to the pseudocode, monkeys move up to 2500m (not in a straight line) every 5 days.
                        self.move_to_point(self.current_position, yangaoping)
                        if self.current_position is not None:
                            moved_list.append(self.current_position)  # moved_list records positions for the heatmap
                else:
                    if self.current_position is not None:
                        moved_list.append(self.current_position)  # moved_list records positions for the heatmap

        elif 26 < self.model.step_in_year < 34 or 56 < self.model.step_in_year < 64:  # head back to rest of reserve
            # after breeding season ends, head away from Yangaoping
            rest_of_reserve = {}
            if self.model.run_type == 'first_run':
                rest_of_reserve = masterdict['Broadleaf'] + masterdict['Mixed']  \
                                         + masterdict['Deciduous']
                for coordinate in masterdict['Elevation_Out_of_Bound'] + masterdict['Household'] + masterdict['PES'] \
                        + masterdict['Farm'] + masterdict['Forest']:
                    if coordinate in rest_of_reserve:
                        rest_of_reserve.remove(coordinate)  # only set acceptable (non-human) destinations
                self.model.saveLoad(rest_of_reserve, 'rest_of_reserve_dict', 'save')
            rest_of_reserve = self.model.saveLoad(rest_of_reserve, 'rest_of_reserve_dict', 'load')
            rest_of_reserve_choice = random.choice(rest_of_reserve)
            center = [50, 50]
            for i in range(random.randint(5, 10)):  # when returning to the rest of the reserve after Yangaoping
                self.move_to_point(self.current_position, rest_of_reserve_choice)
                if self.current_position in masterdict['Elevation_Out_of_Bound'] or  \
                    self.current_position in masterdict['Outside_FNNR']:
                    # the movement formula may land the monkeys in territory where they cannot move.
                    # this territory is not very common, so if that occurs, the monkeys simply keep moving.
                    for i in range(random.randint(5, 10)):  # the monkeys move multiple pixels each step, not just one
                        self.move_to_point(self.current_position, center)
                        if self.current_position is not None:
                            moved_list.append(self.current_position)  # moved_list records positions for the heatmap
                else:
                    if self.current_position is not None:
                        moved_list.append(self.current_position)  # moved_list records positions for the heatmap

        else:
            # When it is not about to be breeding season/during it/just past it, move according to vegetation
            if self.current_position in masterdict['Elevation_Out_of_Bound']:
                center = [50, 50]
                for i in range(random.randint(5, 10)):
                    self.move_to_point(self.current_position, center)
                if self.current_position in masterdict['Elevation_Out_of_Bound']:  # still
                    center = [50, 50]
                    for i in range(random.randint(5, 10)):
                        self.move_to_point(self.current_position, center)
            for i in range(random.randint(5, 10)):
                neig = self.model.grid.get_neighborhood(self.current_position, True, False)
                current_position = self.neighbor_choice(neig, masterdict)
                from humans import human_avoidance_list
                if current_position not in human_avoidance_list:
                    self.move_to(current_position)
                    if current_position is not None:
                        self.current_position = current_position
                        moved_list.append(self.current_position)  # moved_list records positions for the heatmap

        if self.current_position is not None:
            moved_list.append(self.current_position)  # moved_list records positions for the heatmap

    def move_to_point(self, current_position, new_position):
        current_position = list(current_position)  # current position
        if current_position[0] < new_position[0]:  # if the current position is away from Yaogaoping,
            current_position[0] = current_position[0] + 1  # move it closer
        elif current_position[0] == new_position[0]:
            pass
        else:
            current_position[0] = current_position[0] - 1

        if current_position[1] < new_position[1]:
            current_position[1] = current_position[1] + 1
        elif current_position[1] == new_position[1]:
            pass
        else:
            current_position[1] = current_position[1] - 1
        current_position = tuple(current_position)
        from humans import human_avoidance_list
        if current_position not in human_avoidance_list:
            self.move_to(current_position)
            self.current_position = current_position

    def check_vegetation_of_neighbor(self, neighborlist, neighbordict):
        # returns a list of neighbors as vegetation
        neighbor_veg = {}
        neighbor_veg_list = []
        for neighbor in neighborlist:
            for nposlist in neighbordict.values():  # from all the grid values, find neighbors for this particular grid
                for neighbor_position in nposlist:  # in order to find out neighbor's vegetation -> neighbor's weighted
                    if neighbor == neighbor_position:  # value -> selected neighbor to move to.
                        vegetation = list(neighbordict.keys())[list(neighbordict.values()).index(nposlist)]
                        neighbor_veg.setdefault(neighbor, []).append(vegetation)
        for list_of_values in neighbor_veg.values():
            if len(list_of_values) > 1:  # if there is more than one land type at that grid,
                for value in list_of_values:
                    if value != 'Elevation_Out_of_Bound' and value != 'Outside_FNNR' \
                            and value != 'PES' and value != 'Forest' and value != 'Farm'\
                            and value != 'Household':
                        if len(list_of_values) > 1:  # checking again in case this loops multiple times
                            list_of_values.remove(value)
                        # Vegetation is considered the bottom layer, so in case of a conflict, it is removed.
                    elif value == 'Outside_FNNR':
                        list_of_values = ['Outside_FNNR']  # Otherwise, Outside_FNNR is the defining layer;
                    elif value == 'Elevation_Out_of_Bound':
                        list_of_values = ['Elevation_Out_of_Bound']  # then the other layers follow in order of
                    elif value == 'Household':  # formation.
                        list_of_values = ['Household']
                    elif value == 'Farm':
                        list_of_values = ['Farm']
                    elif value == 'PES':
                        list_of_values = ['PES']
                    elif value == 'Forest':
                        list_of_values = ['Forest']
            for value in list_of_values:
                neighbor_veg_list.append(value)
        return neighbor_veg_list

    def neighbor_choice(self, neighborlist, neighbordict):
        # agent chooses a neighbor to move to based on weights
        choicelist = []
        # picks a weighted neighbor to move to
        # neighbordict is a dictionary with all vegetation categories and their corresponding grid values
        # neighborlist is a list of 8-cell neighbors to the current position
        neighbor_veg = self.check_vegetation_of_neighbor(neighborlist, neighbordict)
        # weights below were taken from the pseudocode
        for vegetation in neighbor_veg:
            if vegetation == 'Elevation_Out_of_Bound':
                weight = 0
            elif vegetation == 'Bamboo':
                weight = 0.8
            elif vegetation == 'Coniferous':
                weight = 1
            elif vegetation == 'Broadleaf':
                weight = 1
            elif vegetation == 'Mixed':
                weight = 1
            elif vegetation == 'Lichen':
                weight = 0.8
            elif vegetation == 'Deciduous':
                weight = 1
            elif vegetation == 'Shrublands':
                weight = 0.8
            elif vegetation == 'Clouds':
                weight = random.uniform(0, 1)
            elif vegetation == 'Farmland':
                weight = 0
            elif vegetation == 'Outside_FNNR':
                weight = 0
            elif vegetation == 'Household':
                weight = 0
            elif vegetation == 'Farm':
                weight = 0.05
            elif vegetation == 'PES':
                weight = 0.2
            elif vegetation == 'Forest':
                weight = 0.3
            choicelist.append(weight)

        if choicelist != [] and choicelist != [0, 0, 0, 0, 0, 0, 0, 0]:
            # this takes care of edges
            while len(choicelist) < 8:
                choicelist.append(0)
            # random choice plays a role, but each neighbor choice is affected by weights
            # the next few dozen lines determine which weighted % category the random choice falls into

            # For example: if the relative weight of the north neighbor was 0.16 (with the sum of all weights
            # equaling 1) and the relative weight of the south neighbor was 0.08, then oldsum < chance < newsum
            # for the north neighbor would be 0 < x (random decimal from 0 to 1) < 0.16, and oldsum < chance < newsum
            # for the south neighbor follows that, from 0.16 < x < 0.24. The exact order does not matter; for the
            # north neighbor, whose relative weight is 0.16, we could also write something like 0.08 < x < 0.24
            # after assessing the weight of the south neighbor first (0 < x < 0.08), so long as the range (difference
            # between high and low values) for the north neighbor was 0.16, etc.
            #  and all of the continuous ranges summed up to 16.

            # a new weighted-choice function in Python 3.6 eliminates the need for this formula; however,
            # this project will not chnage its dependencies at this point.
            chance = random.uniform(0, 1)

            oldsum = 0
            newsum = choicelist[1] / sum(choicelist)  # defines the relative weight of the north neighbor
            if oldsum < chance < newsum:  # if the randomly-chosen number falls into this weight's range,
                direction = neighborlist[1]  # the north neighbor is selected
            oldsum = newsum
            newsum += choicelist[6] / sum(choicelist)  # defines the relative weight of the south neighbor
            if oldsum < chance < newsum:  # if the randomly-chosen number falls into this weight's range,
                direction = neighborlist[6]  # the south neighbor is selected
            oldsum = newsum
            newsum += choicelist[3] / sum(choicelist)  # defines the relative weight of the west neighbor
            if oldsum < chance < newsum:  # if the randomly-chosen number falls into this weight's range,
                direction = neighborlist[3]  # the west neighbor is selected
            oldsum = newsum
            newsum += choicelist[4] / sum(choicelist)  # defines the relative weight of the east neighbor
            if oldsum < chance < newsum:  # if the randomly-chosen number falls into this weight's range,
                direction = neighborlist[4]  # the east neighbor is selected
            oldsum = newsum
            newsum += choicelist[0] / sum(choicelist)  # defines the relative weight of the northwest neighbor
            if oldsum < chance < newsum:  # if the randomly-chosen number falls into this weight's range,
                direction = neighborlist[0]  # the northwest neighbor is selected
            oldsum = newsum
            newsum += choicelist[2] / sum(choicelist)  # defines the relative weight of the northeast neighbor
            if oldsum < chance < newsum:  # if the randomly-chosen number falls into this weight's range,
                direction = neighborlist[2]  # the northeast neighbor is selected
            oldsum = newsum
            newsum += choicelist[5] / sum(choicelist)  # defines the relative weight of the southwest neighbor
            if oldsum < chance < newsum:  # if the randomly-chosen number falls into this weight's range,
                direction = neighborlist[5]  # the southwest neighbor is selected
            oldsum = newsum
            newsum += choicelist[7] / sum(choicelist)  # defines the relative weight of the southeast neighbor
            if newsum != 1 and newsum > 0.999:
                newsum = 1
            if oldsum < chance < newsum:  # if the randomly-chosen number falls into this weight's range,
                direction = neighborlist[7]  # the southeast neighbor is selected
            try:
                assert int(newsum) == 1
            except AssertionError:
                direction = self.current_position
            return direction

    def move_to(self, current_position):
        if current_position != None:
            self.model.grid.move_agent(self, current_position)