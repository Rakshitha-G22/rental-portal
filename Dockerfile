# Stage 1: Build Angular frontend
FROM node:22-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/user-app/package*.json ./
RUN npm install
COPY frontend/user-app/ ./
RUN npm run build --configuration production

# Stage 2: Build Python backend
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy backend
COPY backend/ ./backend
COPY backend/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend build into backend static folder
COPY --from=frontend-builder /app/frontend/dist/user-app backend/frontend_dist

# Set environment variables (Railway will override with its own)
ENV PORT=8080
ENV DATABASE_URL=<your_database_url>
ENV JWT_SECRET_KEY=<your_jwt_secret>

# Expose port
EXPOSE 8080

# Start command
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:$PORT", "backend.wsgi:application"]