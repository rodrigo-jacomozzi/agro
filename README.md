# Agro

The API allows the registration/editing/listing/deletion of Producers in the database 
and also provides an endpoint with relevant statistics considering the geography and 
crops of the producers registered on the platform.

### Project Setup

#### Docker and Docker Compose
1. [Install Docker](https://docs.docker.com/engine/install/)
2. [Install Docker Compose](https://docs.docker.com/compose/install/)
 
### Setting up the environment

#### Build the API and Postgres containers 
```shell
make build
```
This will download necessary Docker images (if they are not present locally), 
build your containers and start all of the services specified 
in `docker-compose.yml`

#### Run the containers
```shell
make up
```

#### Run the Django migrations
```shell
make migrate
```

#### Restart environment
```shell
make restart
```

Observation: you will find other useful make commands inside `Makefile` such as `make stop` and `make test`.