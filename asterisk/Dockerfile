FROM debian:stable-slim

RUN apt-get update && \
    apt-get install -y asterisk

COPY conf/ /etc/asterisk/

CMD ["asterisk", "-f"]
