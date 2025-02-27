FROM python:3.9-slim

ENV DYNAMO_DB_ACCESS_KEY = ""
ENV DYNAMO_DB_SECRET_KEY = ""

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]