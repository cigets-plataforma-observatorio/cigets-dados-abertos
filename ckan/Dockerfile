FROM ckan/ckan-base:2.10.1
#FROM ckan/ckan-base:2.9.9

# Set up environment variables
ENV APP_DIR=/srv/app
ENV TZ=UTC
RUN echo ${TZ} > /etc/timezone

COPY /static/images/placeholder-420x220.png $APP_DIR/src/ckan/ckan/public/base/images/placeholder-420x220.png
COPY /static/images/favicon.ico $APP_DIR/src/ckan/ckan/public/base/images/ckan.ico

# Make sure both files are not exactly the same
RUN if ! [ /usr/share/zoneinfo/${TZ} -ef /etc/localtime ]; then \
        cp /usr/share/zoneinfo/${TZ} /etc/localtime ;\
    fi ;
