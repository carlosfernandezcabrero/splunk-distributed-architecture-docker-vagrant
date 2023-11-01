FROM python:3.12-alpine3.18
COPY ./receive.py ./receive.py
COPY ./.env ./.env
RUN pip install --no-cache pika python-dotenv
CMD python ./receive.py