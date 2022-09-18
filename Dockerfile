FROM python:3.10.7-alpine

RUN adduser --uid 3478 -D devuser
USER 3478

WORKDIR /home/devuser/app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["python3", "run.py"]