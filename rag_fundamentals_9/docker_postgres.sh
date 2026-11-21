sudo docker run -d \
  --name pgvector-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=vector_lab \
  -p 5434:5432 \
  pgvector/pgvector:pg16