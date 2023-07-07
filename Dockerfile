FROM solr:7.4

COPY --from=uclalibrary/solr-ursus:2021-12-14 /opt/solr/server/solr/mycores /opt/solr/server/solr/mycores

COPY --from=uclalibrary/solr-ursus:2021-12-14 /opt/solr/server/solr/mycores/californica /opt/solr/server/solr/mycores/calursus-dev
COPY --from=uclalibrary/solr-ursus:2021-12-14 /opt/solr/server/solr/mycores/californica /opt/solr/server/solr/mycores/calursus-test
COPY --from=uclalibrary/solr-ursus:2021-12-14 /opt/solr/server/solr/mycores/californica /opt/solr/server/solr/mycores/calursus-stage
COPY --from=uclalibrary/solr-ursus:2021-12-14 /opt/solr/server/solr/mycores/californica /opt/solr/server/solr/mycores/calursus-prod
