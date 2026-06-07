# Container image for deploying the Presentation Strategy Studio (Streamlit) to
# Google Cloud Run (optionally fronted by Firebase Hosting).
#
# Cloud Run provides the listening port via $PORT (default 8080). The app reads
# the API key from the ANTHROPIC_API_KEY environment variable / secret — never
# from the image (.env and venv are excluded via .dockerignore).

FROM python:3.12-slim

# System deps kept minimal; Python wheels cover lxml/reportlab on slim.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Hugging Face Spaces (Docker) expects the app on port 7860; Cloud Run sets
# its own $PORT (8080) which overrides this default. So this works on both.
ENV PORT=7860
EXPOSE 7860

# Shell form so $PORT expands at runtime.
CMD streamlit run app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --browser.gatherUsageStats=false
