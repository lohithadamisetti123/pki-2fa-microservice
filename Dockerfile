# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

ENV TZ=UTC
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends cron tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
ENV PYTHONPATH=/app

COPY app app
COPY scripts scripts
COPY cron cron
COPY student_private.pem student_private.pem
COPY student_public.pem student_public.pem
COPY instructor_public.pem instructor_public.pem

RUN chmod +x scripts/log_2fa_cron.py
RUN chmod 0644 cron/2fa-cron && crontab cron/2fa-cron

RUN mkdir -p /data /cron && chmod 755 /data /cron

VOLUME ["/data", "/cron"]

EXPOSE 8080

CMD service cron start && \
    uvicorn app.main:app --host 0.0.0.0 --port 8080
