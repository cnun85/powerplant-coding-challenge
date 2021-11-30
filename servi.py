#powerplant-challenge application
#Server module which listens to a POST request and make the response

from flask import Flask
import json
from flask import request,jsonify, make_response
import logging
import pplan


app = Flask(__name__)

#logging management
logging.basicConfig(filename='runtime.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# methods after this line

	
@app.route("/productionplan", methods=['POST'])
def json_example():
    
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    if request.is_json:
        req = request.get_json()
        app.logger.debug("JSON recieved:")
        app.logger.debug(req)
        
        power=pplan.Powerplant(req)
        result=power.production()
        
        result = make_response(jsonify(result), 200)
        
        app.logger.info('Operation completed succesfully:')
        app.logger.info(result)
        app.logger.info("\n")
        app.logger.info("\n")
        app.logger.info("\n")
        
        return result
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)
        app.logger.info('Fail:Request body must be JSON')

	
if __name__ == "__main__":
	#app init
    app.run(debug=True,port=8888)