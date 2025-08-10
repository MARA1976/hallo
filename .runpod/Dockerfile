# Utilisation de l'image CUDA de NVIDIA correspondant à votre version
FROM nvidia/cuda:12.2.2-cudnn8-devel-ubuntu22.04

# Mettre à jour les listes de paquets et installer wget et d'autres outils essentiels
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    build-essential \
    cmake \
    libgl1-mesa-glx \
    libgtk2.0-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    zlib1g-dev \
    libxkbcommon-x11-dev \
    libglib2.0-0 \
    # Nettoyer les fichiers temporaires pour réduire la taille de l'image
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer Miniconda
ENV MINICONDA_VERSION=py310_23.1.0-1
ENV MINICONDA_INSTALLER_SCRIPT=Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh
ENV MINICONDA_PREFIX=/opt/conda

RUN wget https://repo.anaconda.com/miniconda/${MINICONDA_INSTALLER_SCRIPT} \
    && chmod +x ${MINICONDA_INSTALLER_SCRIPT} \
    && ./${MINICONDA_INSTALLER_SCRIPT} -b -p ${MINICONDA_PREFIX} \
    && rm ${MINICONDA_INSTALLER_SCRIPT}

ENV PATH=$MINICONDA_PREFIX/bin:$PATH

# Initialiser Conda pour que `conda activate` fonctionne dans le shell
RUN conda init bash

# IMPORTANT : Reconstruire le shell après conda init pour que les changements prennent effet
SHELL ["/bin/bash", "--login", "-c"]

# Mettre à jour conda et installer des dépendances de base
RUN conda update -n base -c defaults conda \
    && conda install -y python=3.10 \
    && conda clean --all -f -y

# Créer un environnement Conda pour votre projet et installer les bibliothèques
ENV CONDA_ENV_NAME=multimedia_env

# Créer l'environnement
RUN conda create -n ${CONDA_ENV_NAME} python=3.10 pip -y


# Créer un environnement Conda pour votre projet et installer les bibliothèques
ENV CONDA_ENV_NAME=multimedia_env

# Créer l'environnement
RUN conda create -n ${CONDA_ENV_NAME} python=3.10 pip -y

# Installer les bibliothèques via pip dans l'environnement spécifique
#RUN conda run -n ${CONDA_ENV_NAME} pip install --upgrade pip && \
 #   conda run -n ${CONDA_ENV_NAME} pip install \
 #       numpy \
  #      pandas \
   #     scipy \
   #     matplotlib \
    #    jupyterlab \
     #   notebook \
      #  opencv-python-headless \
       # scikit-image \
        #Pillow \
        #librosa \
        #soundfile \
        #moviepy \
        #imageio \
        #imageio-ffmpeg \
        #tqdm \
        #ffmpeg-python \
        #pydub

# --- DÉBUT DES MODIFICATIONS : Utilisation de requirements.txt ---
# Copier le fichier requirements.txt
COPY requirements.txt .

RUN conda run -n ${CONDA_ENV_NAME} pip install --no-cache-dir -r requirements.txt
#FIN
# Tenter d'installer dlib via Conda-forge (plus fiable pour dlib)
RUN conda run -n ${CONDA_ENV_NAME} conda install -c conda-forge dlib -y \
    && conda clean --all -f -y

# Retourner au comportement de shell par défaut pour les RUN suivants si nécessaire
SHELL ["/bin/sh", "-c"]

# Exposer le port pour JupyterLab si vous l'utilisez
EXPOSE 8888

# Launch the main script with the activated Conda environment
CMD ["/bin/bash", "-c", "source /opt/conda/etc/profile.d/conda.sh && conda activate multimedia_env && python handler.py"]



























