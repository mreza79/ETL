FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt  --upgrade pip
COPY /app /app
CMD [ "python3", "main.py"]