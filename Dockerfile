FROM python:3.9.13-bullseye
WORKDIR /project
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "app.py","--host=127.0.0.1"]