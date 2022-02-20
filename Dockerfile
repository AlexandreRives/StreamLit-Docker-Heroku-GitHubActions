FROM python:3.8-slim

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

CMD streamlit run --server.port $PORT app.py