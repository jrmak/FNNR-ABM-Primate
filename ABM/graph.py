# !/usr/bin/python
# 2/11/2019

"""
This document runs the server and helps visualize the agents.
"""
from excel_export_summary_monkeys import save_summary
from excel_export_summary_humans import save_summary_humans, save_summary_human_demographics
from excel_export_summary_households import save_summary_households
from excel_export_density_plot import save_density_plot
from model import *
from families import demographic_structure_list, female_list, male_maingroup_list, reproductive_female_list, moved_list
from humans import hh_size_list, human_birth_list, human_death_list, human_marriage_list,\
    single_male_list, married_male_list, \
    num_labor_list, total_migration_list, human_demographic_structure_list
from land import non_gtgp_part_list, gtgp_part_list, non_gtgp_area_list, gtgp_area_list, household_income_list
from fnnr_config_file import human_setting, year_setting, random_walk_graph_setting, plot_setting
import os
import matplotlib.pyplot as plt
import numpy as np

monkey_population_list = []
monkey_birth_count = []
monkey_death_count = []

model = Movement()  # run the model
model_time = 73 * year_setting # 73 time-steps of 5 days each for 10 years, 730 steps total
run = 1  # do not change this; it will automatically search for the first number-as-string not taken
while os.path.isfile(os.getcwd() + '\\' + 'abm_export_summary_humans' + str(run) + '.csv'):
    # if folder exists in current directory, loop up until it finds a unique number
    run += 1
for t in range(model_time):  # for each time-step in the time we just defined,
    monkey_population_list.append(model.number_of_monkeys)
    monkey_birth_count.append(model.monkey_birth_count)
    monkey_death_count.append(model.monkey_death_count)
    model.step()  # see model.step() in model.py; monkey agents age, family-pixel agents move
    print('Loading, Progress', t, '/', model_time)
    if t % 6 == 0 and t != 0:  # save beginning structure, then every 100 days thereafter
        save_summary(str(run), t, model.number_of_monkeys, model.monkey_birth_count, model.monkey_death_count,
                 demographic_structure_list, female_list, male_maingroup_list, reproductive_female_list)
        save_summary_humans(str(run), t, model.number_of_humans, len(human_birth_list), len(human_death_list),
                            sum(human_marriage_list), sum(num_labor_list),
                            len(single_male_list), len(married_male_list), sum(total_migration_list)
                            )  # 94 households
        save_summary_human_demographics(str(run), t, human_demographic_structure_list[0],
                                        human_demographic_structure_list[1],
                                        human_demographic_structure_list[2], human_demographic_structure_list[3],
                                        human_demographic_structure_list[4], human_demographic_structure_list[5],
                                        human_demographic_structure_list[6], human_demographic_structure_list[7],
                                        human_demographic_structure_list[8], human_demographic_structure_list[9],
                                        human_demographic_structure_list[10], human_demographic_structure_list[11],
                                        human_demographic_structure_list[12], human_demographic_structure_list[13],
                                        human_demographic_structure_list[14], human_demographic_structure_list[15],
                                        human_demographic_structure_list[16], human_demographic_structure_list[17],
                                        human_demographic_structure_list[18], human_demographic_structure_list[19])
        save_summary_households(str(run), t, sum(non_gtgp_part_list), sum(gtgp_part_list),
                                sum(non_gtgp_part_list) / 94, sum(gtgp_part_list) / 94,
                                sum(non_gtgp_area_list) / 94,
                                sum(gtgp_area_list) / 94
                                )
save_density_plot(moved_list, str(run))
print('Done!')

if random_walk_graph_setting == True:  # disabled or enabled according to fnnr_config_file.py
    # this should only be run with 1 family at a time or else the graphs will be messed up
    for i in [1, 3, 5]:
        if t == 73 * i:
            save_density_plot(moved_list, i)

plt.subplot(211)
age_category_list = ('0-1', '1-3', '3-7', '7-10', '10-25', '25+')
index = np.arange(len(age_category_list))
width = 0.5  # width of each bar
plt.bar(index, demographic_structure_list, width, align = 'center')
plt.xticks(index, age_category_list)
plt.title('Age Structure in the FNNR After ' + str(model_time) + ' Steps')
plt.xlabel('Age')
plt.ylabel('# of Monkeys')
print('Below is an incomplete output of monkey demographic information.')
print('More info, including human and GTGP demographics, can be found in the output .csv files in this directory.')
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
plt.title('Gender Structure in the FNNR After ' + str(model_time) + ' Steps')
plt.ylabel('# of Monkeys')
print('Gender Structure Count || Reproductive Females: %i | Total Females: %i | Main-group Males: %i' %
      (len(reproductive_female_list), len(female_list), len(male_maingroup_list)))
plt.tight_layout()  # needed to make the graph look neat
plt.figure()  # each instance of plt.figure() sets a graph in a new window

plt.subplot(2, 2, 1)
plt.plot(np.array(range(model_time)), np.array(monkey_population_list))
plt.title('GGM Population in the FNNR')
plt.xlabel('5-Day Intervals (Steps)')
plt.ylabel('Number of Monkeys')

plt.subplot(2, 2, 2)
plt.plot(np.array(range(model_time)), np.array(monkey_birth_count))
plt.title('GGM Births in the FNNR')
plt.xlabel('5-Day Intervals (Steps)')
plt.ylabel('Number of Births')

plt.subplot(2, 2, 3)
plt.plot(np.array(range(model_time)), np.array(monkey_death_count))
plt.title('GGM Deaths in the FNNR')
plt.xlabel('5-Day Intervals (Steps)')
plt.ylabel('Number of Deaths')
plt.tight_layout()

if plot_setting == True:
    plt.show()  # shows all plots at once