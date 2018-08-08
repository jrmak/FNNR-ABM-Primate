# !/usr/bin/python

"""
This document imports human data from the excel file.
"""

from mesa.agent import Agent
import random

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
                 home_position, resource_position, resource_frequency):
        super().__init__(unique_id, model)
        self.current_position = current_position
        self.hh_id = hh_id
        self.age = age
        self.resource_check = resource_check
        self.home_position = home_position
        self.resource_position = resource_position
        self.resource_frequency = resource_frequency

    def step(self):
        # self.age += 1  # currently not used; humans don't age
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

        if self.age > 70:
            pass
            # may input human aging later. for example -
            # if random.uniform(0, 1) > 0.95:
            #     self.death()

    def death(self):
        # currently not used
        # must implement birth() (not created yet) too if used
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)

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