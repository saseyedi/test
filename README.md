# To Do List App

## List of Dependencies

- Install Bottle




  Assuming that you have a fairly new installation of Python (version 2.5 or higher), you only need to install Bottle in addition to that. Bottle has no other dependencies than Python itself.

  You can either manually install Bottle or use Python’s easy_install: `easy_install bottle`

  Creation of Dockerfile

  To create a Docker image we need to create a text file named Dockerfile and use the available commands and syntax to declare how the image will be built. At the beginning of the file we need to specify the base image we are going to use and our contact informations:

FROM ubuntu:18.04
MAINTAINER Ashkan Hadadi <ashkan.hadadi@mehrparsict.com>
ENV DEBIAN_FRONTEND newt




In our case we are using Ubuntu 14.04 as base image. After these instructions we need to add PostgreSQL package repository and GnuPG public key:

RUN apt-get update && apt-get install -y gnupg2 wget

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

then we need to update the packages available in Ubuntu and install PostgreSQL:

RUN apt-get update && apt-get -y -q install python-software-properties software-properties-common   
  && apt-get -y -q install postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3
We are installing version 9.3 of PostgreSQL, instructions would be very similar for any other version of the database.

Note: it's important to have apt-get update and apt-get install commands in the same RUN line, else they would be considered two different layers by Docker and in case an updated package is available it won't be installed when the image is rebuilt.

At this point we switch to postgres user to execute the next commands:

USER postgres
RUN /etc/init.d/postgresql start   
  && psql --command "CREATE USER pguser WITH SUPERUSER PASSWORD 'pguser';"   
  && createdb -O pguser pgdb
We switch to root user and we complete the configuration:

USER root
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf
We expose the port where PostgreSQL will listen to:

EXPOSE 5432
We setup the data and shared folders that we will use later:

RUN mkdir -p /var/run/postgresql && chown -R postgres /var/run/postgresql
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
Finally we switch again to the postgres user and we define the entry command for this image:

USER postgres
CMD ["/usr/lib/postgresql/9.3/bin/postgres", "-D", "/var/lib/postgresql/9.3/main", "-c", "config_file=/etc/postgresql/9.3/main/postgresql.conf"]
The full Dockerfile is available here https://github.com/andreagrandi/postgresql-docker/blob/master/Dockerfile

Building Docker image
Once the Dockerfile is ready, we need to build the image before running it in a container. Please customize the tag name using your own docker.io hub account (or you won't be able to push it to the hub):

docker build --rm=true -t andreagrandi/postgresql:9.3 .
Running the PostgreSQL Docker container
To run the container, once the image is built, you just need to use this command:

docker run -i -t -p 5432:5432 andreagrandi/postgresql:9.3
Testing the running PostgreSQL
To test the running container we can use any client, even the commandline one:

psql -h localhost -p 5432 -U pguser -W pgdb
When you are prompted for password, type: pguser
Please note that localhost is only valid if you are running Docker on Ubuntu. If you are an OSX user, you need to discover the correct ip using: boot2docker ip
