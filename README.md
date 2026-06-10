# docker-solr-ursus

Solr config for the [UCLA Digital Library](https://digital.library.ucla.edu) ([github](https://github.com/uclalibrary/ursus)) and [Sinai Manuscripts Digital Library](https://sinaimanuscripts.library.ucla.edu) ([github](https://github.com/uclalibrary/sinaimanuscripts)) websites.

Includes Dockerfile and github actions workflow to build an image for local development.

## Running tests

Tests are written in python and can be run with a docker-compose one-liner:
```
docker-compose run --renew-anon-volumes test
```

## Notes

- There might be an issue with old config persisting on anonymous docker volumes, preventing updates from taking effect even after the docker image is rebuilt. (Or there might not, I haven't confirmed this.) Docker includes a flag that sounds like it will prevent this: `docker-compose up --detach --renew-anon-volumes`, and volumes can always be destroyed with `docker-compose down -v`

