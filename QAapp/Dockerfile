FROM python:3.8-alpine

COPY requirements.txt /home/requirements.txt

RUN apk update && apk add gcc python3-dev zlib-dev jpeg-dev musl-dev
RUN pip install --no-cache-dir -r /home/requirements.txt

WORKDIR /home/.

EXPOSE 8000

CMD ["python3" , "/home/manage.py" , "runserver" , "0.0.0.0:8000"]
