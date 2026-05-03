FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN addgroup -S app && adduser -S app -G app
USER app
EXPOSE 8000
CMD ["python", "-m", "gunicorn", "app:app", "--bind", "0.0.0.0:8000"]