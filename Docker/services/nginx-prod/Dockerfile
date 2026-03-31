FROM nginxinc/nginx-unprivileged:alpine3.23-perl

COPY --chown=101:101 default.conf /etc/nginx/conf.d/

COPY --chown=101:101 public/ /var/www/domain/
