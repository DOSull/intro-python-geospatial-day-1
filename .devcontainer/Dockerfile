FROM mcr.microsoft.com/devcontainers/anaconda

RUN conda install -n base -c conda-forge mamba

# COPY environment.yml* /tmp/conda-tmp/

# RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then umask 0002 && /opt/conda/bin/mamba env create -f /tmp/conda-tmp/environment.yml; fi && rm -rf /tmp/conda-tmp

RUN umask 0002 && /opt/conda/bin/mamba env create -n intro-python-1 -c conda-forge python=3.11 jupyter ipykernel ipywidgets ipycanvas cachetools colorama geopandas 
