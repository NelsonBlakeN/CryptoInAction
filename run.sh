#!/bin/bash

# Set arguments
HOST=127.0.0.1
PORT=8080
REQUESTS=100
BUFFSIZE=100
CHANNELS=20

# Build and compile all files
make all

if [[ $? -eq 0 ]]; then
    client -n $HOST -b $BUFFSIZE -w $REQUESTS -h $HOST -p $PORT
fi
