import os
import runpod  # Required by RunPod
import requests
import uuid
import yaml
from argparse import Namespace
from scripts.inference import inference_process


def download_file(url, dest_folder):
    """
    Download a file from a URL and save it locally.
    """
    os.makedirs(dest_folder, exist_ok=True)
    local_path = os.path.join(dest_folder, f"{uuid.uuid4()}")
    with open(local_path, 'wb') as file:
        file.write(requests.get(url).content)
    return local_path


def handler(event):
    """
    Main handler function for RunPod.
    Downloads input files, prepares config, runs inference, and returns output path.
    """
    input_data = event["input"]

    # Step 1: Download input files
    image_path = download_file(input_data["image_url"], ".cache/input")
    audio_path = download_file(input_data["audio_url"], ".cache/input")

    # Step 2: Prepare configuration
    config_path = ".cache/config.yaml"
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

    # Step 3: LoRA extension (future-ready, inactive for now)
    if input_data.get("use_lora"):
        config_data["lora_path"] = "/workspace/lora/my_character_lora.safetensors"
        # You will add LoRA loading logic here in the future

    # Step 4: Save config file
    with open(config_path, "w", encoding="utf-8") as file:
        yaml.dump(config_data, file)

    # Step 5: Run inference
    args = Namespace(**config_data)
    output_path = inference_process(args)

    # Step 6: Return result
    return {"output_path": output_path}


# Required by RunPod
runpod.serverless.start({"handler": handler})
