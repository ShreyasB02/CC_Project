# DockerFile for producer.
FROM python:3.10.6-slim
#RUN apt-get update
#WORKDIR /consumer_one
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY ./producer.py /app/producer.py


RUN pip install -r requirements.txt
#CMD [ "touch", "healthcheck.py" ]
#CMD [ "ls" ]
CMD ["python","producer.py"]
