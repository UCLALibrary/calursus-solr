# docker-solr-ursus

Solr index for uclalibrary/ursus local development and testing, populated by cloning ursus-stage and sinaimanuscripts-stage.

## How to build

### Prerequisites

- Python >= 3.11
- [poetry](http://python-poetry.org)
- [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/)
- Direct API access to the Ursus and Sinai solr cores - for example by running on a UCLA Library server or by setting up ssh port forwarding via the jump server.

### Install Python dependencies

```
poetry install
```

### Build and start the container

```
docker-compose build
docker-compose up --detach
```

### Clone the solr cores

```
poetry run python3 clone_ursus_index.py http://[URSUS_SOLR_URL]/solr/calursus http://localhost:7983/solr/ursus
poetry run python3 clone_ursus_index.py http://[SINAI_SOLR_URL]/solr/sinaimanu http://localhost:7983/solr/sinai
```

### Commit and push to dockerhub
```
docker commit docker-solr-ursus_solr_1 uclalibrary/solr-ursus:[YYYY-MM-DD]
docker push uclalibrary/solr-ursus:[YYYY-MM-DD]
```

### Use in Ursus

Update `docker-compose-standalone.yml` and `docker-compose-ci.yml` to point to the new tag.
