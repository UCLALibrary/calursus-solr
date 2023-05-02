FROM solr:7.4

COPY --from=uclalibrary/solr-ursus:2021-12-14 /opt/solr/server/solr/mycores /opt/solr/server/solr/mycores
