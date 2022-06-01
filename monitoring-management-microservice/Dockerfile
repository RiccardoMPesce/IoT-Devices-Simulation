FROM python

WORKDIR /monitoring-management-microservice

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# COPY ./app /monitoring-management-microservice/app
# COPY /../.env ./database/env

CMD ["python", "/monitoring-management-microservice/main.py"]