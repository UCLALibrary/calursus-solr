# docker-solr-ursus

Solr index for uclalibrary/ursus local development and testing, populated by cloning ursus-stage and sinaimanuscripts-stage.

## Installing python scripts

### Prerequisites

- Python >= 3.11
- [poetry](http://python-poetry.org)
- [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/)
- Direct API access to the Ursus and Sinai solr cores - for example by running on a UCLA Library server or by setting up ssh port forwarding via the jump server.

### Install Python dependencies

```
poetry install
```

## SSH Tunnel to Solr Server

DevSupport can help you get set up on the jump server, then in `~/.ssh/config`:

```
Host jump
HostName [JUMP HOSTNAME].ucla.edu
User [JUMP USERNAME]
Port [JUMP PORT]
```

Then run in terminal:

```
ssh -L [LOCAL SOLR PORT]:[SOLR HOSTNAME].ucla.edu:80 [JUMP USERNAME]@[JUMP HOSTNAME].ucla.edu -p [JUMP PORT]
```

Then access the solr web console at `http://localhost:[LOCAL SOLR PORT]/solr/#` and the api at `http://localhost:[LOCAL SOLR_PORT]/solr/[CORE]

## Create a test image for Ursus and Sinai

### Build and start the container

```
docker-compose build
docker-compose up --detach
```

### Copy sample data the solr cores

```
poetry run python3 clone_ursus_index.py http://[URSUS_SOLR_URL]/solr/calursus http://localhost:7983/solr/ursus
poetry run python3 clone_ursus_index.py http://[SINAI_SOLR_URL]/solr/sinaimanu http://localhost:7983/solr/sinai
```

TODO: Move this function to a subcommand of solr_tools.py

### Commit and push to dockerhub
```
docker commit calursus-solr-solr-1 uclalibrary/solr-ursus:[YYYY-MM-DD]
docker push uclalibrary/solr-ursus:[YYYY-MM-DD]
```

### Use in Ursus

Update `docker-compose-standalone.yml` and `docker-compose-ci.yml` to point to the new tag.

## Copy all data from one solr core to another

```
poetry run ./solr_tools.py clone http://[SOURCE HOSTNAME]:[SOURCE PORT]/solr/[SOURCE CORE] http://[DEST HOSTNAME]:[DEST PORT]/solr/[DEST CORE]
```

For example,

```
poetry run ./solr_tools.py clone http://localhost:8898/solr/calursus http://localhost:7983/solr/calursus-prod
```