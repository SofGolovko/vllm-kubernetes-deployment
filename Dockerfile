FROM vllm/vllm-openai-cpu:v0.32.0
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

# Переменные окружения
ENV HOME=/home/vllm \
    HF_HOME=/models/huggingface \
    HF_HUB_DISABLE_TELEMETRY=1 \
    PYTHONUNBUFFERED=1

# Рабочая директория
WORKDIR /app

# Копируем скрипт загрузки модели
COPY --chown=2000:2000 scripts/download_model.py /app/scripts/download_model.py

# Копируем пользовательский код
COPY --chown=2000:2000 app/ /app/app/

# Переключаемся на непривилегированного пользователя
USER 2000:2000