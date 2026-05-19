FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --upgrade pip
COPY . .
RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["uvicorn", "artref.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
