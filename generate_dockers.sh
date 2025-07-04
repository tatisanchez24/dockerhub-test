#!/bin/bash

REPO="tatianasanchez426/test1"

for file in docs/*.yaml; do
  name=$(basename "$file" .yaml)
  cp Dockerfile.template Dockerfile
  sed -i "s|__YAML_FILE__|$file|" Dockerfile
  docker build -t "$REPO:$name" .
  docker push "$REPO:$name"
done

rm Dockerfile
