import matplotlib.pyplot as plt
import numpy as np

# I know my method here is a bit clumsy, I was up the entire night, take pity lol

modes_file = open('algosTimeData.txt')

modesDict = {'ARC4':  [], 'AES': [],
             'TripleDES': [], 'Blowfish': [], 'SM4': []}

for line in modes_file:
    tokens = line.split('-')
    if tokens[0] == "ARC4":
        modesDict["ARC4"].append([tokens[1], int(tokens[2].strip())])
    else:
        modesDict[tokens[0]].append([tokens[2], int(tokens[3].strip())])


algos = ['ARC4', 'AES',
         'TripleDES', 'Blowfish', 'SM4']
files = ["sam: hello world", "Frankenstein.txt",
         "Dickens.txt", "Joyce.txt", "Dumas.txt"]
# averages = {'ARC4':  [], 'AES': [],
#              'TripleDES': [], 'Blowfish': [], 'SM4': []}

ARC4_Values = {"sam: hello world": [], "Frankenstein.txt": [],
               "Dickens.txt": [], "Joyce.txt": [], "Dumas.txt": []}

AES_Values = {"sam: hello world": [], "Frankenstein.txt": [],
              "Dickens.txt": [], "Joyce.txt": [], "Dumas.txt": []}

TripleDES_Values = {"sam: hello world": [], "Frankenstein.txt": [
], "Dickens.txt": [], "Joyce.txt": [], "Dumas.txt": []}

Blowfish_Values = {"sam: hello world": [], "Frankenstein.txt": [
], "Dickens.txt": [], "Joyce.txt": [], "Dumas.txt": []}

SM4_Values = {"sam: hello world": [], "Frankenstein.txt": [],
              "Dickens.txt": [], "Joyce.txt": [], "Dumas.txt": []}


for algo in algos:
    for vals in modesDict.get(algo):
        if algo == "ARC4":
            ARC4_Values[vals[0]].append(vals[1])
        elif algo == "AES":
            AES_Values[vals[0]].append(vals[1])
        elif algo == "TripleDES":
            TripleDES_Values[vals[0]].append(vals[1])
        elif algo == "Blowfish":
            Blowfish_Values[vals[0]].append(vals[1])
        elif algo == "SM4":
            SM4_Values[vals[0]].append(vals[1])


ARC4_Averages = {"sam: hello world":  0, "Frankenstein.txt":  0,
                 "Dickens.txt": 0, "Joyce.txt":  0, "Dumas.txt":  0}

AES_Averages = {"sam: hello world": 0, "Frankenstein.txt": 0,
                "Dickens.txt": 0, "Joyce.txt": 0, "Dumas.txt": 0}

TripleDES_Averages = {"sam: hello world": 0, "Frankenstein.txt": 0,
                      "Dickens.txt": 0, "Joyce.txt": 0, "Dumas.txt": 0}

Blowfish_Averages = {"sam: hello world": 0, "Frankenstein.txt": 0,
                     "Dickens.txt": 0, "Joyce.txt": 0, "Dumas.txt": 0}

SM4_Averages = {"sam: hello world": 0, "Frankenstein.txt": 0,
                "Dickens.txt": 0, "Joyce.txt": 0, "Dumas.txt": 0}


def Avg(lst):
    return round(sum(lst) / len(lst), 4)


for file in files:
    for key in ARC4_Values.keys():
        if key == file:
            ARC4_Averages[key] = Avg(ARC4_Values.get(key))
    for key in AES_Values.keys():
        if key == file:
            AES_Averages[key] = Avg(AES_Values.get(key))
    for key in Blowfish_Values.keys():
        if key == file:
            Blowfish_Averages[key] = Avg(Blowfish_Values.get(key))
    for key in TripleDES_Values.keys():
        if key == file:
            TripleDES_Averages[key] = Avg(TripleDES_Values.get(key))
    for key in SM4_Values.keys():
        if key == file:
            SM4_Averages[key] = Avg(SM4_Values.get(key))

files_sizes = ["sam: hello world (<1 kb)", "Frankenstein.txt (439kb)",
               "Dickens.txt (786kb)", "Joyce.txt (1550kb)", "Dumas.txt (2722kb)"]
ARC4_y = [ARC4_Averages["sam: hello world"], ARC4_Averages["Frankenstein.txt"],
          ARC4_Averages["Dickens.txt"], ARC4_Averages["Joyce.txt"], ARC4_Averages["Dumas.txt"]]
AES_y = [AES_Averages["sam: hello world"], AES_Averages["Frankenstein.txt"],
         AES_Averages["Dickens.txt"], AES_Averages["Joyce.txt"], AES_Averages["Dumas.txt"]]
TripleDES_y = [TripleDES_Averages["sam: hello world"], TripleDES_Averages["Frankenstein.txt"],
               TripleDES_Averages["Dickens.txt"], TripleDES_Averages["Joyce.txt"], TripleDES_Averages["Dumas.txt"]]
Blowfish_y = [Blowfish_Averages["sam: hello world"], Blowfish_Averages["Frankenstein.txt"],
              Blowfish_Averages["Dickens.txt"], Blowfish_Averages["Joyce.txt"], Blowfish_Averages["Dumas.txt"]]
SM4_y = [SM4_Averages["sam: hello world"], SM4_Averages["Frankenstein.txt"],
         SM4_Averages["Dickens.txt"], SM4_Averages["Joyce.txt"], SM4_Averages["Dumas.txt"]]

plt.xlabel('Files', fontweight='bold', color='blue',
           fontsize='13', horizontalalignment='center')
plt.ylabel('Runtime(ns)', fontweight='bold', color='blue',
           fontsize='13', horizontalalignment='center')
plt.plot(files_sizes, ARC4_y, label="ARC4 Average Time")
plt.plot(files_sizes, AES_y, label="AES Average Time")
plt.plot(files_sizes, TripleDES_y, label="TripleDES Average Time")
plt.plot(files_sizes, Blowfish_y, label="Blowfish Average Time")
plt.plot(files_sizes, SM4_y, label="SM4 Average Time")
plt.legend(loc='best')
print("hi")
plt.show()
