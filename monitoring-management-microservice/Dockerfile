FROM python

WORKDIR /app/monitoring-management-microservice

COPY . ./

RUN ls -a

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# RUN apt-get update \
#     && apt-get -y install kafkacat\
#     && apt-get clean

# ENTRYPOINT ["sh", "./entrypoint.sh"]
