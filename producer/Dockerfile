# DockerFile for producer.
FROM python:3.10.6
WORKDIR /producer
RUN apt-get update
RUN pip install -r requirements.txt
CMD ["python", "producer.py"]


