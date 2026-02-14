# Use official Node.js LTS image
FROM node:20-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install Node.js dependencies
RUN npm ci

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["node", "scripts/scan_and_sync.js"]
