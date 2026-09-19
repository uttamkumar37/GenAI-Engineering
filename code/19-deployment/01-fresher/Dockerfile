# multi-stage: build deps in a fat stage, ship a slim runtime image
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# expected at runtime: OPENAI_API_KEY / ANTHROPIC_API_KEY, DATABASE_URL
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
