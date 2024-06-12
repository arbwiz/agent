#!/bin/bash

# Pull the latest changes from the Git repository
git pull

# Bring down any running Docker containers
docker-compose down

# Build and start the containers in detached mode
docker-compose up --build -d

# List running Docker containers
docker ps

# Get the last Docker container ID
container_id=$(docker ps -q | tail -n 1)

# Check if we got a container ID
if [ -z "$container_id" ]; then
  echo "No running Docker containers found."
  exit 1
fi

echo "Docker container ID: $container_id"

# Create a new cron job entry to restart the container every hour
cron_job="0 * * * * docker container restart $container_id"

# Remove existing cron job entries for docker container restart
crontab -r

# Add the new cron job entry
(crontab -l ; echo "$cron_job") | crontab -

echo "Cron job added: $cron_job"
