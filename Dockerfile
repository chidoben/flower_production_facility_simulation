FROM python:alpine3.7
COPY . /app
WORKDIR /app
CMD python ./flower_production_facility.py