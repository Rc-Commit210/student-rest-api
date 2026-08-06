#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$HOME/student-rest-api"
API_URL="http://localhost:5000"
TEST_EMAIL="milestone3@example.com"

echo "========================================"
echo "Milestone 3 Verification"
echo "========================================"

cd "$PROJECT_DIR"

echo
echo "1. Validating Docker Compose configuration..."
docker compose config >/dev/null
echo "Docker Compose configuration is valid."

echo
echo "2. Stopping existing services..."
make down || true

echo
echo "3. Starting complete environment..."
make up

echo
echo "4. Checking running containers..."
docker compose ps

echo
echo "5. Checking PostgreSQL readiness..."
until docker compose exec -T db pg_isready -U student -d studentdb >/dev/null 2>&1; do
    echo "Waiting for PostgreSQL..."
    sleep 2
done
echo "PostgreSQL is ready."

echo
echo "6. Verifying database tables..."
docker compose exec -T db \
    psql -U student -d studentdb -c "\dt"

echo
echo "7. Verifying Alembic migration version..."
docker compose exec -T db \
    psql -U student -d studentdb \
    -c "SELECT * FROM alembic_version;"

echo
echo "8. Testing health endpoint..."
curl --fail --silent --show-error \
    "$API_URL/healthcheck"
echo

echo
echo "9. Creating test student..."

HTTP_CODE=$(curl --silent \
    --output /tmp/student_create_response.json \
    --write-out "%{http_code}" \
    -X POST "$API_URL/api/v1/students" \
    -H "Content-Type: application/json" \
    -d "{
        \"name\": \"Milestone Test\",
        \"age\": 25,
        \"email\": \"$TEST_EMAIL\"
    }")

if [[ "$HTTP_CODE" == "201" ]]; then
    echo "Student created successfully."
elif [[ "$HTTP_CODE" == "409" ]]; then
    echo "Test student already exists. Continuing."
else
    echo "Student creation failed with HTTP status: $HTTP_CODE"
    cat /tmp/student_create_response.json
    exit 1
fi

cat /tmp/student_create_response.json
echo

echo
echo "10. Fetching all students..."
curl --fail --silent --show-error \
    "$API_URL/api/v1/students"
echo

echo
echo "11. Checking recent API logs..."
docker compose logs --tail=20 api

echo
echo "12. Checking recent database logs..."
docker compose logs --tail=20 db

echo
echo "13. Checking required project files..."

REQUIRED_FILES=(
    "Dockerfile"
    "docker-compose.yml"
    ".dockerignore"
    "Makefile"
    "README.md"
    "requirements.txt"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo "Found: $file"
    else
        echo "Missing required file: $file"
        exit 1
    fi
done

echo
echo "14. Checking Git status..."
git status --short

echo
echo "========================================"
echo "Milestone 3 verification completed."
echo "========================================"
