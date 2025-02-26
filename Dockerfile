# Use official Node.js image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the project files
COPY . .

# Build the TypeScript project
RUN npm run build

# Expose the API port
EXPOSE 3301

# Run the application
CMD ["node", "dist/index.js"]
