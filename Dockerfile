FROM vllm/vllm-openai-cpu:v0.32.0.0@sha256:ffaba3989b9b96d95a576143c872a4110ce9800f5199b6a36eb27bdff1cbbe05
USER root

RUN groupadd --gid 2000 vllm \
    && useradd \
        --uid 2000 \
        --gid 2000 \
        --create-home \
        --shell /usr/sbin/nologin \
        vllm \
    && mkdir -p /models/huggingface /app/scripts /app/app \
    && chown -R 2000:2000 /models /app /home/vllm

ENV HOME=/home/vllm \
    HF_HOME=/models/huggingface \
    HF_HUB_DISABLE_TELEMETRY=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app
COPY --chown=2000:2000 scripts/download_model.py /app/scripts/download_model.py
COPY --chown=2000:2000 app/ /app/app/
USER 2000:2000