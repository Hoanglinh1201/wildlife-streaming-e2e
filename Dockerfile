FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv
RUN uv pip install --system -r uv.lock
COPY . .
CMD ["uvicorn", "app.server.main:app", "--host", "0.0.0.0", "--port", "8000"]
