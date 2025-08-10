import os
import runpod
import requests
import uuid
import yaml
from argparse import Namespace
from runpod.serverless.utils.rp_validator import validate
from scripts.inference import inference_process

# Define input schema
schema = {
    "image_url": {"type": str, "required": True},
    "audio_url": {"type": str, "required": True},
    "pose_weight": {"type": float, "required": False},
    "face_weight": {"type": float, "required": False},
    "lip_weight": {"type": float, "required": False},
    "face_expand_ratio": {"type": float, "required": False},
    "use_lora": {"type": bool, "required": False}
}

def download_file(url, dest_folder):
    os.makedirs(dest_folder, exist_ok=True)
    local_path = os.path.join(dest_folder, f"{uuid.uuid4()}")
    with open(local_path, 'wb') as file:
        file.write(requests.get(url).content)
    return local_path

def handler(event):
    validated = validate(event["input"], schema)
    if "errors" in validated:
        return {"error": validated["errors"]}

    input_data = validated["validated_input"]

    # Step 1: Download input files
    image_path = download_file(input_data["image_url"], ".cache/input")
    audio_path = download_file(input_data["audio_url"], ".cache/input")

    # Step 2: Prepare configuration
    job_id = str(uuid.uuid4())
    config_path = f".cache/configs/{job_id}.yaml"
    os.makedirs(".cache/configs", exist_ok=True)
    config_data = {
        "source_image": image_path,
        "driving_audio": audio_path,
        "save_path": ".cache",
        "output": ".cache/output.mp4",
        "pose_weight": input_data.get("pose_weight", 1.0),
        "face_weight": input_data.get("face_weight", 1.0),
        "lip_weight": input_data.get("lip_weight", 1.0),
        "face_expand_ratio": input_data.get("face_expand_ratio", 1.5),
        "audio_ckpt_dir": "pretrained_models",
        "weight_dtype": "fp32",
        "config": "configs/inference/default.yaml"
    }

    if input_data.get("use_lora"):
        config_data["lora_path"] = "/workspace/lora/my_character_lora.safetensors"

    with open(config_path, "w", encoding="utf-8") as file:
        yaml.dump(config_data, file)

    args = Namespace(**config_data)
    output_path = inference_process(args)

    return {"output": output_path}

runpod.serverless.start({"handler": handler})
