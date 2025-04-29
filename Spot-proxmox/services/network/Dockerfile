FROM python:3.11-slim


WORKDIR /APP

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
COPY . .


EXPOSE 5000


CMD [ "python" , "app.py" ]