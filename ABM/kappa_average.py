import os

directory = r'C:\Users\Judy\Desktop\270 Multiplier runs\Kappa'
os.chdir(directory)

average_list = []

for n in os.listdir(directory):
    if 'kappa' in n and n[-3:] == 'csv':
        with open(n, 'r') as f:
            lines = f.readlines()
            ilist50 = []
            ilist100 = []
            ilist200 = []
            ilist400 = []
            ilist600 = []
            for i in lines[:10]:
                split_i = i.split(",")
                ilist50.append(float(split_i[1]))
            for i in lines[10:20]:
                split_i = i.split(",")
                ilist100.append(float(split_i[1]))
            for i in lines[20:30]:
                split_i = i.split(",")
                ilist200.append(float(split_i[1]))
            for i in lines[30:40]:
                split_i = i.split(",")
                ilist400.append(float(split_i[1]))
            for i in lines[40:50]:
                split_i = i.split(",")
                ilist600.append(float(split_i[1]))
            average_list.append(['50', n.split('_')[2], n.split('_')[3], n.split('_')[4], sum(ilist50) / len(ilist50)])
            average_list.append(['100', n.split('_')[2], n.split('_')[3], n.split('_')[4], sum(ilist100) / len(ilist100)])
            average_list.append(['200', n.split('_')[2], n.split('_')[3], n.split('_')[4], sum(ilist200) / len(ilist200)])
            average_list.append(['400', n.split('_')[2], n.split('_')[3], n.split('_')[4], sum(ilist400) / len(ilist400)])
            average_list.append(['600', n.split('_')[2], n.split('_')[3], n.split('_')[4], sum(ilist600) / len(ilist600)])
        f.close()
with open('combined.csv', 'w+') as f2:
    for x in average_list:
        f2.write(x[0] + ',' + x[1] + ',' + x[2] + ',' + x[3] + ',' + str(x[4]))
        f2.write('\n')

        
            

