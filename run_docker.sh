#!/bin/bash
echo "Starting Highwind docker image"
mkdir -p highwind_jsons
mkdir -p build
docker run -d -p 8501:8501 -v $PWD/highwind_jsons:/home/highwind_jsons -v $PWD/build:/home/build highwind
echo "Website live at localhost:8501"