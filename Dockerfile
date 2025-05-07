# -------- Stage 1: Build environment --------
    FROM python:3.12-slim AS builder

    # Set work directory
    WORKDIR /app
    
    # Install build dependencies
    RUN apt-get update && apt-get install -y build-essential
    
    # Install pip dependencies into /install
    COPY requirements.txt .
    RUN pip install --upgrade pip && \
        pip install --prefix=/install --no-cache-dir -r requirements.txt
    
    # -------- Stage 2: Runtime environment --------
    FROM python:3.12-slim
    
    # Set environment variables
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    
    # Set work directory
    WORKDIR /app
    
    # Copy installed dependencies from builder stage
    COPY --from=builder /install /usr/local
    
    # Copy application code
    COPY . .
    
    # Expose the port FastAPI will run on
    EXPOSE 8000
    
    # Run the API using Uvicorn
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    