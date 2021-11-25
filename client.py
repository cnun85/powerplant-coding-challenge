#powerplant-challenge application
#Client module which reads JSON from file and send a request method to the server


import requests
import os
# Python program to read
# json file
 
 
import json
 
path = "example_payloads/"
dirs = os.listdir( path )
numero_de_salida=1

#iterates on all the files "payloads" in folder
for file in dirs:
	print(" ")
	print (file)
	print(" ")
	f = open('example_payloads/'+file+'',)
	
	# returns JSON object as
	# a dictionary
	data = json.load(f)

	# Closing file
	f.close()

	# error if no response
	url = "http://localhost:8888/productionplan"

	response = requests.post(url, json = data)
	dicc=response.json()
	#format json
	json_object = json.dumps(dicc, indent = 4)

	# save json response to file
	with open("response"+str(numero_de_salida)+".json", "w") as outfile:
		outfile.write(json_object)

	print(json_object)
	numero_de_salida=numero_de_salida+1