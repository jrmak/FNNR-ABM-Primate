# !/usr/bin/python

import os
import inspect

"""
This file calculates the kappa statistic for two heatmap outputs (csv file of movements) of the visualization submodel.
"""

def readCSV(file):
    list_to_read = []
    f = open(file, 'r')
    body = f.readlines()
    f.close()
    for line in body: # format ('57,42,62,73')
        list_to_read.append(line.strip("\n").replace(" ",""))  # first coordinates of line (first 5 characters, e.g. '57,42')
    return list_to_read

full_grid = []

for x in range(85):
    for y in range(66, 101):  # trimmed: only top 35% of FNNR where we have data for 2 villages
        full_grid.append(str(x)+ ',' + str(y))

def kappa(with_and_without_count, with_count, without_count, neither_count, frequency_count, possible_grid_count):
    """Calculates Cohen's Kappa Coefficient"""
    p0 = (with_and_without_count + neither_count) / (possible_grid_count)  # 1425 data points in the FNNR, 2975 in 35x85
    pA = with_count / (possible_grid_count)
    pB = without_count / (possible_grid_count)
    pE_presence = pA * pB
    pE_nopresence = (1 - pA) * (1 - pB)
    pE = pE_presence + pE_nopresence
    return (round((p0 - pE)/(1 - pE), 3))  # rounds to 3 decimal places
    # writeKappa(frequency_count, round((p0 - pE)/(1 - pE), 3))

def calculate_count_x(list1, list2, x):
    with_count = 0
    without_count = 0
    with_and_without_count = 0
    with_only_count = 0
    without_only_count = 0
    neither_count = 0
    for coordinate in full_grid:
        if list1.count(coordinate) >= x:
            with_count += 1
            if list2.count(coordinate) >= x:
                with_and_without_count += 1
            else:
                with_only_count += 1

        elif list2.count(coordinate) >= x:
            without_count += 1
            if list1.count(coordinate) < x:
                without_only_count += 1

        else:
            neither_count += 1

    # print(with_and_without_count, with_count, without_count, neither_count)
    return(with_and_without_count, with_count, without_count, neither_count, x, 2975)
    # 1425 data points in the FNNR, 2975 in 35x85

currentpath = str(inspect.getfile(inspect.currentframe()))[:-14]  # removes 'kappa_batch.py' at end
os.chdir(currentpath)  # uses current directory path

def writeKappa(count, kappa_output, text_input):
    """
    try:
        max_refresh = open('maxent.csv', 'w+')  # w+ will create the file if it doesn't exist already
        max_refresh.truncate()
        max_refresh.close()
    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    """
    try:
        kappa30 = open('kappa30_average_' + text_input + '.csv', 'a+')  # a+ will create the file if it doesn't exist already
        # kappa30 = open('kappa_maxent_diff.csv', 'a+')  # a+ will create the file if it doesn't exist already
        # kappa30 = open('kappa_average_w.csv', 'a+')
        # kappa30 = open('kappa_average_w.csv', 'a+')  # comparing with vs. without

    except IOError:
        print('Please close Excel and retry.')  # will not work if the .csv is already open
    kappa30.writelines(str(count))
    kappa30.writelines(',')
    kappa30.writelines(str(kappa_output))
    kappa30.writelines('\n')
    kappa30.flush()  # flush memory
    kappa30.close()


threshold_list = [50, 100, 200, 400, 600]
for i in threshold_list:
    # text1 = 'abm_export_density_plot_wo' + str(number) + '.csv'
    # text2 = 'abm_export_density_plot_wo' + str(number + 1) + '.csv'
    # text1 = 'export_density_plot_w' + str(number) + '.csv'
    # text2 = 'export_density_plot_w' + str(number + 1) + '.csv'
    # text1 = 'export_density_plot_w' + str(number) + '.csv'
    # text2 = 'export_density_plot_w' + str(number) + '.csv'
    # text2 = 'maxent.csv'
    for number in range(1, 31):
        currentpath = os.getcwd()
        list1 = readCSV(currentpath + '\\270 Trimmed\\abm_export_density_plot_with_humans_' + str(number) + '.csv')
        list2 = readCSV(currentpath + '\\0 Trimmed\\abm_export_density_plot_with_humans_' + str(number) + '.csv')
        kappa_number = kappa(*calculate_count_x(list1, list2, i))
        writeKappa(i, kappa_number, '270_with_0')
        print('Progress: ' + str(number) + ' / 30 for ' + str(i))
