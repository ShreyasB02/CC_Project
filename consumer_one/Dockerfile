# specify ubuntu version (same as the one I'm using)
#FROM ubuntu:22.04 
FROM python:3.10.6-slim
RUN apt-get update
#WORKDIR /consumer_one
COPY requirements.txt /tmp
WORKDIR /tmp

RUN pip install -r requirements.txt
#CMD [ "touch", "healthcheck.py" ]
COPY /consumer_one/healthcheck.py /tmp/healthcheck.py
CMD ["python","healthcheck.py"]
