# for line in modes_file:
#     tokens = line.split('-')
#     if tokens[1] == "CBC":

#     elif tokens[1] == "CBC":
#     elif tokens[1] == "CBC":
#     elif tokens[1] == "CBC":
#     elif tokens[1] == "CBC":
import matplotlib.pyplot as plt
import numpy as np

# I know my method here is a bit clumsy, I was up the entire night, take pity lol

modes_file = open('modesTimeData.txt')

modesDict = {'CBC':  [], 'CTR': [],
             'ECB': [], 'OFB': [], 'CFB': []}

for line in modes_file:
    tokens = line.split('-')
    modesDict[tokens[1]].append([tokens[2], int(tokens[3].strip())])


modes = ['CBC', 'CTR', 'ECB', 'OFB', 'CFB']
files = ["sam: hello world", "Frankenstein.txt",
         "Dickens.txt", "Joyce.txt", "Dumas.txt"]

CBC_Values = {"sam: hello world": [], "Frankenstein.txt": [],
              "Dickens.txt": [], "Joyce.txt": [], "Dumas.txt": []}

CTR_Values = {"sam: hello world": [], "Frankenstein.txt": [],
              "Dickens.txt": [], "Joyce.txt": [], "Dumas.txt": []}

ECB_Values = {"sam: hello world": [], "Frankenstein.txt": [
], "Dickens.txt": [], "Joyce.txt": [], "Dumas.txt": []}

OFB_Values = {"sam: hello world": [], "Frankenstein.txt": [
], "Dickens.txt": [], "Joyce.txt": [], "Dumas.txt": []}

CFB_Values = {"sam: hello world": [], "Frankenstein.txt": [],
              "Dickens.txt": [], "Joyce.txt": [], "Dumas.txt": []}


for mode in modes:
    for vals in modesDict.get(mode):
        if mode == "CBC":
            CBC_Values[vals[0]].append(vals[1])
        elif mode == "CTR":
            CTR_Values[vals[0]].append(vals[1])
        elif mode == "ECB":
            ECB_Values[vals[0]].append(vals[1])
        elif mode == "OFB":
            OFB_Values[vals[0]].append(vals[1])
        elif mode == "CFB":
            CFB_Values[vals[0]].append(vals[1])


CBC_Averages = {"sam: hello world":  0, "Frankenstein.txt":  0,
                "Dickens.txt": 0, "Joyce.txt":  0, "Dumas.txt":  0}

CTR_Averages = {"sam: hello world": 0, "Frankenstein.txt": 0,
                "Dickens.txt": 0, "Joyce.txt": 0, "Dumas.txt": 0}

ECB_Averages = {"sam: hello world": 0, "Frankenstein.txt": 0,
                "Dickens.txt": 0, "Joyce.txt": 0, "Dumas.txt": 0}

OFB_Averages = {"sam: hello world": 0, "Frankenstein.txt": 0,
                "Dickens.txt": 0, "Joyce.txt": 0, "Dumas.txt": 0}

CFB_Averages = {"sam: hello world": 0, "Frankenstein.txt": 0,
                "Dickens.txt": 0, "Joyce.txt": 0, "Dumas.txt": 0}


def Avg(lst):
    return round(sum(lst) / len(lst), 4)


for file in files:
    for key in CBC_Values.keys():
        if key == file:
            CBC_Averages[key] = Avg(CBC_Values.get(key))
    for key in CTR_Values.keys():
        if key == file:
            CTR_Averages[key] = Avg(CTR_Values.get(key))
    for key in ECB_Values.keys():
        if key == file:
            ECB_Averages[key] = Avg(ECB_Values.get(key))
    for key in OFB_Values.keys():
        if key == file:
            OFB_Averages[key] = Avg(OFB_Values.get(key))
    for key in CFB_Values.keys():
        if key == file:
            CFB_Averages[key] = Avg(CFB_Values.get(key))

files_sizes = ["sam: hello world (<1 kb)", "Frankenstein.txt (439kb)",
               "Dickens.txt (786kb)", "Joyce.txt (1550kb)", "Dumas.txt (2722kb)"]
CBC_y = [CBC_Averages["sam: hello world"], CBC_Averages["Frankenstein.txt"],
         CBC_Averages["Dickens.txt"], CBC_Averages["Joyce.txt"], CBC_Averages["Dumas.txt"]]
CTR_y = [CTR_Averages["sam: hello world"], CTR_Averages["Frankenstein.txt"],
         CTR_Averages["Dickens.txt"], CTR_Averages["Joyce.txt"], CTR_Averages["Dumas.txt"]]
ECB_y = [ECB_Averages["sam: hello world"], ECB_Averages["Frankenstein.txt"],
         ECB_Averages["Dickens.txt"], ECB_Averages["Joyce.txt"], ECB_Averages["Dumas.txt"]]
OFB_y = [OFB_Averages["sam: hello world"], OFB_Averages["Frankenstein.txt"],
         OFB_Averages["Dickens.txt"], OFB_Averages["Joyce.txt"], OFB_Averages["Dumas.txt"]]
CFB_y = [CFB_Averages["sam: hello world"], CFB_Averages["Frankenstein.txt"],
         CFB_Averages["Dickens.txt"], CFB_Averages["Joyce.txt"], CFB_Averages["Dumas.txt"]]

plt.xlabel('Files', fontweight='bold', color='blue',
           fontsize='13', horizontalalignment='center')
plt.ylabel('Runtime(ns)', fontweight='bold', color='blue',
           fontsize='13', horizontalalignment='center')
plt.plot(files_sizes, CBC_y, label="CBC Average Time")
plt.plot(files_sizes, CTR_y, label="CTR Average Time")
plt.plot(files_sizes, ECB_y, label="ECB Average Time")
plt.plot(files_sizes, OFB_y, label="OFB Average Time")
plt.plot(files_sizes, CFB_y, label="CFB Average Time")
plt.legend(loc='best')

plt.show()
