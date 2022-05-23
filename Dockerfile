FROM python

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./app /code/app
COPY ./.env /code/app/repository/ 

CMD ["python", "app/main.py"]