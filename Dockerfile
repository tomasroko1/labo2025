# Use the official Playwright image with Node.js
# This image comes with Node.js and all necessary Playwright browser dependencies pre-installed.
FROM mcr.microsoft.com/playwright:v1.50.0-noble

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
# This step ensures that npm dependencies are re-installed only if package.json or package-lock.json changes
COPY package.json package-lock.json ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose any ports if your application were a server (not strictly necessary for this script)
# EXPOSE 3000

# Command to run the application
# Use `node scripts/scan_and_sync.js` to execute the script
# This command will be the default when the container starts
CMD ["node", "scripts/scan_and_sync.js"]
