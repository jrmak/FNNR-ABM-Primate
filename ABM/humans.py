# !/usr/bin/python

"""
This document imports human data from the excel file.
"""

from mesa.agent import Agent
import random


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
    def __init__(self, unique_id, model, pos, hh_id, age):
        super().__init__(unique_id, model)
        self.pos = pos
        self.hh_id = hh_id
        self.age = age

    def step(self):
        self.age += 1

        neig = self.model.grid.get_neighborhood(self.pos, True, False)  # gets neighboring pixels again
        pos = random.choice(neig)
        self.move_to(pos)

        if self.age > 70:
            pass
            # if random.uniform(0, 1) > 0.95:
            #     self.death()

    def death(self):
        self.model.schedule.remove(self)

    def move_to(self, pos):
        if pos != None:
            self.model.grid.move_agent(self, pos)

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
