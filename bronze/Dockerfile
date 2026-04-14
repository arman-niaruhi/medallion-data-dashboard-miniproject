FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pandas==2.2.3

COPY generate_bronze.py /app/generate_bronze.py

CMD ["python", "/app/generate_bronze.py"]