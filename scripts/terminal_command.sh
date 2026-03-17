#!/usr/bin/env bash

# Prerequisite: `jq` is used below for pretty-printing JSON responses.

# Docker-first local stack
docker compose up -d --build --wait

# Health
curl http://localhost:8000/health | jq


# -----------------------------
# Folder endpoints
# -----------------------------

# Create a folder
curl -X POST http://localhost:8000/folders \
	-H "Content-Type: application/json" \
	-d '{ "title": "first_folder" }' | jq

# List folders
curl http://localhost:8000/folders | jq

# Get folder by id
curl http://localhost:8000/folders/1 | jq

# Update folder title
curl -X PUT http://localhost:8000/folders/1 \
	-H "Content-Type: application/json" \
	-d '{ "title": "updated_folder" }' | jq

# Delete folder (soft delete)
curl -i -X DELETE http://localhost:8000/folders/1


# -----------------------------
# Item endpoints
# -----------------------------

# Add item to folder
curl -X POST http://localhost:8000/folders/1/items \
	-H "Content-Type: application/json" \
	-d '{ "title": "first_item" }' | jq

# List items in folder
curl http://localhost:8000/folders/1/items | jq

# Get specific item
curl http://localhost:8000/folders/1/items/1 | jq

# Update item title
curl -X PUT http://localhost:8000/folders/1/items/1 \
	-H "Content-Type: application/json" \
	-d '{ "title": "updated_item" }' | jq

# Toggle item completion
curl -X PUT http://localhost:8000/folders/1/items/1/toggle | jq

# Reorder items in folder
curl -X PUT http://localhost:8000/folders/1/item_order \
	-H "Content-Type: application/json" \
	-d '{ "itemOrder_id": [3,1,2] }' | jq

# Delete item (soft delete)
curl -i -X DELETE http://localhost:8000/folders/1/items/1


# Stop stack
docker compose down
