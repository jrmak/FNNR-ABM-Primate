import random

from mesa.agent import Agent
from maxent import Maxent

class Monkey(Agent):

    strategy = None
    age = 0

    def __init__(self, unique_id, model, pos=None):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        self.age += 1

        self.switch()
        """
        # new Monkey
        neig = self.model.grid.get_neighborhood(self.pos, True, False)
        pos = random.choice(neig)
        last = self.model.number_of_monkeys
        print(last)
        new_monkey = Monkey(last + 1, self.model)
        new_monkey.strategy = self.strategy
        self.model.grid.place_agent(new_monkey, pos)
        self.model.schedule.add(new_monkey)
        self.model.number_of_monkeys += 1
        
        else:
        """
        from model import masterdict  # can't do this at the beginning
        neig = self.model.grid.get_neighborhood(self.pos, True, False)
        pos = self.neighbor_choice(neig, masterdict)
        # pos = random.choice(neig)
        self.move_to(pos)

        # Death
 #       if self.age > 10:
 #           self.die()

    def neighbor_choice(self, neighborlist, neighbordict):
        # agent chooses a neighbor to move to based on weights
        choicelist = []
        # picks a weighted neighbor to move to
        # print(neighborlist)
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
        # print(choicelist)
        if choicelist != [] and choicelist != [0, 0, 0, 0, 0, 0, 0, 0]:
            try:
                # print(choicelist)
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

    def switch(self):
        # currently not working, ignore this function
        from maxent import masterdict  # can't do this at the beginning
        neig = self.model.grid.get_neighborhood(self.pos, True, False)
        # neig lists 8 coordinates
        # pos = random.choice(neig)
        pos = self.neighbor_choice(neig, masterdict)
        # determines direction agent moves in
        if pos != None:
            if self.model.grid.is_cell_empty(pos):
                self.move_to(pos)
        else:
            pass  # don't move


    def move_to(self, pos):
        if pos != None:
            self.model.grid.move_agent(self, pos)

    def die(self):
        # not implemented yet
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)
        self.model.number_of_monkeys -= 1

# all parameters below are currently unused except for seed and weight

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