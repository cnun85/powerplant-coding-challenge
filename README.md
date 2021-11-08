powerplant-coding-challenge

It has been built using Python 3.8 with Flask.

Install Python 3 (Python 3.8 used in this app)

python.org
Clone repository

$ cd path/to/where/you/want/it
$ git clone https://github.com/cnun85/powerplant-coding-challenge.git



There are two main ways prepare the environment for running the application. One is to simply install it as a Python project. The other is to run it as docker container.

Basic Python installation

*It is recommended to do this in a Virtual Environment.
Make the virtual environment

$ cd powerplant-coding-challenge
$ py -3 -m venv venv
$ venv\Scripts\activate

Install dependencies

$ pip3 install -r requirements.txt

Running the application

$ python3 servi.py

POST request
In a new terminal run the client
$ cd powerplant-coding-challenge
$ venv\Scripts\activate
$ python3 client.py

Exit the application

CTRL + C

Leave the virtual environment

$ deactivate

Using Docker
If you prefer to run the application within Docker you need to execute the .bat file called lotes:

in anew terminal:
$ cd powerplant-coding-challenge
$ lotes.bat

If you want to check or extract the generated content, run the next command

	docker ps #to check the container_id
	docker exec -t -i <container_id> /bin/bash




