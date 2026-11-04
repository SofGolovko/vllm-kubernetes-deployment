import os
from pathlib import Path
from huggingface_hub import snapshot_download

MODEL_ID = os.getenv(
    "MODEL_ID",
    "Qwen/Qwen2.5-1.5B-Instruct"
)

HF_HOME = Path(
    os.getenv("HF_HOME", "/models/huggingface")
)

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_DIR = HF_HOME / MODEL_ID.split("/")[-1]
DOWNLOAD_MARKER = MODEL_DIR / ".download_complete"

def is_model_downloaded() -> bool:
    has_config = (MODEL_DIR / "config.json").is_file()
    has_weights = (
        (MODEL_DIR / "model.safetensors").is_file()
        or any(MODEL_DIR.glob("model-*.safetensors"))
        or any(MODEL_DIR.glob("pytorch_model*.bin"))
    )
    return DOWNLOAD_MARKER.is_file() and has_config and has_weights


def download_model() -> None:
    if is_model_downloaded():
        print(f"Model already exists: {MODEL_DIR}")
        print("Skipping download.")
        return
    print(f"Downloading model: {MODEL_ID}")
    print(f"Destination: {MODEL_DIR}")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_download(
        repo_id=MODEL_ID,
        local_dir=str(MODEL_DIR),
        token=HF_TOKEN,
    )
    has_config = (MODEL_DIR / "config.json").is_file()
    has_weights = (
        (MODEL_DIR / "model.safetensors").is_file()
        or any(MODEL_DIR.glob("model-*.safetensors"))
        or any(MODEL_DIR.glob("pytorch_model*.bin"))
    )
    if not has_config or not has_weights:
        raise RuntimeError(
            "Model download is incomplete: configuration or weights are missing."
        )

    DOWNLOAD_MARKER.write_text(
        "Model downloaded successfully.",
        encoding="utf-8"
    )
    print(f"Model downloaded successfully: {MODEL_DIR}")


if __name__ == "__main__":
    download_model()
