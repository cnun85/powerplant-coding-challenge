docker build -t proyecto .

docker run -d -p 8888:8888 proyecto:latest


FOR /F %%i IN ('docker ps') DO set VARIABLE=%%i

docker exec -it %VARIABLE% bash -c "python3 client.py"




