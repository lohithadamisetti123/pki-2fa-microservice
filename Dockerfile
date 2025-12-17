# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc libffi-dev libssl-dev python3-dev && rm -rf /var/lib/apt/lists/* && \
    pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

ENV TZ=UTC

WORKDIR /app

RUN apt-get update && apt-get install -y cron tzdata && apt-get clean && rm -rf /var/lib/apt/lists/* && \
    ln -fs /usr/share/zoneinfo/UTC /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY app.py .
COPY scripts/ scripts/
COPY cron/ cron/
COPY student_private.pem .
COPY student_public.pem .
COPY instructor_public.pem .

RUN chmod 0644 cron/2fa-cron && crontab cron/2fa-cron

RUN mkdir -p /data /cron && chmod 755 /data /cron

EXPOSE 8080

CMD ["sh", "-c", "cron && uvicorn app:app --host 0.0.0.0 --port 8080"]
