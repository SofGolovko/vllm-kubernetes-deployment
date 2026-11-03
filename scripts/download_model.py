import os
from huggingface_hub import snapshot_download

MODEL_ID = os.getenv("MODEL_ID", "Qwen/Qwen2.5-7B-Instruct")
HF_HOME = os.getenv("HF_HOME", "/root/.cache/huggingface")

snapshot_download(
    repo_id=MODEL_ID,
    local_dir=os.path.join(HF_HOME, MODEL_ID.split("/")[-1]),
    local_dir_use_symlinks=False,
    resume_download=True,
)
print(f"Model {MODEL_ID} downloaded to {HF_HOME}")