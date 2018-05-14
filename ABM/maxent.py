import random

from mesa.agent import Agent

masterdict = {}

class Maxent(Agent):

    # Environment becomes less suitable during winter: less land, more firewood usage

    # fully_grown = False

    def __init__(self, unique_id, model, pos=None):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass
        """
        from model import masterdict
        land_name = type(self).__name__.lower()
        attr_name = "number_of_{}".format(land_name)
        last = getattr(self.model, attr_name)
        new_land = type(self)(last + 1, self.model)
        masterdict[new_land.__class__.__name__].append(pos)
        """

        """
        neig = self.model.grid.get_neighborhood(self.pos, True, False)
        is_empty = self.model.grid.is_cell_empty

        if any(map(is_empty, neig)):
            empty = list(filter(is_empty, neig))
            pos = random.choice(empty)

            land_name = type(self).__name__.lower()
            attr_name = "number_of_{}".format(land_name)
            last = getattr(self.model, attr_name)
            new_land = type(self)(last + 1, self.model)
            setattr(self.model, attr_name, last + 1)
            self.model.grid.place_agent(new_land, pos)
            if new_land.__class__.__name__ not in masterdict:
                masterdict[new_land.__class__.__name__] = [pos]
            else:
                masterdict[new_land.__class__.__name__].append(pos)
            self.model.schedule.add(new_land)
        """