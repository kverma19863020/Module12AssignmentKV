# Module 12 Assignment — KV

User & Calculation Routes with Integration Testing — FastAPI + PostgreSQL

## Docker Hub
docker pull kverma1986/module12assignmentkv:latest

## Run Locally with Docker

git clone https://github.com/kverma19863020/Module12AssignmentKV.git
cd Module12AssignmentKV
docker compose up --build
open http://localhost:8000/docs

## Run Integration Tests Locally

# Start only Postgres
docker compose up db -d

# Create test database
docker exec -it module12assignmentkv-db-1 \
  psql -U postgres -c "CREATE DATABASE module12test;"

# Install dependencies
pip install -r requirements.txt

# Run all tests
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/module12test \
  pytest tests/ -v

## Endpoints

### Users
POST   /users/register   Register new user
POST   /users/login      Login with password

### Calculations (BREAD)
GET    /calculations/         Browse all
GET    /calculations/{id}     Read one
POST   /calculations/         Add new
PUT    /calculations/{id}     Edit existing
DELETE /calculations/{id}     Delete

## Supported Operations
add · subtract · multiply · divide

## Links
GitHub:     https://github.com/kverma19863020/Module12AssignmentKV
Docker Hub: https://hub.docker.com/r/kverma1986/module12assignmentkv
