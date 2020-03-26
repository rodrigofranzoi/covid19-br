import urllib, json
import csv
import os
import sys

from helpers import *

def alguma_func(a):
    return a

initFiles()
lastUpdate = getLastUpdate()

checkFolder('data', "./")

url = "https://especiais.g1.globo.com/bemestar/coronavirus/mapa-coronavirus/data/brazil-cases.json"
response = urllib.urlopen(url)
data = json.loads(response.read())

updatedAt = data['updated_at'].encode('utf-8').strip()

if (updatedAt != lastUpdate): addNewUpdateDate(updatedAt)

citiesData = data['docs']

createInitFile('all_data.csv', './')
addLineInFile('./all_data.csv', 'data; cases')


f=open("json_data.json", "w+")
f.write(citiesData)
f.close()

data = pd.read_json("json_data.json")
data.to_csv("data")
print data

# for data in citiesData:
#     state = data['state'].encode('utf-8').strip()
#     stateCod = data['state_cod']
#     city = data['city_name'].encode('utf-8').strip()
#     cityCod = data['city_cod']
#     cases = data['cases']
#     date = data['date']
    #
    # if (checkFolder(state,'./data/') == 0):
    #     p = './data/' + state.upper() + '/'
    #     createRegionFile(state, p)
    #     line = str(stateCod) + ';' + state
    #     addLineInFile('./keys_states.csv', line)
    # line = str(stateCod) + ';' + state + ';' + city + ';' + str(cityCod)
    #
    # addIfDoesNotExists('keys_cities.csv', '', 3, str(cityCod), line)
    # addAtTheTable('brasil_cases.csv', '', 0, date, 1, cases)
