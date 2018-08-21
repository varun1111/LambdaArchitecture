From ubuntu
RUN apt-get update
RUN apt-get install -y python

COPY UsersGenerator.py /UsersGenerator.py
COPY configFile.properties /configFile.properties
COPY users.csv /users.csv

CMD [ "python", "./UsersGenerator.py" ]
~
