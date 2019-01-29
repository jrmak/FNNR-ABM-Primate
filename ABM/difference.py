#!/usr/bin/python

"""
Finds the symmetric difference of the two scenarios' heatmaps ('With Humans' vs. 'Without Humans').
"""
directory_path = 'C:\\Users\\Judy\\Desktop'

text1 = directory_path + '\\10\\abm_export_density_plot_with_humans_10yr_' + '270' + '.csv'
text2 = directory_path + '\\10\\abm_export_density_plot_with_humans_10yr_' + '540' + '.csv'

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

union_difference = {x: abs(newdict1[x] - newdict2[x]) for x in newdict1 if x in newdict2}
symmetric_difference = set(newdict1.items()) ^ set(newdict2.items())

#difference = union_difference.copy()
#difference.update(symmetric_difference)
difference = set(newdict1.items()) - set(newdict2.items())
try:
    diff = open('difference270-540_10.csv', 'a+')  # a+ will create the file if it doesn't exist already
    # diff = open('kappa_average_w.csv', 'a+')
    # diff = open('kappa_average_w.csv', 'a+')  # comparing with vs. without
except IOError:
    print('Please close Excel and retry.')  # will not work if the .csv is already open
for k, v in difference:
    for i in range(v):
        diff.writelines(k)
        diff.writelines('\n')
diff.flush()  # flush memory
diff.close()
