FROM ubuntu:20.04
RUN apt-get update && apt-get install -y tzdata && apt install -y python3.9 python3-pip
RUN apt install python3-dev -y
RUN pip install django==4.2.5 requests
ADD . /app
WORKDIR /app
RUN python3 manage.py makemigrations polls
RUN python3 manage.py sqlmigrate polls 0001
RUN python3 manage.py sqlmigrate polls 0002
RUN python3 manage.py migrate
#RUN python3 manage.py createsuperuser --username admin --email juan.ortiz.sanchez@correounivalle.edu.co
RUN python3 manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'juan.ortiz.sanchez@correounivalle.edu.co', 'HDLCrin8*')"

#HTTP
EXPOSE 1544
#DATABASE
EXPOSE 8070
#FOR RESOURCES API
EXPOSE 8080
#FOR COURSES API
EXPOSE 8090
#FOR AUTH API
EXPOSE 8060

ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "0.0.0.0:8070"]