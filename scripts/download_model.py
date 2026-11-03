import os
from huggingface_hub import snapshot_download

MODEL_ID = os.getenv(
    "MODEL_ID",
    "Qwen/Qwen2.5-1.5B-Instruct"
)

HF_HOME = os.getenv(
    "HF_HOME",
    "/models/huggingface"
)

HF_TOKEN = os.getenv("HF_TOKEN")

print(f"Downloading model: {MODEL_ID}")

snapshot_path = snapshot_download(
    repo_id=MODEL_ID,
    cache_dir=os.path.join(HF_HOME, "hub"),
    token=HF_TOKEN,
)

print(f"Model downloaded to: {snapshot_path}")