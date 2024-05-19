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

import re
import pickle

from fuzzywuzzy import process
from nltk.stem.snowball import RussianStemmer

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


# Formats thedock timestamps to be more readable
def format_time(seconds):
    if type(seconds) != type(None):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return '--:--:--'


def run_ai(pipe: Pipeline, audio: bytes) -> tuple[str, int, int]:
    """### Sets the language and task (Transcription, Translation)"""

    # Use this for transcription (Change <"language": "german"> to your audio files language)
    print("run ai")
    result = pipe(audio, generate_kwargs={"language": "russian", "task": "transcribe"})
    print(f"got result{result}")
    # Use this for translation to English (Change <"language": "german"> to your audio files language)
    # result = pipe(audio, generate_kwargs={"language": "german", "task": "translate"})

    """### Formats the output and saves it to a text file"""
    # Saves the Models Output to a text file in Google Colabs "/content/" directory
    # print("save result")
    # res = ""
    # for i, chunk in enumerate(result['chunks']):
    #     start_time, end_time = chunk['timestamp']
    #     formatted_start_time = format_time(start_time)
    #     formatted_end_time = format_time(end_time)
    #     text = chunk['text']
    #
    #     res += f"Segment {i + 1}:\n"
    #     res += f"Start Time: {formatted_start_time}, End Time: {formatted_end_time}\n\n"
    #     res += f"Text: {text}\n"

    print("return result")
    ans = result_process(result)
    return ans


def result_process(result) -> tuple[str, int, int]:
    # Открываем файлы white_list, black_list
    with open('white_list', 'rb') as f:
        white_list = pickle.load(f)

    with open('black_list', 'rb') as f:
        black_list = pickle.load(f)

    # Убираем окончания
    stemmer = RussianStemmer()
    stem_white_list = [stemmer.stem(x) for x in white_list]

    # Обрабатываем результат распознавания
    # Получаем текст
    text = result['text'].strip()
    # Вырезаем "Продолжение следует..."
    text = text.replace('Продолжение следует...', '')
    # Вырезаем описание звуков капсом
    matches = re.findall(
        r"(\b(?:[А-Я]+[а-я]?[А-Я]+|[А-Я]*[а-я]?[А-Я]+)\b(?:\s+(?:[А-Я]+[а-я]?[А-Я]+|[А-Я]*[а-я]?[А-Я]+)\b)*)", text)
    for i in matches:
        text = text.replace(i, '')

    # Считаем коэфы
    words = [word.strip('., ') for word in text.split()]

    # вайт-лист
    correct_words = []
    for i in words:
        x = process.extractOne(stemmer.stem(i), stem_white_list)
        # print(i, x)
        # x = process.extractOne(i, white_list)
        if x[1] > 90:
            correct_words.append(i)
            # print(i, x)
    correct_ratio = round(len(correct_words) / len(words) * 100)

    # блэк-лист
    incorrect_words = []
    for word in black_list:
        # print(i, x)
        x = process.extractOne(word, words)
        if x[1] > 90:
            incorrect_words.append(x[0])
            # print(word, x)
    incorrect_ratio = round(len(incorrect_words) / len(words) * 100)

    # Выделение неправильных слов звездочками
    for i in incorrect_words:
        text = text.replace(i, f'*{i}*')

    return text, correct_ratio, incorrect_ratio
