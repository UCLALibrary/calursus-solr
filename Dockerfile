FROM solr:8.11.1

COPY --from=uclalibrary/solr-ursus:2023-10-13 /var/solr/data /var/solr/data
