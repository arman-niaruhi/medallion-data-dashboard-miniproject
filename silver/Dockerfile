FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pandas==2.2.3

COPY build_silver.py /app/build_silver.py

CMD ["python", "/app/build_silver.py"]