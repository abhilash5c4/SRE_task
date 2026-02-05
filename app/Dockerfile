# Use slim Python as base, minimal footprint
FROM python:3.11-slim

# Create non-root user
ENV APP_USER=appuser \
    APP_HOME=/app

RUN set -eux; \
    apt-get update && apt-get install -y --no-install-recommends gcc libffi-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Create application directory
RUN mkdir -p ${APP_HOME} && groupadd -r ${APP_USER} && useradd -r -g ${APP_USER} ${APP_USER}
WORKDIR ${APP_HOME}

# Copy project files
COPY requirements.txt ./requirements.txt
# Install minimal dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY metrics_app.py ./

# Make sure files are owned by non-root user
RUN chown -R ${APP_USER}:${APP_USER} ${APP_HOME}

# Switch to non-root user
USER ${APP_USER}

# Healthcheck and listen port
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -q --spider http://127.0.0.1:8000/metrics || exit 1

# Command to run the app
CMD ["python", "metrics_app.py"]