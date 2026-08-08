# syntax=docker/dockerfile:1

ARG NODE_VERSION=24.11-bookworm-slim

# ----------------------------
# Dev image: full toolchain (all devDependencies) for local development via
# docker compose and for CI quality checks (lint, test, build).
# ----------------------------
FROM node:${NODE_VERSION} AS dev

WORKDIR /usr/src/app

# Download dependencies as a separate step to take advantage of Docker's caching.
COPY package.json package-lock.json ./
RUN npm i --include=dev

# Copy the rest of the source files into the image.
COPY . .

EXPOSE 3000

CMD ["npx", "vite", "--host", "--port", "3000"]

# ----------------------------
# Build stage: compiles the production static assets. Not shipped itself —
# only its /dist output is copied into the runtime image below.
# ----------------------------
FROM node:${NODE_VERSION} AS build

WORKDIR /usr/src/app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# ----------------------------
# Runtime image: what you'd deploy — static assets served by nginx. No
# Node.js runtime and no devDependencies, so it's what Trivy should scan.
# ----------------------------
FROM nginx:1.31-alpine AS runtime

# Apply latest Alpine security patches to the base image layer.
RUN apk upgrade --no-cache

COPY --from=build /usr/src/app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
