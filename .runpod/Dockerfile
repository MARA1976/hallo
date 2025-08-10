# Utilise une image officielle avec support CUDA
FROM nvidia/cuda:12.2.0-base-ubuntu22.04

# Installe Python et les dépendances système
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Crée un dossier de travail
WORKDIR /app

# Copie les fichiers du projet
COPY . /app

# Installe les dépendances Python
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install .

# Définit le point d’entrée pour RunPod Serverless
CMD ["python3", "handler.py"]
