# Powerplant-coding-challenge

It has been built using Python 3.8 with Flask.

## Instalation
There are two ways to prepare the environment for running the application. One is to install it as a Python project, the other is to run it as a docker container.

### 1. Basic Python installation

Install Python 3 (Python 3.8 used in this app)

*It is recommended to do the next in a Virtual Environment.

Make the virtual environment:

	$ cd powerplant-coding-challenge
	$ py -3 -m venv venv
	$ venv\Scripts\activate

Install dependencies:

	$ pip3 install -r requirements.txt

#### Running the application server:

	$ python3 servi.py

#### POST request:
*Be aware, if you run the application with Docker first, the port 8888 is going to be in use by the docker container so the execution with this method will fail unless you remove it

In a new terminal run the client:

	$ cd powerplant-coding-challenge
	$ venv\Scripts\activate
	$ python3 client.py

If you want to exit the application:

	$ CTRL + C

If you want to leave the virtual environment:

	$ deactivate

### 2. Using Docker (requires docker installation first)
If you prefer to run the application within Docker you need to execute the .bat file called lotes.bat :

In a new terminal:

	$ cd powerplant-coding-challenge
	$ lotes.bat

If you want to check or extract the generated content, run the next command to enter the docker bash

	docker ps #to check the container_id
	docker exec -t -i <container_id> /bin/bash