for i in threshold_list:
    for number in range(1, 31):
        currentpath = os.getcwd()
        list1 = readCSV(currentpath + '\\270 Trimmed\\abm_export_density_plot_with_humans_' + str(number) + '.csv')
        list2 = readCSV(currentpath + '\\540 Trimmed\\abm_export_density_plot_with_humans_' + str(number) + '.csv')
        kappa_number = kappa(*calculate_count_x(list1, list2, i))
        writeKappa(i, kappa_number, '270_with_540')
        print('Progress: ' + str(number) + ' / 30 for ' + str(i))
for i in threshold_list:
    for number in range(1, 30):
        currentpath = os.getcwd()
        list1 = readCSV(currentpath + '\\270 Trimmed\\abm_export_density_plot_with_humans_' + str(number) + '.csv')
        list2 = readCSV(currentpath + '\\270 Trimmed\\abm_export_density_plot_with_humans_' + str(number + 1) + '.csv')
        kappa_number = kappa(*calculate_count_x(list1, list2, i))
        writeKappa(i, kappa_number, '270_with_self')
        print('Progress: ' + str(number) + ' / 30 for ' + str(i))

#text1 = 'difference2.csv'
#text2 = 'maxent.csv'

"""
kappa(*calculate_count_x(list1, list2, 1))
kappa(*calculate_count_x(list1, list1, 1))
kappa(*calculate_count_x(list2, list2, 1))
print()
kappa(*calculate_count_x(list1, list2, 5))
kappa(*calculate_count_x(list1, list1, 5))
kappa(*calculate_count_x(list2, list2, 5))
print()
kappa(*calculate_count_x(list1, list2, 10))
kappa(*calculate_count_x(list1, list1, 10))
kappa(*calculate_count_x(list2, list2, 10))
print()
kappa(*calculate_count_x(list1, list2, 15))
kappa(*calculate_count_x(list1, list1, 15))
kappa(*calculate_count_x(list2, list2, 15))
print()
kappa(*calculate_count_x(list1, list2, 20))
kappa(*calculate_count_x(list1, list1, 20))
kappa(*calculate_count_x(list2, list2, 20))
print()
kappa(*calculate_count_x(list1, list2, 50))
kappa(*calculate_count_x(list1, list2, 50))
kappa(*calculate_count_x(list2, list2, 50))
print()
kappa(*calculate_count_x(list1, list2, 100))
kappa(*calculate_count_x(list1, list2, 100))
kappa(*calculate_count_x(list2, list2, 100))
"""
"""
text = 'with_without_trimmed35.csv'
text2 = 'with_without_trimmed35_2.csv'

Kappa Statistic for 1 Count Frequency:
0.813
936 1017 121 1837
Kappa Statistic for 1 Count Frequency:
0.809
1014 1091 95 1789
Kappa Statistic for 1 Count Frequency:
0.846

750 798 132 2045
Kappa Statistic for 5 Count Frequency:
0.79
717 798 89 2088
Kappa Statistic for 5 Count Frequency:
0.797
757 882 78 2015
Kappa Statistic for 5 Count Frequency:
0.778

596 642 129 2204
Kappa Statistic for 10 Count Frequency:
0.755
571 642 60 2273
Kappa Statistic for 10 Count Frequency:
0.806
627 725 61 2189
Kappa Statistic for 10 Count Frequency:
0.79

489 546 107 2322
Kappa Statistic for 15 Count Frequency:
0.733
474 546 58 2371
Kappa Statistic for 15 Count Frequency:
0.777
540 596 64 2315
Kappa Statistic for 15 Count Frequency:
0.811

419 475 84 2416
Kappa Statistic for 20 Count Frequency:
0.737
404 475 43 2457
Kappa Statistic for 20 Count Frequency:
0.774
444 503 69 2403
Kappa Statistic for 20 Count Frequency:
0.767

133 183 33 2759
Kappa Statistic for 50 Count Frequency:
0.608
144 183 46 2746
Kappa Statistic for 50 Count Frequency:
0.619
119 166 32 2777
Kappa Statistic for 50 Count Frequency:
0.594

2 7 4 2964
Kappa Statistic for 100 Count Frequency:
0.18
0 7 5 2963
Kappa Statistic for 100 Count Frequency:
-0.002
0 6 2 2967
Kappa Statistic for 100 Count Frequency:
-0.001
"""