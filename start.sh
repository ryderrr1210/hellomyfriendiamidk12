#!/bin/bash
# AzrielGPT Cloud Bootloader
# This script is used by Docker to run both your backends together

# Spin up the Python brain in the background
python api_server.py &

# Wait 2 seconds for Python to bind
sleep 2

# Launch the Node proxy/frontend, listening on the cloud's dynamic port
node server.js --port ${PORT:-3000}
