# Use Jupyter base notebook with Python 3.11
FROM jupyter/base-notebook:latest

# Set working directory
WORKDIR /home/jovyan

# Install mamba for faster package management
USER root
RUN conda install -n base -c conda-forge mamba -y && \
    conda clean --all -y
USER jovyan

# Copy the environment specification
COPY geoprivacy.yml /tmp/geoprivacy.yml

# Install environment
USER root
RUN mamba env update -n base -f /tmp/geoprivacy.yml && \
    mamba install -n base -c conda-forge osmnx && \
    conda clean --all -y
USER jovyan

# Register the base env as a kernel
RUN python -m ipykernel install --user --name=base --display-name="Python (base)"

# Copy everything else in
COPY . .

# Make resources and outputs writable
USER root
RUN mkdir -p /home/jovyan/geoprivacy /home/jovyan/resources && \
    chown -R jovyan:users /home/jovyan/geoprivacy /home/jovyan/resources && \
    chmod -R 755 /home/jovyan/geoprivacy /home/jovyan/resources
USER jovyan

# Expose port and launch notebook
EXPOSE 8888
CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''"]
