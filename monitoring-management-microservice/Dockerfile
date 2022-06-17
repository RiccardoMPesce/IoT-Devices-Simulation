FROM python

WORKDIR /app/monitoring-management-microservice

COPY . ./

RUN ls -a

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app",  "--reload", "--host", "0.0.0.0", "--port", "8000"]

# RUN apt-get update \
#     && apt-get -y install kafkacat\
#     && apt-get clean

# ENTRYPOINT ["sh", "./entrypoint.sh"]
