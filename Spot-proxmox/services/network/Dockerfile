FROM python:3.11-slim


WORKDIR /APP

COPY requirement.txt requirement.txt

RUN pip install --no-cache-dir -r requirement.txt
COPY . .


EXPOSE 5002


CMD [ "python" , "network.py" ]