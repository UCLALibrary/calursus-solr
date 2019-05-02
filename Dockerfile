FROM solr:6.5

ADD --chown=solr:solr calursus /opt/solr/server/solr/mycores/
