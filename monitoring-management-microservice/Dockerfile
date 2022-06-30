FROM python

WORKDIR /app/monitoring-management-microservice

COPY . ./

RUN ls -a

RUN apt-get update && apt-get -y dist-upgrade
RUN apt install -y netcat
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# CMD ["chmod", "u+x", "/wait-for.sh"]

# RUN apt-get update \
#     && apt-get -y install kafkacat\
#     && apt-get clean

# ENTRYPOINT ["sh", "./entrypoint.sh"]
