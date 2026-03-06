FROM node:20-alpine AS build

WORKDIR /app

# Copy angular project package files
COPY frontend/user-app/package*.json ./

RUN npm install --legacy-peer-deps

# Copy full project
COPY frontend/user-app/ ./

# Build Angular
RUN npm run build --configuration=production


# Serve stage
FROM nginx:alpine

COPY --from=build /app/dist/user-app /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]