FROM nginx:latest

RUN apt update

RUN rm /etc/nginx/conf.d/default.conf
COPY ./conf.d/default.conf /etc/nginx/conf.d/

COPY ./staticfiles /usr/src/app/staticfiles
