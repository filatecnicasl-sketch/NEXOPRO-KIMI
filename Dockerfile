FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema para WeasyPrint
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b libgdk-pixbuf2.0-0 \
    libcairo2 libffi-dev shared-mime-info && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "core.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
