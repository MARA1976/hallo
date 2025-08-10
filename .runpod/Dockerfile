# Base image with CUDA and Python
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    libgl1 \
    fontconfig \
    libxrender1 \
    libpulse0 \
    libgbm1 \
    libdrm-radeon1 \
    libdrm-nouveau2 \
    libpango-1.0-0 \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN curl -o ~/miniconda.sh -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh
ENV PATH=/opt/conda/bin:$PATH

# Accept Conda Terms of Service and create environment
RUN conda config --set channel_priority strict && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r && \
    conda create -n hallo python=3.10 -y

# Activate Conda environment for subsequent commands
SHELL ["conda", "run", "-n", "hallo", "/bin/bash", "-c"]

# Copy project files
COPY . /workspace

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install .

# Optional: download pretrained models
# RUN git lfs install && \
#     git clone https://huggingface.co/fudan-generative-ai/hallo pretrained_models

# Optional: copy LoRA weights
# COPY lora/my_character_lora.safetensors /workspace/lora/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/workspace/.cache/huggingface

# RunPod entry point
CMD ["conda", "run", "--no-capture-output", "-n", "hallo", "python", "handler.py"]
