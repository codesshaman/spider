#import sys
#import argvs
import files

#arguments = sys.argv
#distr = argvs.argv_proc_gs(arguments)
#print(argvs)

json_file = files.open_json('cities.json')
json_file.reverse()
for city in json_file:
    print("id: " + str(city['_id']) + ", город: " + city['city'] + " население: " + str(city['population']) + ", страна: " + str(city['country']))

