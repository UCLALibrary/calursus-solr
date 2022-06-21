FROM solr:8.11.1

ADD --chown=solr:solr calursus-solr8 /var/solr/data/californica
ADD --chown=solr:solr calursus-solr8 /var/solr/data/ursus
ADD --chown=solr:solr calursus-solr8 /var/solr/data/sinai
