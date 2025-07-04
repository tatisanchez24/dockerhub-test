#!/bin/bash

REPO="tatianasanchez426/test1"
BUILD_DIR="build_context"

mkdir -p "$BUILD_DIR"

for file in docs/*.yaml; do
  name=$(basename "$file" .yaml)

  # Prepare Dockerfile
  cp Dockerfile.template "$BUILD_DIR/Dockerfile"

  # Copy YAML file
  cp "$file" "$BUILD_DIR/documentation.yaml"

  # Copy README.md if exists
  readme_path="docs_readme/${name}.md"
  if [ -f "$readme_path" ]; then
    cp "$readme_path" "$BUILD_DIR/README.md"
  else
    echo "# Documentación no disponible" > "$BUILD_DIR/README.md"
  fi

  # Build and push Docker image
  docker build -t "$REPO:$name" "$BUILD_DIR"
  docker push "$REPO:$name"

  # Clean build context
  rm -rf "$BUILD_DIR"/*
done

rmdir "$BUILD_DIR"
