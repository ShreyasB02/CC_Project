# specify ubuntu version (same as the one I'm using)
#FROM ubuntu:22.04 
FROM python:3.10.6-slim
#RUN apt-get update
#WORKDIR /consumer_one
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY ./healthcheck.py /app/healthcheck.py


RUN pip install -r requirements.txt
#CMD [ "touch", "healthcheck.py" ]
#CMD [ "ls" ]
CMD ["python","healthcheck.py"]
