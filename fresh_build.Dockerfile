FROM solr:8.11.1

# Parent image mounts a volume at /var/solr/data, which prevents us from committing data to the image.
ENV SOLR_HOME /var/local/solr_data

ADD --chown=solr:solr calursus /var/local/solr_data/californica
ADD --chown=solr:solr calursus /var/local/solr_data/ursus
ADD --chown=solr:solr calursus /var/local/solr_data/sinai
RUN cp /var/solr/data/* /var/local/solr_data/
RUN ls /var/local/solr_data