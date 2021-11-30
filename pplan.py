#powerplant-challenge application
#pplan module which has the functions that read a JSON, define the merit order in use of a powerplant
#and calculates the power each powerplant needs to produce to fullfill the requested load 

import json
 
def json_reading(nombre):

	# Opening JSON file
	f = open(nombre,)
	 
	# returns JSON object as
	# a dictionary
	data = json.load(f)
	# Closing file
	f.close()
	return data

def merit_order(dict):
	tons_Mwh=0.3
	euro_wind=0
	#add merit_order euro/MWh to the powerplants including the c02
	for i in dict["powerplants"]:
		if i["type"]=="gasfired":
			i["merit_order"]=round(dict["fuels"]["gas(euro/MWh)"]/i["efficiency"]*dict["fuels"]["co2(euro/ton)"]*tons_Mwh,2)
		if i["type"]=="turbojet":
			i["merit_order"]=round(dict["fuels"]["kerosine(euro/MWh)"]/i["efficiency"],2)
		if i["type"]=="windturbine":
			i["merit_order"]=euro_wind	
		
	#set order in dictionary by merit_order	
	sort_powerplants_by_merit = sorted(dict["powerplants"], key=lambda x: x["merit_order"])
	
	#print(sort_powerplants_by_merit)
	dict["powerplants"]=sort_powerplants_by_merit
	return dict	
	
	
