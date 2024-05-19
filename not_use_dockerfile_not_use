FROM continuumio/anaconda3
ARG PYTHON_VERSION=3.10
# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y curl && apt-get --yes install libsndfile1 && apt-get --yes install ffmpeg

RUN conda create --name whisperx

ENV PATH /opt/conda/envs/whisperx/bin:$PATH

SHELL ["conda", "run", "-n", "whisperx", "/bin/bash", "-c"]

RUN conda install python=3.10
RUN conda install pip

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
#RUN --mount=type=cache,target=/root/.cache/pip \
#    --mount=type=bind,source=requirements.txt,target=requirements.txt \
#    python -m pip install -r requirements.txt

# Copy the source code into the container.
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/m-bain/whisperx.git

# Expose the port that the application listens on.
EXPOSE 5000

# Run the application.
CMD python conversation_server.py
