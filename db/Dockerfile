FROM postgres:latest

ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG RM_USER
ARG RM_PASSWORD

ENV POSTGRES_USER=$DB_USER
ENV POSTGRES_PASSWORD=$DB_PASSWORD
ENV POSTGRES_DB=$DB_HOST
ENV PGPASSWORD=$DB_PASSWORD
ENV POSTGRES_HOST_AUTH_METHOD="scram-sha-256\nhost replication all 0.0.0.0/0 md5"

COPY /sql/* /docker-entrypoint-initdb.d/
COPY entrypoint.sh /entrypoint.sh

RUN apt update -y && apt upgrade -y && apt install -y openssh-server sysstat sudo systemd iproute2
RUN useradd -m $RM_USER || echo "User $RM_USER already exists, skipping..."
RUN echo "$RM_USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN echo "$DB_USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN echo "$RM_USER:$RM_PASSWORD" | chpasswd
RUN chmod +x /entrypoint.sh
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN usermod -aG sudo $RM_USER
RUN usermod -aG sudo $DB_USER

RUN mkdir -p /oracle/pg_data/archive
RUN chown -R $DB_USER:postgres /oracle/pg_data/archive

USER $DB_USER

EXPOSE 5432
EXPOSE 22

CMD /bin/sh /entrypoint.sh