FROM nginx:1.7.9

RUN apt-get update -y && \
    apt-get install -y apg openssl

ADD nginx /etc/nginx
ADD boot.sh .

CMD ["./boot.sh"]