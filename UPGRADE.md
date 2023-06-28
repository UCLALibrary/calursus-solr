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
