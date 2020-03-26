import urllib, json
import csv
import os
import sys

from helpers import *

lastUpdate = getLastUpdate()

url = "https://especiais.g1.globo.com/bemestar/coronavirus/mapa-coronavirus/data/brazil-cases.json"
response = urllib.urlopen(url)
data = json.loads(response.read())

updatedAt = data['updated_at'].encode('utf-8').strip()
if (updatedAt != lastUpdate): addNewUpdateDate(updatedAt)

citiesData = data['docs']

createInitFile('all_data.csv', './')
addLineInFile('./all_data.csv', 'data; cases')


f=open("./Rdata/R/raw_data.csv", "w")
f.write("state; city_name; date; new_cases; city_cod; state_cod; count\n")
for data in citiesData:
    state = data['state'].encode('utf-8').strip()
    state_cod = data['state_cod']
    city_name = data['city_name'].encode('utf-8').strip()
    city_cod = data['city_cod']
    cases = data['cases']
    date = data['date'].encode('utf-8').strip()
    count = data['count']
    line = state + ";" + city_name + ";" + date + ";" + str(cases) + ";" + str(city_cod) + ";" + str(state_cod) + ";" + str(count) + "\n"
    f.write(line)

    checkFolder(state,'./data/')
f.close()

os.system("chmod +x ./Rdata/R/script.R")
os.system("./Rdata/R/script.R")
