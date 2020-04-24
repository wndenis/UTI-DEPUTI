FROM python:3.6-slim
RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "app.py"]