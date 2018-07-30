# !/usr/bin/python

"""
This document runs the server and helps visualize the agents.
"""

# 7-27-18

from excel_export_summary import *
from excel_export_density_plot import *
import matplotlib.pyplot as plt
import numpy as np
from model import *
from families import demographic_structure_list, female_list, male_maingroup_list, reproductive_female_list, moved_list

monkey_population_list = []
monkey_birth_count = []
monkey_death_count = []
counter = 30

model = Movement()  # run the model
time = 73 * 10  # 73 time-steps of 5 days each for 10 years, 730 steps total
# erase_summary()  # clears the Excel file to overwrite
# erase_density_plot()
for t in range(time):  # for each time-step in the time we just defined,
    monkey_population_list.append(model.number_of_monkeys)
    monkey_birth_count.append(model.monkey_birth_count)
    monkey_death_count.append(model.monkey_death_count)
    model.step()  # see model.step() in model.py; monkey agents age, family-pixel agents move
    print('Loading, Progress ', t, '/', time)
    if t == 1:
        save_summary(t, model.number_of_monkeys, model.monkey_birth_count, model.monkey_death_count,
                 demographic_structure_list, female_list, male_maingroup_list, reproductive_female_list)
save_summary(t, model.number_of_monkeys, model.monkey_birth_count, model.monkey_death_count,
                 demographic_structure_list, female_list, male_maingroup_list, reproductive_female_list)
# save_summary writes the Excel file; see excel_export_summary
save_density_plot(moved_list, counter)

plt.subplot(211)
age_category_list = ('0-1', '1-3', '3-7', '7-10', '10-25', '25+')
index = np.arange(len(age_category_list))
width = 0.5  # width of each bar
plt.bar(index, demographic_structure_list, width, align = 'center')
plt.xticks(index, age_category_list)
plt.title('Age Structure in the FNNR After ' + str(time) + ' Steps')
plt.xlabel('Age')
plt.ylabel('# of Monkeys')
print('Age Structure Count || 0-1: %i | 1-3: %i | 3-7: %i | 7-10: %i | 10-25: %i | 25+: %i' %
      (demographic_structure_list[0], demographic_structure_list[1],
       demographic_structure_list[2], demographic_structure_list[3],
       demographic_structure_list[4], demographic_structure_list[5]))

# Percentages of each age category
print(
str("Age 0-1: " + str(round(demographic_structure_list[0] / sum(demographic_structure_list) * 100, 2)) + "% | "),
str("Age 1-3: " + str(round(demographic_structure_list[1] / sum(demographic_structure_list) * 100, 2)) + "% | "),
str("Age 3-7: " + str(round(demographic_structure_list[2] / sum(demographic_structure_list) * 100, 2)) + "% | "),
str("Age 7-10: " + str(round(demographic_structure_list[3] / sum(demographic_structure_list) * 100, 2)) + "% | "),
str("Age 10-25: " + str(round(demographic_structure_list[4] / sum(demographic_structure_list) * 100, 2)) + "% | "),
str("Age 25+: " + str(round(demographic_structure_list[5] / sum(demographic_structure_list) * 100, 2)) + "%"))

plt.subplot(212)
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
plt.tight_layout()  # needed to make the graph look neat
plt.figure()  # each instance of plt.figure() sets a graph in a new window

# from heatmap import *  # see heatmap.py; discontinued. I now generate an excel file from which I create the heatmap.
# See documentation for how (summary: I create an xy scatterplot and set the points to 99% transparent).
# plt.figure()

plt.subplot(2, 2, 1)
plt.plot(np.array(range(time)), np.array(monkey_population_list))
plt.title('GGM Population in the FNNR')
plt.xlabel('5-Day Intervals (Steps)')
plt.ylabel('Number of Monkeys')

plt.subplot(2, 2, 2)
plt.plot(np.array(range(time)), np.array(monkey_birth_count))
plt.title('GGM Births in the FNNR')
plt.xlabel('5-Day Intervals (Steps)')
plt.ylabel('Number of Births')

plt.subplot(2, 2, 3)
plt.plot(np.array(range(time)), np.array(monkey_death_count))
plt.title('GGM Deaths in the FNNR')
plt.xlabel('5-Day Intervals (Steps)')
plt.ylabel('Number of Deaths')
plt.tight_layout()

# plt.show()  # shows all plots at once