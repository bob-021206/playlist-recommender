FROM python:3.9-slim

WORKDIR /app
COPY ml.py /app
RUN pip install fpgrowth-py pandas

CMD ["python", "ml.py"]
