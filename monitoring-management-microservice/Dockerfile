FROM python

WORKDIR /monitoring-management-microservice

COPY ./requirements.txt /monitoring-management-microservice/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /monitoring-management-microservice/requirements.txt

# COPY ./app /monitoring-management-microservice/app
COPY .env /monitoring-management-microservice/app/repository/.env 

CMD ["python", "app/main.py"]