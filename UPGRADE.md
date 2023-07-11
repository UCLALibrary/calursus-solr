# Solr 7 to 8 upgrade

Ad-hoc instructions for upgrading solr 7 to solr 8 on existing solr 7 systems

## unpack solr

probably already done

## install solr

- `systemctl stop solr.service`
- `ps -A | grep java`
- `mv /var/solr /var/solr7`
- `/opt/solr-8.11.1/bin/install_solr_service.sh /opt/solr-8.11.1.tgz -n -f`
- `systemctl start solr.service`
- `su -c '/opt/solr/bin/solr create -c CORE_NAME' solr`
- `systemctl stop solr.service`

## copy in the configs

- calursus
  - local workstation
    - `git clone git@github.com:UCLALibrary/calursus-solr.git`
    - `cd calursus-solr`
    - `git switch solr8`
    - `rsync -Pia calursus s-u-calursussolrmaster01.library.ucla.edu:/tmp`
  - solr server
    - `rsync -Pia /tmp/calursus/. /var/solr/data/calursus/.`
    - `chown -R solr:solr /var/solr/data/calursus`
- sinaimanu
  - local workstation
    - `git clone git@github.com:UCLALibrary/calursus-solr.git`
    - `cd calursus-solr`
    - `git switch solr8`
    - `rsync -Pia calursus s-u-calursussolrmaster01.library.ucla.edu:/tmp`
  - solr server
    - `rsync -Pia /tmp/sinaimanu/. /var/solr/data/sinaimanu/.`
    - `chown -R solr:solr /var/solr/data/sinaimanu`
- `systemctl start solr.service`

## Migrate Ursus

- edit `.env.production` to point to calursus core
  - `SOLR_URL=http://s-u-californicasolr01.library.ucla.edu/solr/calursus`
- restart rails
  - `systemctl restart httpd.service`
- install Solr (see above)
- copy in the configs (see above, use the correct hostname)
  - `s-u-calursussolrslave01`
- sync the core
  - `/usr/local/sbin/solr-rsync-replication`
- un-edit `.env.production`
- re-restart rails
  - `systemctl restart httpd.service`

## Ensure proper ownerships of all solr config files

- `chown -R solr:solr /var/solr/*`

## Solr Upgrade Status

### Solr 7 sites without Solr 8 installed:

- p-u-californicasolr-ingest01.library.ucla.edu
- p-u-ohsolr01.library.ucla.edu
- s-u-ohsolr01.library.ucla.edu
- t-u-ohsolr01.library.ucla.edu
- p-u-calursussolrslave-ingest01.library.ucla.edu
- p-w-avalonsolr01.library.ucla.edu
- p-u-calursussolrmaster-ingest01.library.ucla.edu

### Solr 8.11.1 Installed

d-u-californicasolr01.library.ucla.edu
d-u-calursussolr01.library.ucla.edu
p-u-sheetmusicsolr01.library.ucla.edu
p-u-shorelinesolr01.library.ucla.edu
p-u-sinaipalimpsolr01.library.ucla.edu
s-u-californicasolr01.library.ucla.edu
s-u-calursussolrmaster01.library.ucla.edu
s-u-calursussolrslave01.library.ucla.edu
t-u-calursussolrmaster01.library.ucla.edu
t-u-calursussolrslave01.library.ucla.edu

### Solr 8.11.2 Insstalled

d-u-sinaimanuscriptssolr01.library.ucla.edu
d-w-avalonsolr01.library.ucla.edu
t-u-sinaimanuscriptssolr01.library.ucla.edu
