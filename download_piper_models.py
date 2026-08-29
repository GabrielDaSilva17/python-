"""
Piper TTS ONNX Neural Voice Models Downloader
Downloads official Piper models for Portuguese (pt_BR), German (de_DE), and English (en_US).
"""

import os
import urllib.request

MODELS_DIR = "piper_models"
os.makedirs(MODELS_DIR, exist_ok=True)

piper_models = {
    "pt": {
        "onnx": "https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx",
        "json": "https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json",
        "name": "pt_BR-faber-medium.onnx"
    },
    "de": {
        "onnx": "https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx",
        "json": "https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx.json",
        "name": "de_DE-thorsten-medium.onnx"
    },
    "en": {
        "onnx": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx",
        "json": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json",
        "name": "en_US-lessac-medium.onnx"
    }
}

def download_all_models():
    for lang, data in piper_models.items():
        onnx_path = os.path.join(MODELS_DIR, data["name"])
        json_path = os.path.join(MODELS_DIR, data["name"] + ".json")
        
        if not os.path.exists(onnx_path):
            print(f"Baixando modelo Piper ONNX ({lang.upper()}): {data['name']}...")
            urllib.request.urlretrieve(data["onnx"], onnx_path)
            print(f"[OK] {data['name']} baixado!")
            
        if not os.path.exists(json_path):
            print(f"Baixando configuracao JSON ({lang.upper()})...")
            urllib.request.urlretrieve(data["json"], json_path)
            print(f"[OK] {data['name']}.json baixado!")

if __name__ == "__main__":
    download_all_models()
    print("Todos os modelos de voz Piper (PT, DE, EN) foram baixados com sucesso!")
