FROM nvcr.io/nvidia/pytorch:23.10-py3

WORKDIR /usr/src/app
RUN python -m pip install --upgrade pip
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get  install libsndfile1 -y

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN apt-get --yes install ffmpeg

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/m-bain/whisperx.git

COPY . .

EXPOSE 5000

# Run the application.
CMD python conversation_server.py