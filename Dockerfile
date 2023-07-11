FROM solr:8.11.1

COPY --from=uclalibrary/solr-ursus:2023-07-11 /opt/solr/server/solr/mycores /opt/solr/server/solr/mycores
