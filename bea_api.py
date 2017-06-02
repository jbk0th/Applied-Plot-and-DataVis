import urllib
import json
import pandas as pd
import numpy as np
import requests
import os
import csv


## write script so you can ask questions to the bea server in an easy wasy  with url 
## fields with your key, and other req info
## then also help with things that you want to ask for

## coursera dr chuck and bea application for getting the data out.

os.chdir('C:\\Users\\Jason\\Applied-Plot-and-DataVis')
	### changes in the directory to be able to call this script

api_key = 'CD6F23EF-CCDE-48BC-B984-93A3650F85BB'

pre_url = 'https://www.bea.gov/api/data?&UserID=CD6F23EF-CCDE-48BC-B984-93A3650F85BB-Key&method='

url_cap = '&ResultFormart=JSON'

to_do = input('What would you like to do: \n')\

### Ann Arbor michigan key = 11460


if to_do == 'get':
	
	api_method = input('Enter in desired api method: \n')
		# to get the list of industries with info available
		#GetParameterValues&DataSetName=underlyingGDPbyIndustry&ParameterName=Industry
	
	get_url = pre_url + api_method + url_cap
	
	get_obj = requests.get(get_url)
		### get_obj - the response object from the api

	print(json.dumps(get_obj.json(), sort_keys=True, indent=4))
		### for the json dump to be able manipulate this, this passed			in obj needs to be a json one. CANNOT forget to finish the methods with ()!!
	
if to_do == 'michigan_GDP':

	get_url = pre_url + 'GetData&DataSetName=RegionalProduct&Component=RGDP_SAN&IndustryID=1&Year=ALL&GeoFips=26000' + url_cap
	
	get_michGDP = requests.get(get_url)
	
	AnnArbor_url = pre_url + 'GetData&datasetname=RegionalProduct&Component=RGDP_MAN&IndustryId=1&Year=ALL&GeoFips=11460' + url_cap
	
	get_AnnArborGDP = requests.get(AnnArbor_url)
	mich_GDP = json.dumps(get_michGDP.json(), sort_keys=True, indent=4)
	### Deserialize JSON data into a string. #THIS is confirmed string now, NOT JSON/Response object because cannot call methods on it 
	### pretty sure this is a string obj now and not a JSON obj because cannot get it to query like a JSON obj
	Ann_ArborGDP = json.dumps(get_AnnArborGDP.json(), sort_keys=True, indent=4)
	js = json.loads(mich_GDP)
	
	jsAA = json.loads(Ann_ArborGDP)
		# the serializes the string back into JSON format for python to read like a dict
		# to start to query this need call ['BEAAPI'], then the other objects are under it as keys
		# js['BEAAPI']['Results']['Data'] the data is stored in here as a LIST of dicts so can and should call by num
		# Can of course iterate through the list of dicts ... b/c its a list like so
		# for obj in (js['BEAAPI']['Results']['Data']): just grab the keys one would like
	
	mich_GDPdict = dict()
	
	res = js['BEAAPI']['Results']['Data']
	
	Ann_res = jsAA['BEAAPI']['Results']['Data']
	
	mich_GDPdict[0] = ['CL_UNIT', 'DataValue', 'GeoName', 'Timeperiod', 'UNIT_MULT']
	for obj, i in zip(res ,range(len(res))):
		
		dummy_list = list()
		# for each new object in JSON read creates a list with its entry in it
		
		dummy_list.append(obj['CL_UNIT'])
		dummy_list.append(obj['DataValue'])
		dummy_list.append(obj['GeoName'])
		dummy_list.append(obj['TimePeriod'])
		dummy_list.append(obj['UNIT_MULT'])
			# add all of these into the dict as an entry 
		mich_GDPdict[(i+1)] = dummy_list
	for obj, i in zip(Ann_res, range(len(Ann_res))):
		
		i = i + len(mich_GDPdict)
		dummy_list = list()
		# for each new object in JSON read creates a list with its entry in it
		
		dummy_list.append(obj['CL_UNIT'])
		dummy_list.append(obj['DataValue'])
		dummy_list.append(obj['GeoName'])
		dummy_list.append(obj['TimePeriod'])
		dummy_list.append(obj['UNIT_MULT'])
		mich_GDPdict[i] = dummy_list
			# add all of these into the dict as an entry 
	
		


### to be able to interact with the output of a script after its called append the python with -i i.e:
	# python -i bea_api.py
with open("mich_GDP.csv", "w", newline='') as fi_obj:
		writer = csv.writer(fi_obj, dialect='excel')
		for num, info in mich_GDPdict.items():
			writer.writerow(info)
	# second argument has characters decribing how the file will be used
		# 'r' when only used to read
		# 'w' for only writing
		# 'a' opens file for appending, any data automatically written to the end
		# 'r+' opens the file for both read and write
		# normally files opened in txt mode  means that read/write strings from and to a file, which are encoded in a specific encoding
		# 'b' is appended to the mode opens the file in BINARY MODE, now data is read/written in bytes objects, SHOULD BE USED FOR ALL FILES THAT DO NOT
		# CONTAIN TEXT


