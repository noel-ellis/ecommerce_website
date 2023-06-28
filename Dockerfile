FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/ecomm
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000