# !/usr/bin/python

"""
This document runs the server and helps visualize the agents.
"""

from excel_export_summary import *
import matplotlib.pyplot as plt
import numpy as np
from model import *
from agents import demographic_structure_list

model = Movement()
time = 73 * 10
erase_summary()
for t in range(time):
    model.step()
    save_summary(t, show_monkey_population(model), show_monkey_birth_count(model), show_monkey_death_count(model),
                 demographic_structure_list)
    print('Loading, Progress ', t, '/', time)


monkey_population = model.datacollector.get_model_vars_dataframe()  # see model.py
monkey_birth = model.datacollector2.get_model_vars_dataframe()
monkey_death = model.datacollector3.get_model_vars_dataframe()
demographic_structure = model.datacollector4.get_model_vars_dataframe()

age_category_list = ('0-1', '1-3', '3-7', '7-10', '10-25', '25+')
index = np.arange(len(age_category_list))
print(demographic_structure_list)
width = 0.5
plt.bar(index, demographic_structure_list, width, align = 'center')
plt.xticks(index, age_category_list)
plt.title('Age Structure in the FNNR After ' + str(time) + ' Steps')
plt.xlabel('Age')
plt.ylabel('Number of Monkeys')

monkey_population.plot()
plt.title('GGM Population in the FNNR')
plt.xlabel('5-Day Intervals (Steps)')
plt.ylabel('Number of Monkeys')

monkey_birth.plot()
plt.title('GGM Births in the FNNR')
plt.xlabel('5-Day Intervals (Steps)')
plt.ylabel('Number of Births')

monkey_death.plot()
plt.title('GGM Deaths in the FNNR')
plt.xlabel('5-Day Intervals (Steps)')
plt.ylabel('Number of Deaths')

plt.show()
