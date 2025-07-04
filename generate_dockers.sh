#!/bin/bash

mkdir -p build_context

for file in docs/*.yaml; do
  name=$(basename "$file" .yaml)
  cp Dockerfile.template build_context/Dockerfile
  cp "$file" build_context/documentation.yaml

  readme_path="docs_readme/${name}.md"
  if [ -f "$readme_path" ]; then
    cp "$readme_path" build_context/README.md
  else
    echo "# Documentación no disponible" > build_context/README.md
  fi

  docker build -t "tatianasanchez426/test1:$name" build_context
  docker push "tatianasanchez426/test1:$name"
  rm -rf build_context/*
done

rmdir build_context
