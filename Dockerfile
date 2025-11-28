FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

ENV FLASK_ENV=production

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
