# !/usr/bin/python

"""
This document imports human data from the excel file.
"""

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

        if self.age > 70:
            if random.randint()

    def death(self):
        self.model.schedule.remove(self)
        self.model.number_of_monkeys -= 1
        self.model.monkey_death_count += 1
        if self.unique_id in female_list:
            female_list.remove(self.unique_id)

class Fuelwood(Agent):

    def __init__(self, unique_id, model, pos = None):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass
