FROM solr:7.4

ADD --chown=solr:solr calursus /opt/solr/server/solr/mycores/calursus
