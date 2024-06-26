#!/bin/bash

# Stop the containers if they are running
docker stop some-postgres
docker stop iroha

# Remove all unused data
docker system prune -f

# Create a new Docker network
docker network create iroha-network

# Run the PostgreSQL container
docker run --name some-postgres \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=mysecretpassword \
    -p 5432:5432 \
    --network=iroha-network \
    -d postgres:9.5 \
    -c 'max_prepared_transactions=100'

# Remove the old volume and create a new one
docker volume rm blockstore
docker volume create blockstore


# Run the Iroha container
cd /Git
docker run --name iroha \
    --rm \
    -d \
    -p 50051:50051 \
    -p 7001:7001 \
    -v $(pwd)/iroha/example:/opt/iroha_data \
    -v blockstore:/tmp/block_store \
    --network=iroha-network \
    -e KEY='node0' \
    hyperledger/iroha-burrow:1.5.0-debug
