"""
text = 'agg_veg60.txt'

out_counter = 0
in_counter = 0
f = open(text, 'r')
body = f.readlines()
abody = body[6:]  # ASCII file with a header
f.close()
with_list = []
for line in abody:
    for item in line.split(" "):
        if str(item) == '-9999':
            out_counter += 1
        else:
            in_counter += 1
print(out_counter, in_counter)
# 3603 coordinates outside FNNR boundaries, 4897 coordinates inside FNNR in 85 x 100 pixel grid
"""

"""
with_humans vs maxent
Kappa Statistic for 1 Count Frequency:
0.853
Kappa Statistic for 5 Count Frequency:
0.828
Kappa Statistic for 10 Count Frequency:
0.81
Kappa Statistic for 15 Count Frequency:
0.818
Kappa Statistic for 20 Count Frequency:
0.969
Kappa Statistic for 50 Count Frequency:
1.0

without vs maxent
Kappa Statistic for 1 Count Frequency:
0.856
Kappa Statistic for 5 Count Frequency:
0.861
Kappa Statistic for 10 Count Frequency:
0.845
Kappa Statistic for 15 Count Frequency:
0.832
Kappa Statistic for 20 Count Frequency:
0.976
Kappa Statistic for 50 Count Frequency:
1.0
"""

text = 'with_maxent.csv'
text = 'without_maxent.csv'
# text = 'with_without_trimmed35.csv'
# text2 = 'with_without_trimmed35_2.csv'

f = open(text, 'r')
body = f.readlines()
abody = body[2:]  # ASCII file with a header
f.close()
with_list = []
without_list = []
for line in abody: # format ('57,42,62,73')
    with_list.append(line[:5].strip("\\n"))  # first coordinates of line (first 5 characters, e.g. '57,42')
    without_list.append(str(line[-6:-1]))  # second coordinates of line (last 5 characters, e.g. '62,73')
"""
f2 = open(text2, 'r')
body2 = f2.readlines()
abody2 = body2[2:]  # ASCII file with a header
f2.close()
with_list2 = []
without_list2 = []
for line in abody2:
    with_list2.append(line[:5].strip("\\n"))
    without_list2.append(str(line[-6:-1]))
unique_with_list2 = list(set(with_list2))
unique_without_list2 = list(set(without_list2))
"""
full_grid = []

for x in range(85):
    for y in range(66,101):
        full_grid.append(str(x)+ ',' + str(y))

def kappa(with_and_without_count, with_count, without_count, neither_count, frequency_count, possible_grid_count):
    """Calculates Cohen's Kappa Coefficient"""
    p0 = (with_and_without_count + neither_count) / (possible_grid_count)  # 1425 data points in the FNNR, 2975 in 35x85
    pA = with_count / (possible_grid_count)
    pB = without_count / (possible_grid_count)
    pE_presence = pA * pB
    pE_nopresence = (1 - pA) * (1 - pB)
    pE = pE_presence + pE_nopresence
    print('Kappa Statistic for', frequency_count, 'Count Frequency:')
    print(round((p0 - pE)/(1 - pE), 3))  # rounds to 3 decimal places

def calculate_count_x(with_list, without_list, x):
    with_count = 0
    without_count = 0
    with_and_without_count = 0
    with_only_count = 0
    without_only_count = 0
    neither_count = 0
    for coordinate in full_grid:
        if with_list.count(coordinate) >= x:
            with_count += 1
            if without_list.count(coordinate) >= x:
                with_and_without_count += 1
            else:
                with_only_count += 1

        if without_list.count(coordinate) >= x:
            without_count += 1
            if with_list.count(coordinate) < x:
                without_only_count += 1
        else:
            neither_count += 1
    # print(with_and_without_count, with_count, without_count, neither_count)
    return(with_and_without_count, with_count, without_count, neither_count, x, 2975)

kappa(*calculate_count_x(with_list, without_list, 1))
kappa(*calculate_count_x(with_list, without_list, 5))
kappa(*calculate_count_x(with_list, without_list, 10))
kappa(*calculate_count_x(with_list, without_list, 15))
kappa(*calculate_count_x(with_list, without_list, 20))
kappa(*calculate_count_x(with_list, without_list, 50))

"""
kappa(*calculate_count_x(with_list, without_list, 1))
kappa(*calculate_count_x(with_list, with_list2, 1))
kappa(*calculate_count_x(without_list, without_list2, 1))
print()
kappa(*calculate_count_x(with_list, without_list, 5))
kappa(*calculate_count_x(with_list, with_list2, 5))
kappa(*calculate_count_x(without_list, without_list2, 5))
print()
kappa(*calculate_count_x(with_list, without_list, 10))
kappa(*calculate_count_x(with_list, with_list2, 10))
kappa(*calculate_count_x(without_list, without_list2, 10))
print()
kappa(*calculate_count_x(with_list, without_list, 15))
kappa(*calculate_count_x(with_list, with_list2, 15))
kappa(*calculate_count_x(without_list, without_list2, 15))
print()
kappa(*calculate_count_x(with_list, without_list, 20))
kappa(*calculate_count_x(with_list, with_list2, 20))
kappa(*calculate_count_x(without_list, without_list2, 20))
print()
kappa(*calculate_count_x(with_list, without_list, 50))
kappa(*calculate_count_x(with_list, with_list2, 50))
kappa(*calculate_count_x(without_list, without_list2, 50))
print()
kappa(*calculate_count_x(with_list, without_list, 100))
kappa(*calculate_count_x(with_list, with_list2, 100))
kappa(*calculate_count_x(without_list, without_list2, 100))
"""
"""
text = 'with_without_trimmed35.csv'
text2 = 'with_without_trimmed35_2.csv'

Kappa Statistic for 1 Count Frequency:
0.9
Kappa Statistic for 1 Count Frequency:
0.91
Kappa Statistic for 1 Count Frequency:
0.931

Kappa Statistic for 5 Count Frequency:
0.891
Kappa Statistic for 5 Count Frequency:
0.924
Kappa Statistic for 5 Count Frequency:
0.936

Kappa Statistic for 10 Count Frequency:
0.878
Kappa Statistic for 10 Count Frequency:
0.94
Kappa Statistic for 10 Count Frequency:
0.943

Kappa Statistic for 15 Count Frequency:
0.884
Kappa Statistic for 15 Count Frequency:
0.934
Kappa Statistic for 15 Count Frequency:
0.933

Kappa Statistic for 20 Count Frequency:
0.897
Kappa Statistic for 20 Count Frequency:
0.945
Kappa Statistic for 20 Count Frequency:
0.918

Kappa Statistic for 50 Count Frequency:
0.9
Kappa Statistic for 50 Count Frequency:
0.868
Kappa Statistic for 50 Count Frequency:
0.893

Kappa Statistic for 100 Count Frequency:
0.692
Kappa Statistic for 100 Count Frequency:
0.583
Kappa Statistic for 100 Count Frequency:
0.75
"""