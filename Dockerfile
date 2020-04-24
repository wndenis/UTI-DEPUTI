FROM python:3.6-slim
EXPOSE 5554
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "app.py"]