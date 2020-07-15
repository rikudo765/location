FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install gunicorn

CMD gunicorn "main:create_app()"


