FROM nginxinc/nginx-unprivileged:alpine3.23-perl AS build

ARG NGINX_VERSION=1.29.5
ARG MODSEC_BRANCH=v3.0.14
ARG OWASP_BRANCH=v4.24.0

USER root

WORKDIR /opt

RUN echo "Installing Dependencies" && \
	apk add --no-cache --virtual general-dependencies \
	autoconf \
	automake \
	byacc \
	curl-dev \
	flex \
	g++ \
	gcc \
	geoip-dev \
	git \
	libc-dev \
	libmaxminddb-dev \
	libstdc++ \
	libtool \
	libxml2-dev \
	linux-headers \
	lmdb-dev \
	make \
	openssl-dev \
	pcre-dev \
	yajl-dev \
	zlib-dev

# Clone and compile modsecurity. Binary will be located in /usr/local/modsecurity
RUN echo "Installing ModSec Library" && \
    git clone -b ${MODSEC_BRANCH} --depth 1 https://github.com/owasp-modsecurity/ModSecurity && \
    git -C /opt/ModSecurity submodule update --init --recursive && \
    (cd "/opt/ModSecurity" && \
        ./build.sh && \
	export CXXFLAGS="-include cstdint" && \
        ./configure --with-lmdb && \
        make && \
        make install \
    ) && \
    rm -fr /opt/ModSecurity \
        /usr/local/modsecurity/lib/libmodsecurity.a \
        /usr/local/modsecurity/lib/libmodsecurity.la

RUN echo 'Cloning Modsec Nginx Connector, ModSec OWASP Rules, and download/extract nginx' && \
    git clone -b master --depth 1 https://github.com/owasp-modsecurity/ModSecurity-nginx.git && \
    git clone -b ${OWASP_BRANCH} --depth 1 https://github.com/coreruleset/coreruleset.git /usr/local/owasp-modsecurity-crs && \
    wget -O - https://nginx.org/download/nginx-$NGINX_VERSION.tar.gz | tar -xz

# Installing Modsecurity nginx Modules
RUN echo 'Installing Nginx Modules' && \
    (cd "/opt/nginx-$NGINX_VERSION" && \
        ./configure --with-compat \
            --add-dynamic-module=../ModSecurity-nginx && \
        make modules \
    ) && \
    cp /opt/nginx-$NGINX_VERSION/objs/ngx_http_modsecurity_module.so \
        /usr/lib/nginx/modules/ && \
    rm -fr /opt/* && \
    apk del general-dependencies

FROM nginxinc/nginx-unprivileged:alpine3.23-perl

USER root

# Copy nginx, owasp-modsecurity-crs and modsecurity from the build image
COPY --from=build --chown=nginx:nginx /etc/nginx/ /etc/nginx/
COPY --from=build --chown=nginx:nginx /usr/local/modsecurity /usr/local/modsecurity
COPY --from=build --chown=nginx:nginx /usr/local/owasp-modsecurity-crs /usr/local/owasp-modsecurity-crs
COPY --from=build --chown=nginx:nginx /usr/lib/nginx/modules/ /usr/lib/nginx/modules/

# Copy local config files into the image
#COPY --chown=nginx:nginx errors /usr/share/nginx/errors
COPY --chown=nginx:nginx /security/modsecurity/modsec/ /etc/nginx/modsec/
COPY --chown=nginx:nginx /security/modsecurity/owasp/ /usr/local/owasp-modsecurity-crs/
COPY --chown=nginx:nginx nginx.conf /etc/nginx/
COPY --chown=nginx:nginx security/ssl/options-ssl-nginx.conf security/ssl/ssl-dhparams.pem /etc/nginx/ssl/

RUN apk add --no-cache \
    pcre \
    curl \
    libmaxminddb \
    libstdc++ \
    libxml2 \
    lmdb \
    tzdata \
    yajl && \
    chown -R nginx:nginx /usr/share/nginx


RUN mkdir -p /tmp/nginx/log && \
	chown nginx:nginx /tmp/nginx/log && \
	chmod 755 /tmp/nginx/log

USER nginx

EXPOSE 8080 8443
