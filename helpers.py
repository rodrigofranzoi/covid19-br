import os
import sys
import csv
import fileinput

from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

def initFiles():
    createInitFile('keys_states.csv', './')
    addLineInFile('./keys_states.csv', 'stateCod; state')
    createInitFile('keys_cities.csv', './')
    addLineInFile('./keys_cities.csv', 'stateCod; state; city; cityCod')
    createInitFile('brasil_cases.csv', './')
    addLineInFile('./brasil_cases.csv', 'data; cases')

def createRegionFile(region, path):
    r = region + '.csv'
    pth = path + r
    createInitFile(r, path)
    addLineInFile(pth, 'data; cases')

def checkFolder(folderName, folderPath):
    if not os.path.exists(folderPath + folderName):
        os.makedirs(folderPath + folderName)
        return 0
    else:
        return 1

def getLastUpdate():
    with open('lastUpdate.csv', 'r') as f:
        lines = f.read().splitlines()
        f.close()
        return lines[-1]

def addLineInFile(file, line):
    f=open(file, "a+")
    f.write(line +  '\n')
    f.close()

def addNewUpdateDate(line):
    addLineInFile('lastUpdate.csv', line)

def createInitFile(fileName, path):
    f=open(path+fileName, "w")
    f.close()

def addIfDoesNotExists(fileName, path, headerIndex, comparator, line):
    new_path = path + fileName
    flag = 0
    with open(new_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if (row[headerIndex] == comparator):
                flag = 1
                break
        csv_file.close()
    if (flag == 0):
        addLineInFile(new_path, line)

def addAtTheTable(fileName, path, headerIndex, comparator, sumIndex, value):
    new_path = path + fileName
    count = 0
    flag = 0
    valueToSum = value
    with open(new_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if (row[headerIndex] == comparator):
                flag = 1
                valueToSum += int(row[sumIndex])
                text = comparator + ';' + str(valueToSum)
                old_text = row[0] + ';' + str(row[1])
                replace(new_path, old_text, text)
                break
            count = count + 1

        l = comparator + ';' + str(valueToSum)
        if (flag == 0):
            addLineInFile(new_path, l)
        flag = 0

def replace(file_path, pattern, subst):
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    copymode(file_path, abs_path)
    remove(file_path)
    move(abs_path, file_path)
