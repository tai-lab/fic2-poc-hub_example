FROM node:latest

WORKDIR /root

RUN npm install -g bower

ENV HOME=/root

CMD ["bower", "--config.interactive=false", "install"]