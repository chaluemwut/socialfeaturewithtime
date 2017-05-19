FROM chaluemwut/nginx
MAINTAINER Feng Honglin <hfeng@tutum.co>

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-available/default
ADD default /etc/nginx/sites-available/

EXPOSE 80

CMD ["/usr/sbin/nginx"]