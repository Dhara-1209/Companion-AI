# Deployment & DevOps Guide

## Docker Containerization

### Frontend Dockerfile
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --legacy-peer-deps
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

### Backend Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "src/backend/main.py"]
```

## Docker Compose

```yaml
version: '3.8'
services:
  frontend:
    build: ./docker
    container_name: homebuddy-frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend
  
  backend:
    build: ./docker
    container_name: homebuddy-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/homebuddy
    depends_on:
      - db
  
  db:
    image: postgres:15
    container_name: homebuddy-db
    environment:
      - POSTGRES_USER=homebuddy
      - POSTGRES_PASSWORD=secure_password
      - POSTGRES_DB=homebuddy
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

## Deployment Steps

### Local Deployment
```bash
docker-compose up -d
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Production Deployment

1. **AWS Deployment**
   - Frontend: CloudFront + S3
   - Backend: ECS + RDS
   - Database: RDS PostgreSQL

2. **Azure Deployment**
   - Frontend: Azure Static Web Apps
   - Backend: Azure App Service
   - Database: Azure Database for PostgreSQL

3. **GCP Deployment**
   - Frontend: Cloud Storage + CDN
   - Backend: Cloud Run
   - Database: Cloud SQL

## CI/CD Pipeline

### GitHub Actions Workflow
```yaml
name: Deploy
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: npm test
  
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: npm run build
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: ./deploy.sh
```

## Monitoring & Logging

✅ Application logs
✅ Performance metrics
✅ Error tracking
✅ User analytics
✅ Health checks

---

**QA Lead: Dhara-1209**
