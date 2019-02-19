#!/usr/bin/python
from collections import Counter

"""
Finds the symmetric difference of the two scenarios' heatmaps ('With Humans' vs. 'Without Humans').
"""
directory_path = 'C:\\Users\\Judy\Desktop\\FNNR-ABM-Primate-master\\Results'

text1 = directory_path + '\\270-0 Difference\\abm_export_density_plot_with_humans_1-270_10.csv'
text2 = directory_path + '\\270-0 Difference\\abm_export_density_plot_with_humans_1-0_10.csv'

def readCSV(file):
    list_to_read = []
    f = open(file, 'r')
    body = f.readlines()
    f.close()
    for line in body: # format ('57,42,62,73')
        list_to_read.append(line.strip("\n").replace(" ",""))  # first coordinates of line (first 5 characters, e.g. '57,42')
    return list_to_read

list1 = readCSV(text1)
list2 = readCSV(text2)

dict1 = {}
dict2 = {}

def dict_values_append(sample_dict, sample_list):
    for coordinate in sample_list:
        sample_dict.setdefault(coordinate, []).append(1)
    return sample_dict

dict1 = dict_values_append(dict1, list1)
dict2 = dict_values_append(dict2, list2)

def sum_dict_values(sample_dict):
    for key in sample_dict:
        sample_dict[key] = sum(sample_dict[key])
    return sample_dict

newdict1 = sum_dict_values(dict1)
newdict2 = sum_dict_values(dict2)

def difference_dict(dict1, dict2):
    output_dict = {}
    for key in dict1.keys():
        if key in dict2.keys():
            output_dict[key] = abs(dict1[key] - dict2[key])
    return output_dict

def difference_dict_percentage(dict1, dict2):
    output_dict = {}
    for key in dict1.keys():
        if key in dict2.keys():
            output_dict[key] = int(round(abs(dict1[key] - dict2[key])/max([dict1[key], dict2[key]]) * 100, 0))
    return output_dict

difference = difference_dict_percentage(newdict1, newdict2)
print(difference)

try:
    diff = open('difference270-0_10_percentage.csv', 'w+')  # a+ will create the file if it doesn't exist already
except IOError:
    print('Please close Excel and retry.')  # will not work if the .csv is already open
for k, v in difference.items():
    for i in range(v):
        diff.writelines(k)
        diff.writelines('\n')
diff.flush()  # flush memory
diff.close()