FROM postgres:latest

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=Qq12345
ENV POSTGRES_DB=bot_db
ENV POSTGRES_HOST_AUTH_METHOD="scram-sha-256\nhost replication all 0.0.0.0/0 md5"
ENV PGPASSWORD=Qq12345

COPY /sql/* /docker-entrypoint-initdb.d/
COPY entrypoint.sh /entrypoint.sh

RUN apt update -y && apt upgrade -y && apt install -y openssh-server sysstat sudo systemd
RUN echo 'root:root' | chpasswd
RUN chmod +x /entrypoint.sh

RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN usermod -aG sudo postgres

RUN mkdir -p /oracle/pg_data/archive
RUN chown -R postgres:postgres /oracle/pg_data/archive

USER postgres

EXPOSE 5432
EXPOSE 22

CMD /bin/sh /entrypoint.sh