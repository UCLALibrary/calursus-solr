FROM solr:7.4 as builder

USER root
RUN apt-get update && apt-get install -y git
RUN mkdir /home/solr && chown solr:solr /home/solr
USER solr

RUN git clone --depth 1 --branch main --single-branch https://github.com/UCLALibrary/californica.git ~/californica
RUN mkdir --parents /opt/solr/server/solr/mycores/californica/data 
RUN touch /opt/solr/server/solr/mycores/californica/core.properties 
RUN mv ~/californica/solr/config /opt/solr/server/solr/mycores/californica/conf

RUN cp -r /opt/solr/server/solr/mycores/californica /opt/solr/server/solr/mycores/ursus
RUN cp -r /opt/solr/server/solr/mycores/californica /opt/solr/server/solr/mycores/sinai


FROM solr:7.4

COPY --from=builder /opt/solr/server/solr/mycores /opt/solr/server/solr/mycores
