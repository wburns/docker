FROM wburns/build-base
MAINTAINER William Burns <william.a.burns@gmail.com>

RUN mkdir infinispan \
  && git clone --single-branch --progress --branch master https://github.com/infinispan/infinispan.git infinispan

WORKDIR infinispan

CMD ["/bin/bash"]
