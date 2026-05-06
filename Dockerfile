FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "flask_app:app", "--bind", "0.0.0.0:5000", "--timeout", "120", "--workers", "1"]