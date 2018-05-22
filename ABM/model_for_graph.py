from model import *

def show_monkey_population(model):
    """Returns the total population of modeled monkeys in the FNNR"""
    return model.number_of_monkeys

def show_monkey_birth_count(model):
    """Returns the total number of births of modeled monkeys in the FNNR"""
    return model.monkey_birth_count

def show_monkey_death_count(model):
    """Returns the total number of deaths of modeled monkeys in the FNNR"""
    return model.monkey_death_count

def show_demographic_structure_list(model):
    """Returns a list that shows population structure of modeled monkeys in the FNNR"""
    return demographic_structure_list