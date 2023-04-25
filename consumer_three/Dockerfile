# specify ubuntu version (same as the one I'm using)

FROM python:3.10.6-slim
RUN apt-get update
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY ./deletion.py /app/deletion.py
RUN pip install -r requirements.txt
CMD ["python","deletion.py"]