def production(dict):

	power_load=dict["load"]
	power_left=power_load
	power_supplied_total=0.0
	power_supplied_this_powerplant=0.0
	pmin_previous=0
	pmax_previous=0
	
	response=dict["powerplants"]
	#print(response)
	aux=0
		
	#print(response)
	print(" ")
	
	print("power_load " ,power_load) #shows the power_load
	aux=0 #variable that is the index of previous read powerplants
	extra_flag=0
	pmin_extra=0
	two_need=False #variable that determines the need of combine 2 powerplants to obtain the power
	for i in dict["powerplants"]: #going through the dictionay of the powerplants
		print(" ")
		print("power_supplied_total until now ",power_supplied_total) #power supplied shown in each iteraction
		print("power left ",power_left)#energy left to satisfy demand
		print(" ")
		print("powerplant to process ",i["name"]) #next powerplant in the loop
		
		if power_supplied_total<power_load:
			
			#manage the windturbines
			if (i["type"]=="windturbine"):				
				if (dict["fuels"]["wind(%)"]!=0):
					print("managing windturbines")
					
					if power_left<i["pmax"]*dict["fuels"]["wind(%)"]/100:
						power_supplied_this_powerplant=power_left
						power_supplied_total=power_supplied_total+power_supplied_this_powerplant
						power_left=power_left-power_supplied_this_powerplant
						response[aux]["p"]=power_supplied_this_powerplant
						print("Enough with this windturbine to fullfill the load")
						
					else:
						power_supplied_this_powerplant=i["pmax"]*dict["fuels"]["wind(%)"]/100
						power_supplied_total=power_supplied_total+power_supplied_this_powerplant
						power_left=power_left-power_supplied_this_powerplant
						response[aux]["p"]=power_supplied_this_powerplant
						print("this windturbine powerplant is not enough to fullfill the load")
						
				print("power supplied " +i["name"]+" , " +str(power_supplied_this_powerplant))
				print("power_left "+ str(power_left)+ " power_supplied_total "+ str(power_supplied_total))

			#manage rest of powerplants following merit order
			else:
				
				if power_left>=i["pmin"]+pmin_previous:#switching on this powerplant
					print("switching on ",i["name"])
					if power_left<=i["pmax"] and two_need==False:#this powerplant is  enough to fullfill the load
						print("this powerplant is  enough to fullfill the load ",i["name"])
						power_supplied_this_powerplant=power_left
						power_supplied_total=power_supplied_total+power_supplied_this_powerplant
						power_left=power_left-power_supplied_this_powerplant
						response[aux]["p"]=power_supplied_this_powerplant
						print(power_supplied_this_powerplant)
						print(power_left)
					elif (power_left>=i["pmin"]+pmin_previous) and (power_left<=i["pmax"]+pmax_previous): #switching on this powerplant and the previous tha can be switched on (based on pmin requisite)
						#ambas aportan su pmin
						print("this powerplant is  enough to fullfill the load "+i["name"]+" y "+nombre_previous)
						two_need=False
						
						power_supplied_this_powerplant=i["pmin"]#power supplied by this powerplant
						power_supplied_previous_powerplant=pmin_previous#power supplied by the previous
						power_supplied_total=power_supplied_total+power_supplied_this_powerplant+power_supplied_previous_powerplant
						power_left=power_left-power_supplied_this_powerplant-power_supplied_previous_powerplant
						#print(power_left, power_supplied_total)
						#calculating power from pmins of both
						power_left_in_previous_powerplant=pmax_previous-pmin_previous
						power_left_in_current_powerplant=i["pmax"]-i["pmin"]
						if power_left<=power_left_in_previous_powerplant:#current powerplant supplies the pmin and the previous supplied the rest
							power_supplied_previous_powerplant=power_supplied_previous_powerplant+power_left
							power_supplied_total=power_supplied_total+power_left
							response[aux]["p"]=power_supplied_this_powerplant
							response[aux_previous]["p"]=power_supplied_previous_powerplant
							power_left=power_left-power_left
							#print(power_left)

							
						else:
							#print(power_left, power_supplied_total)
							
							#previous powerplant supplies its pmax
							power_supplied_previous_powerplant=power_supplied_previous_powerplant+power_left_in_previous_powerplant
							power_supplied_total=power_supplied_total+power_left_in_previous_powerplant #update power_supplied_total
							power_left=power_left-power_left_in_previous_powerplant #update power_left
							#print(power_left, power_supplied_total)
							power_supplied_this_powerplant=power_supplied_this_powerplant+power_left #current supplies until load complete
							power_supplied_total=power_supplied_total+power_left
							power_left=power_left-power_left
							#print(power_left,power_supplied_total)
							response[aux]["p"]=power_supplied_this_powerplant
							response[aux_previous]["p"]=power_supplied_previous_powerplant
					else:
						if pmax_previous>0:#checking if there is previous data. if not, its the first powerplant under processing
							response[aux_previous]["p"]=pmax_previous
							power_supplied_total=power_supplied_total+pmax_previous
							power_left=power_left-pmax_previous
							pmax_previous=0
							two_need=False
							if i["name"]==list(dict["powerplants"])[-1]["name"]:#last powerplant and demand is not fullfill. Switching on to pmax
								response[aux]["p"]=i["pmax"]
								power_supplied_total=power_supplied_total+i["pmax"]
								power_left=power_left-i["pmax"]
								
						else:
							two_need=True
						pmin_previous=i["pmin"]
						pmax_previous=i["pmax"]
						nombre_previous=i["name"]
						aux_previous=aux
				else:#this powerplant will be switched on only if the demand is not fullfill
					print("not switching on "+i["name"]+ " because of pmin exceeding power_left")				
					if extra_flag==0:
						pmin_extra=i["pmin"]
						pmax_extra=i["pmax"]
						nombre_extra=i["name"]
						aux_extra=aux
						extra_flag=1
		aux=aux+1				
					
	if power_supplied_total<power_load: #no powerplant fullfill requisites so the first possible by merit order is switched on
		if extra_flag==1:
			aux=0
			for i in dict["powerplants"]:
				if aux>=aux_extra: #rest powerplants to 0 because demand is overloaded by the previous
					i["p"]=0
				aux=aux+1
			print("switching on "+nombre_extra+ " to respond demand even if the system is overloaded")
			response[aux_extra]["p"]=pmin_extra
			power_supplied_total=power_supplied_total+pmin_extra
			power_left=power_left-pmin_extra
	
	print("power_supplied_total until now ",power_supplied_total) #each itation shows power supplied 
	print("power left ",power_left)#energy left to satisfy demand
	
	#print(response)
	return dict
	
def format_result(dict):
    resultado=dict["powerplants"]
    #formatting result
    aux=0
    for i in resultado:
        del i["type"],i["pmin"],i["pmax"],i["efficiency"],i["merit_order"]
        if "p" not in i:
            resultado[aux]["p"]=0
        aux=aux+1
    return resultado


if __name__ == "__main__":

	# data=json_reading('payload1.json')

	# print(" ")
	# data_ordenada=merit_order(data)
	# production(data)
	
	# print(" ")
	print(data)
	# resultado=data["powerplants"]
	# aux=0

	# for i in resultado:	
		# del i["type"],i["pmin"],i["pmax"],i["efficiency"],i["merit_order"]
		# if "p" not in i:
			# resultado[aux]["p"]=0			
		# aux=aux+1
	
	
	# print(" ")
	# print(resultado)
	# json_object = json.dumps(resultado, indent = 4)
	# with open("sample.json", "w") as outfile:
		# outfile.write(json_object)