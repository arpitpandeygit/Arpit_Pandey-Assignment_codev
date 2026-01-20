# ---------- Base Image ----------
FROM python:3.11-slim

# ---------- Security: non-root user ----------
RUN useradd -m appuser
WORKDIR /app

# ---------- Install dependencies ----------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Copy application ----------
COPY app ./app

# ---------- Change ownership ----------
RUN chown -R appuser:appuser /app
USER appuser

# ---------- Expose port ----------
EXPOSE 8000

# ---------- Healthcheck ----------
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# ---------- Run ----------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

