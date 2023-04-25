# specify ubuntu version (same as the one I'm using)
FROM python:3.10.6-slim
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY ./read.py /app/read.py
RUN pip install -r requirements.txt
CMD ["python","read.py"]
