FROM python:3.12.8

RUN apt-get install wget

WORKDIR /app
COPY pipeline.py pipeline.py
COPY requirements.txt requirements.txt


RUN pip install -r requirements.txt

ENTRYPOINT ["python", "pipeline.py"]
