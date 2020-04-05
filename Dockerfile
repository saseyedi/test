
FROM ubuntu:18.04
MAINTAIRNE Ashkan Hadadi <ashkan.hadadi@mehrparsict.com>
ENV DEBIAN_FRONTEND newt

RUN apt-get update && apt-get install -y gnupg2 wget

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get update && apt-get -y -q install software-properties-common && apt-get -y -q install postgresql-9.4 postgresql-client-9.4 postgresql-contrib-9.4

USER postgres
RUN /etc/init.d/postgresql start && psql --command "CREATE USER ashkanhadadi WITH SUPERUSER PASSWORD '123456';" && createdb -O ashkanhadadi todo

USER root
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.4/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.4/main/postgresql.conf

EXPOSE 5432

RUN mkdir -p /var/run/postgresql && chown -R postgres /var/run/postgresql
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

USER postgres
CMD ["/usr/lib/postgresql/9.4/bin/postgres", "-D", "/var/lib/postgresql/9.4/main", "-c", "config_file=/etc/postgresql/9.4/main/postgresql.conf"]

