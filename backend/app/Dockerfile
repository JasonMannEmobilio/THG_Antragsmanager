FROM python:3.11-slim
WORKDIR /app
# We'll copy requirements from the parent dir if building from backend root,
# or we assume they are present in the context.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
