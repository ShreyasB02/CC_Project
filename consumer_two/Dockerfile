# specify ubuntu version (same as the one I'm using)

FROM python:3.10.6
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY ./insertion.py /app/insertion.py

RUN pip install -r requirements.txt

CMD ["python","insertion.py"]
