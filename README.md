# vLLM Kubernetes Deployment
Проект предназначен для локального запуска языковой модели с использованием CPU и постоянного хранилища для файлов модели.

## Технологический стек

Kubernetes: Minikube.
Контейнеризация: Docker.
Inference engine: vLLM 0.32.0.
Режим вычислений: CPU-only.
Языковая модель: Qwen/Qwen2.5-1.5B-Instruct.
Python: 3.12.15.

## Docker-образ

Для создания собственного образа используется официальный CPU-образ vLLM версии 0.32.0, закреплённый по digest.

## Сборка образа:

docker build -t vllm-custom:0.32.0 .


## Проверка зависимостей:

docker run --rm --entrypoint python vllm-custom:0.32.0 -m pip check

Для загрузки весов модели используется отдельный rootless Docker-образ, собираемый из downloader/Dockerfile:

docker build -f downloader/Dockerfile -t model-downloader:0.1.0 .


Перед запуском необходимо указать значения VLLM_API_KEY и HF_TOKEN в файле k8s/secret.yaml.

VLLM_API_KEY можно сгенерировать с помощью:

python -c "import secrets; print(secrets.token_urlsafe(32))"

## Запуск и проверка

Запуск Minikube:

minikube start --driver=docker

Загрузка собранных Docker-образов в Minikube:

minikube image load vllm-custom:0.32.0
minikube image load model-downloader:0.1.0

Применение манифестов Kubernetes:

kubectl apply -k k8s/

Проверка состояния приложений:

kubectl get pods -n vllm
kubectl get services -n vllm
kubectl get pvc -n vllm

Просмотр логов:

init-контейнера:

kubectl logs -n vllm deployment/vllm-inference -c download-model

основного контейнера:

kubectl logs -n vllm deployment/vllm-inference -c vllm


Для обращения к API используется проброс порта:

kubectl port-forward -n vllm svc/vllm-service 8000:80

После этого API модели доступен по адресу:

http://localhost:8000

Для отправки запроса к модели используется следующий код:

$headers = @{
    Authorization = "Bearer API_КЛЮЧ"
    
}

$body = @{    
    model = "/models/huggingface/Qwen2.5-1.5B-Instruct"
    messages = @(
         @{
             role = "user"
             content = "What is machine learning? Answer in one simple sentence."
         }
     )
     max_tokens = 100
     temperature = 0.2
 } | ConvertTo-Json -Depth 5
 
 $result = Invoke-RestMethod `
     -Uri "http://localhost:8000/v1/chat/completions" `
     -Method Post `
     -Headers $headers `
     -ContentType "application/json" `
     -Body $body
 
 $result.choices[0].message.content
Для доступа к API необходимо передавать Bearer-токен, заданный в Secret.