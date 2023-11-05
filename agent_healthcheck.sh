#!/bin/bash

# Define the file path
file_path="output/last_time_written"

# Check if the file exists
if [ -f "$file_path" ]; then
    # Get the current time in seconds since epoch
    current_time=$(date +%s)

    # Read the content of the file (epoch timestamp)
    file_timestamp=$(cat "$file_path")

    # Calculate the age of the file in seconds
    age=$((current_time - file_timestamp))

    # Check if the age is greater than 5 minutes (300 seconds)
    if [ "$age" -gt 300 ]; then
        echo "File is older than 5 minutes"
        exit 1
    else
        echo 'File is not older than 5 minutes'
        exit 0
    fi
else
    echo "File not found"
    exit 2
fi