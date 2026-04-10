FROM solr:8.11

RUN mkdir $SOLR_HOME/lib 
RUN cp /opt/solr/dist/solr-analysis-extras-*.jar $SOLR_HOME/lib/ 
RUN cp /opt/solr/contrib/analysis-extras/**/*.jar $SOLR_HOME/lib/

ENV SOLR_MODULES=analysis-extras
ADD --chown=solr:solr ursus /var/solr/data/ursus
