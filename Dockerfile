FROM solr:8.11.1

ADD --chown=solr:solr calursus /var/solr/data/californica
ADD --chown=solr:solr calursus /var/solr/data/ursus
ADD --chown=solr:solr calursus /var/solr/data/sinai
