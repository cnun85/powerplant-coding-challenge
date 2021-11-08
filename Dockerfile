# base images
FROM python:3.8.3
# workdir is used to set the pwd inside docker container
WORKDIR /code
COPY requirements.txt /requirements.txt
# Install pip dependency.
RUN pip install -r /requirements.txt
# copy whole directory inside /code working directory.
COPY . /code
# This command execute at the time when container start.
CMD ["python3", "servi.py","client.py"]
