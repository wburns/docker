FROM wburns/ispn-master
MAINTAINER William Burns <william.a.burns@gmail.com>

USER root

COPY settings.xml /opt/jboss/.m2/
# Unfortunately copy doesn't take into account current user
# so we have to chown over the new directory
RUN chown -R jboss:jboss /opt/jboss/.m2/

USER jboss

# use this to cache the maven artifacts for faster rebuilds
# Afterwards we delete any target directories as they just add bloat
RUN mvn clean install -DskipTests=true \
  && find . -name target -type d | xargs rm -rf

COPY . /opt/jboss/

ENTRYPOINT ["/bin/bash", "/opt/jboss/run.sh"]
