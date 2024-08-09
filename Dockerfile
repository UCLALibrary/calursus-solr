FROM solr:8.11.1

# Parent image mounts a volume at /var/solr/data, which prevents us from committing data to the image.
ENV SOLR_HOME /var/local/solr_data
COPY --from=uclalibrary/solr-ursus:2024-08-09 /var/local/solr_data /var/local/solr_data
