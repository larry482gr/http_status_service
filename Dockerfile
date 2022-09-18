FROM python:3.10.7-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000
EXPOSE 8001

CMD ["python3", "run.py"]