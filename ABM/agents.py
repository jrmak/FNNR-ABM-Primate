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
                 saved_position):
        super().__init__(unique_id, model)
        self.current_position = current_position
        self.family_size = family_size
        self.list_of_family_members = list_of_family_members
        self.family_type = family_type
        self.saved_position = saved_position

    def step(self):
        # movement rules for each pixel-agent at each step
        load_dict = {}
        masterdict = self.model.saveLoad(load_dict, 'masterdict_veg', 'load')

        # Movement for families is defined below

        if 16 < self.model.step_in_year < 25 or 46 < self.model.step_in_year < 55:  # head to Yangaoping for Apr/Sept
            # April: steps 19-25
            # September: steps 49-55
            yangaoping = [random.randint(50, 70), random.randint(70, 80)]
            # The grid is drawn from the bottom, so even though it is currently 85 x 100,
            # these numbers are relatively high because they indicate the top right corner of the grid
            for i in range(random.randint(5, 10)):  # the monkeys move multiple pixels each step, not just one
                current_position = self.move_to_point(yangaoping)
                if current_position in masterdict['Elevation_Out_of_Bound'] or  \
                    current_position in masterdict['Outside_FNNR']:
                    for i in range(random.randint(5, 10)):  # the monkeys move multiple pixels each step, not just one
                        current_position = self.move_to_point(yangaoping)

        elif 26 < self.model.step_in_year < 30 or 56 < self.model.step_in_year < 60:  # head back to rest of reserve
            # after breeding season ends, head away from Yangaoping
            rest_of_reserve = {}
            """
            rest_of_reserve = masterdict['Broadleaf'] + masterdict['Mixed']  \
                                     + masterdict['Deciduous']
            for coordinate in masterdict['Elevation_Out_of_Bound'] + masterdict['Household'] + masterdict['PES'] \
                    + masterdict['Farm'] + masterdict['Forest']:
                if coordinate in rest_of_reserve:
                    rest_of_reserve.remove(coordinate)  # only set acceptable (non-human) destinations
            self.model.saveLoad(rest_of_reserve, 'rest_of_reserve_dict', 'save')
            """
            # The above process is commented out because it was pickled; I should move it to its own function
            # when I have time
            rest_of_reserve = self.model.saveLoad(rest_of_reserve, 'rest_of_reserve_dict', 'load')
            rest_of_reserve_choice = random.choice(rest_of_reserve)
            for i in range(random.randint(5, 10)):  # when returning to the rest of the reserve after Yangaoping
                current_position = self.move_to_point(rest_of_reserve_choice)
                if current_position in masterdict['Elevation_Out_of_Bound'] or  \
                    current_position in masterdict['Outside_FNNR']:
                    for i in range(random.randint(2, 5)):  # the monkeys move multiple pixels each step, not just one
                        current_position = self.move_to_point(rest_of_reserve_choice)

        else:
            # When it is not about to be breeding season, during it, or just past it, move according to vegetation
            for i in range(random.randint(5, 10)):
                if self.current_position is None:
                    try:
                        self.current_position = moved_list[-2]
                    except:
                        self.current_position = self.saved_position
                neig = self.model.grid.get_neighborhood(self.current_position, True, False)
                current_position = self.neighbor_choice(neig, masterdict)
                from humans import human_avoidance_list
                if current_position not in human_avoidance_list:
                    self.move_to(current_position)
                    self.current_position = current_position

        moved_list.append(current_position)  # moved_list records positions for the heatmap

    def move_to_point(self, new_position):
        if self.current_position is None:
            self.current_position = moved_list[-2]
        current_position = list(self.current_position)  # current position
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
            for nposlist in neighbordict.values():  # for all grid values, find neighbors of this particular grid,
                for neighbor_position in nposlist:
                    if neighbor == neighbor_position:
                        vegetation = list(neighbordict.keys())[list(neighbordict.values()).index(nposlist)]
                        neighbor_veg.setdefault(neighbor, []).append(vegetation)
        for list_of_values in neighbor_veg.values():
            if len(list_of_values) > 1:
                for value in list_of_values:
                    if value != 'Elevation_Out_of_Bound' and value != 'Outside_FNNR' and value != 'PES'  \
                        and value != 'Forest' and value != 'Farm' and value != 'Household':
                        list_of_values.remove(value)
                    elif value == 'Outside_FNNR':
                        list_of_values = ['Outside_FNNR']
                    elif value == 'Elevation_Out_of_Bound':
                        list_of_values = ['Elevation_Out_of_Bound']
                    elif value == 'Household':
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
        # neighborlist = list of 8-cell neighbors to the current position
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
                weight = 0
            elif vegetation == 'PES':
                weight = 0
            elif vegetation == 'Forest':
                weight = 0
            choicelist.append(weight)


        if choicelist != [] and choicelist != [0, 0, 0, 0, 0, 0, 0, 0]:
            # this takes care of edges
            while len(choicelist) < 8:
                choicelist.append(0)
            # random choice plays a role, but each neighbor choice is affected by weights
            # the next few dozen lines determine which weighted % category the random choice falls into
            chance = random.uniform(0, 1)

            oldsum = 0
            newsum = choicelist[1] / sum(choicelist)  # defines the relative weight of the north neighbor
            if oldsum < chance < newsum:
                direction = neighborlist[1]  # north neighbor is selected
            oldsum = newsum
            newsum += choicelist[6] / sum(choicelist)  # defines the relative weight of the south neighbor
            if oldsum < chance < newsum:
                direction = neighborlist[6]  # south neighbor is selected
            oldsum = newsum
            newsum += choicelist[3] / sum(choicelist)  # defines the relative weight of the west neighbor
            if oldsum < chance < newsum:
                direction = neighborlist[3]  # west neighbor is selected
            oldsum = newsum
            newsum += choicelist[4] / sum(choicelist)  # defines the relative weight of the east neighbor
            if oldsum < chance < newsum:
                direction = neighborlist[4]  # east neighbor is selected
            oldsum = newsum
            newsum += choicelist[0] / sum(choicelist)  # defines the relative weight of the northwest neighbor
            if oldsum < chance < newsum:
                direction = neighborlist[0]  # northwest neighbor is selected
            oldsum = newsum
            newsum += choicelist[2] / sum(choicelist)  # defines the relative weight of the northeast neighbor
            if oldsum < chance < newsum:
                direction = neighborlist[2]  # northeast neighbor is selected
            oldsum = newsum
            newsum += choicelist[5] / sum(choicelist)  # defines the relative weight of the southwest neighbor
            if oldsum < chance < newsum:
                direction = neighborlist[5]  # southwest neighbor is selected
            oldsum = newsum
            newsum += choicelist[7] / sum(choicelist)  # defines the relative weight of the southeast neighbor
            if newsum != 1 and newsum > 0.999:
                newsum = 1
            if oldsum < chance < newsum:
                direction = neighborlist[7]  # southeast neighbor is selected
            assert int(newsum) == 1
            return direction


    def move_to(self, current_position):
        if current_position != None:
            self.model.grid.move_agent(self, current_position)