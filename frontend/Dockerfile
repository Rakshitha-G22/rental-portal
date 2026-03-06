# Node build stage
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy project files
COPY . .

# Build Angular production build
RUN npm run build --configuration=production


# Serve stage
FROM nginx:alpine

# Copy build output (Change dist/user-app if needed ⚠)
COPY --from=build /app/dist/user-app /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]