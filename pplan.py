#powerplant-challenge application
#pplan module which has the functions that read a JSON, define the merit order in use of a powerplant
#and calculates the power each powerplant needs to produce to fullfill the requested load 

import json
import logging

logger = logging.getLogger('runtime.log')
 
def json_reading(nombre):

	# Opening JSON file
	f = open(nombre,)
	 
	# returns JSON object as
	# a dictionary
	data = json.load(f)
	# Closing file
	f.close()
	return data

class Powerplant:
    
    def __init__(self, payload):
        #the json of the payload
        self.payload=payload
        self.load=payload["load"]
        self.powerplants=payload["powerplants"]
        self.fuels=payload["fuels"]

    def merit_order(self):
        tons_Mwh=0.3
        euro_wind=0
        #add merit_order euro/MWh to the powerplants including the c02
        for i in self.powerplants:
            if i["type"]=="gasfired":
                i["merit_order"]=round(self.fuels["gas(euro/MWh)"]/i["efficiency"]*self.fuels["co2(euro/ton)"]*tons_Mwh,2)
            if i["type"]=="turbojet":
                i["merit_order"]=round(self.fuels["kerosine(euro/MWh)"]/i["efficiency"],2)
            if i["type"]=="windturbine":
                i["merit_order"]=euro_wind	
            
        #set order in dictionary by merit_order	
        sort_powerplants_by_merit = sorted(self.powerplants, key=lambda x: x["merit_order"])
        
        return sort_powerplants_by_merit	
        
        
    def production(self):

        #power_load=dict["load"]
        power_load=self.load
        
        power_left=power_load
        power_supplied_total=0.0
        power_supplied_this_powerplant=0.0
        pmin_previous=0
        pmax_previous=0
        
        #response=dict["powerplants"]
        response=self.merit_order()
        aux=0
            
        logger.info(response)
        
        logger.info("power_load: %s",power_load) #shows the power_load
        aux=0 #variable that is the index of previous read powerplants
        extra_flag=0
        pmin_extra=0
        two_need=False #variable that determines the need of combine 2 powerplants to obtain the power
        for i in response: #going through the dictionay of the powerplants
            
            logger.info("power_supplied_total until now %s", power_supplied_total) #power supplied shown in each iteraction
            logger.info("power left %s", power_left) #energy left to satisfy demand
            
            name=i["name"]
            
            logger.info("powerplant to process %s" ,i["name"]) #next powerplant in the loop
            
            if power_supplied_total<power_load:
                
                #manage the windturbines
                if (i["type"]=="windturbine"):				
                    if (self.fuels["wind(%)"]!=0):
                        logger.info("managing windturbines")
                        
                        if power_left<i["pmax"]*self.fuels["wind(%)"]/100:
                            power_supplied_this_powerplant=power_left
                            power_supplied_total=power_supplied_total+power_supplied_this_powerplant
                            power_left=power_left-power_supplied_this_powerplant
                            response[aux]["p"]=power_supplied_this_powerplant
                            logger.info("Enough with this windturbine to fullfill the load")
                            
                        else:
                            power_supplied_this_powerplant=i["pmax"]*self.fuels["wind(%)"]/100
                            power_supplied_total=power_supplied_total+power_supplied_this_powerplant
                            power_left=power_left-power_supplied_this_powerplant
                            response[aux]["p"]=power_supplied_this_powerplant
                            logger.info("this windturbine powerplant is not enough to fullfill the load")
                            
                    logger.info('power supplied %s %s', i["name"], str(power_supplied_this_powerplant))
                    logger.info('power_left %s power_supplied_total %s',str(power_left), str(power_supplied_total))
                    

                #manage rest of powerplants following merit order
                else:
                    
                    if power_left>=i["pmin"]+pmin_previous:#switching on this powerplant
                        logger.info("switching on %s",i["name"])
                        if power_left<=i["pmax"] and two_need==False:#this powerplant is  enough to fullfill the load
                            logger.info("this powerplant is  enough to fullfill the load %s",i["name"])
                            power_supplied_this_powerplant=power_left
                            power_supplied_total=power_supplied_total+power_supplied_this_powerplant
                            power_left=power_left-power_supplied_this_powerplant
                            response[aux]["p"]=power_supplied_this_powerplant
                            logger.info(power_supplied_this_powerplant)
                            logger.info(power_left)
                        elif (power_left>=i["pmin"]+pmin_previous) and (power_left<=i["pmax"]+pmax_previous): #switching on this powerplant and the previous tha can be switched on (based on pmin requisite)
                            #ambas aportan su pmin
                            logger.info("this powerplant is  enough to fullfill the load %s y %s",i["name"],nombre_previous)
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
                                if i["name"]==list(self.powerplants)[-1]["name"]:#last powerplant and demand is not fullfill. Switching on to pmax
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
                        logger.info("not switching on %s because of pmin exceeding power_left", i["name"])				
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
                for i in response:
                    if aux>=aux_extra: #rest powerplants to 0 because demand is overloaded by the previous
                        i["p"]=0
                    aux=aux+1
                logger.info("switching on %s to respond demand even if the system is overloaded", nombre_extra)
                response[aux_extra]["p"]=pmin_extra
                power_supplied_total=power_supplied_total+pmin_extra
                power_left=power_left-pmin_extra
        
        logger.info("power_supplied_total until now %s",power_supplied_total) #each itation shows power supplied 
        
        logger.info("power left %s", power_left)#energy left to satisfy demand
        
        resultado=self.format_result()
        
        #print(response)
        return resultado
        
    def format_result(self):
        resultado=self.powerplants
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