FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install django==4.2.5
RUN pip install requests
COPY . /app
RUN python manage.py makemigrations polls
RUN python manage.py sqlmigrate polls 0001
RUN python manage.py sqlmigrate polls 0002
RUN python manage.py migrate
RUN python manage.py createsuperuser --username admin --email juan.ortiz.sanchez@correounivalle.edu.co
#HTTP
EXPOSE 1544
#DATABASE
EXPOSE 80
#FOR RESOURCES API
EXPOSE 8080
#FOR COURSES API
EXPOSE 8090
#FOR AUTH API
EXPOSE 8060
CMD ["python", "manage.py", "runserver", "80"]
