import os

directory = r'C:\Users\Judy\Desktop\Fertility Runs\3.5 GTGP New'

dict_population = {}
dict_migrants = {}
for i in os.listdir(directory):
    if 'humans' in i and 'csv' in i:
        with open(directory + r'\\' + i, 'r') as f:
            for row in f.readlines():
                step = row.split(',')[0]
                population = row.split(',')[3]
                migrants = row.split(',')[4]
                dict_population.setdefault(step, []).append(float(population))
                dict_migrants.setdefault(step, []).append(float(migrants))

summary_dict1 = {}
summary_dict2 = {}
for key, value in dict_population.items():
    summary_dict1[key] = [sum(value)/len(value)]
for key, value in dict_migrants.items():
    summary_dict2[key] = sum(value)/len(value)
for key, value in summary_dict1.items():
    summary_dict1[key].append(summary_dict2[key])

with open(directory + r'\\' + 'Household Composite.csv', 'w+') as f2:
    for key, value in summary_dict1.items():
        f2.write(key + ',' + str(value[0]) + ',' + str(value[1]))
        f2.write('\n')