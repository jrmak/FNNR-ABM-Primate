# !/usr/bin/python

"""
This document runs the server and helps visualize the agents.
"""

from excel_export_summary import *
import matplotlib.pyplot as plt
import numpy as np
from model import *
from agents import demographic_structure_list, female_list, male_maingroup_list, reproductive_female_list
from model_for_graph import *


model = Movement()  # run the model
time = 73 * 1  # 73 time-steps of 5 days each for 10 years, 730 steps total
erase_summary()  # clears the Excel file to overwrite
for t in range(time):  # for each time-step in the time we just defined,
    model.step()  # see model.step() in model.py; monkey agents age, family-pixel agents move
    save_summary(t, show_monkey_population(model), show_monkey_birth_count(model), show_monkey_death_count(model),
                 demographic_structure_list, female_list, male_maingroup_list, reproductive_female_list)
    # save_summary writes the Excel file; see excel_export_summary
    print('Loading, Progress ', t, '/', time)


monkey_population = model.datacollector.get_model_vars_dataframe()  # see model.py
monkey_birth = model.datacollector2.get_model_vars_dataframe()
monkey_death = model.datacollector3.get_model_vars_dataframe()
demographic_structure = model.datacollector4.get_model_vars_dataframe()

plt.subplot(311)
age_category_list = ('0-1', '1-3', '3-7', '7-10', '10-25', '25+')
index = np.arange(len(age_category_list))
width = 0.5
plt.bar(index, demographic_structure_list, width, align = 'center')
plt.xticks(index, age_category_list)
plt.title('Age Structure in the FNNR After ' + str(time) + ' Steps')
plt.xlabel('Age')
plt.ylabel('# of Monkeys')
print('Age Structure Count || 0-1: %i | 1-3: %i | 3-7: %i | 7-10: %i | 10-25: %i | 25+: %i' %
      (demographic_structure_list[0], demographic_structure_list[1],
       demographic_structure_list[2], demographic_structure_list[3],
       demographic_structure_list[4], demographic_structure_list[5]))

plt.subplot(313)
gender_category_list = ('Rep. Females', 'Total Females', 'Main Group Males')
index2 = np.arange(len(gender_category_list))
# print(gender_category_list)
width = 0.5
plt.bar(index2, [len(reproductive_female_list), len(female_list), len(male_maingroup_list)], width, align = 'center')
plt.xticks(index2, gender_category_list)
plt.title('Gender Structure in the FNNR After ' + str(time) + ' Steps')
plt.ylabel('# of Monkeys')
print('Gender Structure Count || Reproductive Females: %i | Total Females: %i | Main-group Males: %i' %
      (len(reproductive_female_list), len(female_list), len(male_maingroup_list)))

from heatmap import *  # see heatmap.py


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

plt.show()  # shows all plots at once