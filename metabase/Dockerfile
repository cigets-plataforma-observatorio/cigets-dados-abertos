FROM metabase/metabase:v0.47.0

# Set up environment variables
ENV APP_DIR=/
ENV TZ=UTC
RUN echo ${TZ} > /etc/timezone

COPY /plugins/dremio.metabase-driver.jar $APP_DIR/plugins/dremio.metabase-driver.jar

# Make sure both files are not exactly the same
RUN if ! [ /usr/share/zoneinfo/${TZ} -ef /etc/localtime ]; then \
        cp /usr/share/zoneinfo/${TZ} /etc/localtime ;\
    fi ;
