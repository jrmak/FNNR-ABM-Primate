# !/usr/bin/python

"""
This document imports human data from the excel file.
"""

from mesa.agent import Agent
import random
originalpos = []

def _readCSV(self, text):
    # reads in a text file that determines the environmental grid setup
    f = open(text, 'r')
    body = f.readlines()
    for line in body:
        cells.append(line.split(" "))
    return cells


class Human(Agent):
    # the pixel that represents each group of monkeys with the same family id.
    # it moves on the visualization grid, unlike individual monkey agents.
    # it is currently not important in the demographic model, just the visualization model.
    def __init__(self, unique_id, model, pos, hh_id, age, resource_check):
        super().__init__(unique_id, model)
        self.pos = pos
        self.hh_id = hh_id
        self.age = age
        self.resource_check = resource_check

    def step(self):
        self.age += 1
        for x in list(self.pos):
            originalpos.append(x)
        newpos = list(self.pos)  # current
        pos = [57, 57]  # replace later
        if self.resource_check == 0:
            self.move_to_point(newpos, pos)
        else:
            self.move_to_point(newpos, (originalpos[0], originalpos[1]))
            if self.pos[0] == originalpos[0] and self.pos[1] == originalpos[1]:
                self.resource_check == 0

        if self.age > 70:
            pass
            # if random.uniform(0, 1) > 0.95:
            #     self.death()

    def death(self):
        self.model.schedule.remove(self)

    def move_to(self, pos):
        if pos != None:
            self.model.grid.move_agent(self, pos)

    def move_to_point(self, newpos, pos):
        if newpos[0] < pos[0]:
            newpos[0] = newpos[0] + 1
        elif newpos[0] == pos[0]:
            pass
        else:
            newpos[0] = newpos[0] - 1
        if newpos[1] < pos[1]:
            newpos[1] = newpos[1] + 1
        elif newpos[1] == pos[1]:
            pass
        else:
            newpos[1] = newpos[1] - 1
        newpos = tuple(newpos)
        self.move_to(newpos)
        if newpos[0] == pos[0] and newpos[1] == pos[1]:
            self.resource_check = 1

class Bamboo(Agent):

    def __init__(self, unique_id, model, pos = None):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass

class Herbs(Agent):

    def __init__(self, unique_id, model, pos = None):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass

class Fungi(Agent):

    def __init__(self, unique_id, model, pos = None):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass

class Fodder(Agent):

    def __init__(self, unique_id, model, pos = None):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass

class Fish(Agent):

    def __init__(self, unique_id, model, pos = None):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass

class Fuelwood(Agent):

    def __init__(self, unique_id, model, pos = None):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass
