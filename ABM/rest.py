import random
thedict = {44: 888, 80: 550, 45: 900, 81: 409, 43: 807, 79: 687, 78: 769, 42: 696, 15: 34, 14: 35, 13: 33, 26: 232, 71: 1487, 27: 264, 70: 1568, 72: 1441, 73: 1412, 34: 357, 56: 1955, 55: 1972, 54: 1986, 53: 1991, 35: 378, 36: 424, 46: 1049, 7: 39, 47: 1294, 8: 30, 9: 21, 63: 1767, 76: 863, 75: 1074, 64: 1688, 62: 1906, 61: 1863, 37: 453, 38: 496, 33: 361, 39: 721, 32: 409, 40: 549, 31: 388, 30: 359, 41: 618, 74: 1272, 60: 1832, 28: 245, 59: 1856, 25: 168, 24: 115, 17: 30, 18: 34, 57: 2142, 19: 43, 20: 43, 58: 1987, 16: 30, 48: 1300, 49: 1462, 50: 1577, 10: 23, 12: 20, 11: 18, 77: 781, 52: 1830, 69: 1640, 29: 274, 23: 86, 6: 30, 51: 1805, 82: 355, 83: 293, 84: 130, 5: 23, 65: 1717, 66: 1743, 67: 1642, 68: 1667, 21: 45, 22: 57, 4: 18, 3: 2, 85: 122, 86: 122, 87: 150, 88: 153, 89: 122, 90: 67, 91: 47, 92: 27, 93: 22, 94: 10, 95: 4}
newdict = {}

# for key, value in sorted(thedict.items()):
#     newdict.setdefault(key, []).append(value)

# print(newdict)

newdict = {3: [2], 4: [18], 5: [23], 6: [30], 7: [39], 8: [30], 9: [21], 10: [23], 11: [18], 12: [20], 13: [33], 14: [35], 15: [34], 16: [30], 17: [30], 18: [34], 19: [43], 20: [43], 21: [45], 22: [57], 23: [86], 24: [115], 25: [168], 26: [232], 27: [264], 28: [245], 29: [274], 30: [359], 31: [388], 32: [409], 33: [361], 34: [357], 35: [378], 36: [424], 37: [453], 38: [496], 39: [721], 40: [549], 41: [618], 42: [696], 43: [807], 44: [888], 45: [900], 46: [1049], 47: [1294], 48: [1300], 49: [1462], 50: [1577], 51: [1805], 52: [1830], 53: [1991], 54: [1986], 55: [1972], 56: [1955], 57: [2142], 58: [1987], 59: [1856], 60: [1832], 61: [1863], 62: [1906], 63: [1767], 64: [1688], 65: [1717], 66: [1743], 67: [1642], 68: [1667], 69: [1640], 70: [1568], 71: [1487], 72: [1441], 73: [1412], 74: [1272], 75: [1074], 76: [863], 77: [781], 78: [769], 79: [687], 80: [550], 81: [409], 82: [355], 83: [293], 84: [130], 85: [122], 86: [122], 87: [150], 88: [153], 89: [122], 90: [67], 91: [47], 92: [27], 93: [22], 94: [10], 95: [4]}