# Use official Node.js 22 LTS image
FROM node:22.16

# Set working directory to backend contents inside container
WORKDIR /app

# Only copy dependency manifests first for better caching
COPY backend/package.json ./package.json
COPY backend/yarn.lock ./yarn.lock

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy backend source code
COPY backend/ ./

# If you expose a port from your app, set it here (change 3000 if different)
EXPOSE 3000

# Default start command (uses the backend's package.json "start" script).
CMD ["yarn", "start"]