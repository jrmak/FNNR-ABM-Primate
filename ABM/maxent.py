import random

from mesa.agent import Agent

masterdict = {}

class Maxent(Agent):

    # Environment becomes less suitable during winter: less land, more firewood usage

    def __init__(self, unique_id, model, pos=None):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass
        # will add seasonal variations to environment later, if vegetation data is imported