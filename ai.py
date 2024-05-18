# -*- coding: utf-8 -*-
"""OpenAI_Whisper_V3_Large_Transcription_Translation (2).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zUJZvFYN_eHooE79MjRV50ERx6FSXqKZ

### Installs the required packages
"""

# Installs packages
# pip install --upgrade git+https://github.com/huggingface/transformers.git accelerate datasets[audio]

"""### Imports the required packages"""

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline, Pipeline

"""### Sets up the device and data types"""


def setup_ai() -> Pipeline:
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    # device = "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    """### Specifies the model"""

    # Other available model variants can be found here: https://huggingface.co/openai/whisper-large-v3#:~:text=on%20the%20Hub%3A-,Size,%E2%9C%93,-Usage
    model_id = "openai/whisper-large-v3"

    """### Initializes and configures the model and the processor"""

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=False, use_safetensors=True
        # Use Flash Attention if you have a GPU that supports it (Ampere and newer)
        # ,use_flash_attention_2=True
    ).to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    """### Configures the pipeline"""

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=420,
        chunk_length_s=8,  # Adjust this based on the type of audio content
        batch_size=8,  # Adjust this based on your hardware (Fine for T4 GPU)
        return_timestamps=True,  # Set this to false if you don't want/need timestamps
        torch_dtype=torch_dtype,
        device=device,
    )

    return pipe


"""### Specifies the audio file path and filetype"""


# Formats the timestamps to be more readable
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def run_ai(pipe: Pipeline, audio: bytes) -> str:
    """### Sets the language and task (Transcription, Translation)"""

    # Use this for transcription (Change <"language": "german"> to your audio files language)
    result = pipe(audio, generate_kwargs={"language": "russian", "task": "transcribe"})

    # Use this for translation to English (Change <"language": "german"> to your audio files language)
    # result = pipe(audio, generate_kwargs={"language": "german", "task": "translate"})

    """### Formats the output and saves it to a text file"""

    # Saves the Models Output to a text file in Google Colabs "/content/" directory
    res = ""
    for i, chunk in enumerate(result['chunks']):
        start_time, end_time = chunk['timestamp']
        formatted_start_time = format_time(start_time)
        formatted_end_time = format_time(end_time)
        text = chunk['text']

        res += f"Segment {i + 1}:\n"
        res += f"Start Time: {formatted_start_time}, End Time: {formatted_end_time}\n\n"
        res += f"Text: {text}\n"

    return res

    # with open('/content/whisper_output.txt', 'r') as f:
    #     orig = f.read()
    # with open('/content/whisper_output_96.txt', 'r') as f:
    #     orig_96 = f.read()
    # orig == orig_96