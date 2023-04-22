# specify ubuntu version (same as the one I'm using)

FROM python:3.10.6
WORKDIR /consumer_three
RUN apt-get update
RUN pip install -r requirements.txt

CMD ["python","deletion.py"]
