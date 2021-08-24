#!/bin/bash -e
export image_name=preprocess_pipeline
export image_tag=latest
export full_image_name=${image_name}:${image_tag}

cd "$(dirname "$0")"
docker login
docker build -t "${full_image_name}" .
docker tag $full_image_name drobnov1994/example:$image_tag
docker push drobnov1994/example:$image_tag

