FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/home/downloader \
    HF_HOME=/models/huggingface \
    HF_HUB_DISABLE_TELEMETRY=1

WORKDIR /app
RUN groupadd --gid 2000 downloader && \
    useradd --uid 2000 --gid 2000 \
        --create-home \
        --shell /usr/sbin/nologin downloader && \
    mkdir -p /models/huggingface && \
    chown -R 2000:2000 /app /home/downloader /models

COPY downloader/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --no-compile \
    -r /app/requirements.txt
COPY --chown=2000:2000 scripts/download_model.py /app/download_model.py
USER 2000:2000

ENTRYPOINT ["python", "/app/download_model.py"]