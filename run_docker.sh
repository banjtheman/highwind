#!/bin/bash
echo "Starting Highwind docker image"
docker run -d -p 8501:8501 -v highwind_jsons:/home/highwind_jsons highwind