FROM solr

ADD --chown=solr:solr calursus.tar.gz /opt/solr/server/solr/mycores/
