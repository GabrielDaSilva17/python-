#!/usr/bin/bash

# =========================================================================
# Script de Instalação e Execução Automática no Termux (Android)
# LEO Translator ~ Dicionário & Conversação Frente a Frente 100% Offline
# =========================================================================

echo "🚀 Iniciando configuração do LEO Translator no Termux..."

# 1. Atualizar repositórios do Termux e instalar dependências do sistema
echo "📦 Atualizando pacotes e instalando dependências do sistema..."
pkg update -y && pkg upgrade -y
pkg install -y python git ffmpeg espeak clang libjpeg-turbo rust

# 2. Atualizar o pip e instalar bibliotecas Python do projeto
echo "🐍 Instalando bibliotecas Python (FastHTML, Piper TTS, ArgosTranslate)..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 3. Baixar modelos de voz Piper ONNX neurais (PT, DE, EN)
echo "🎙️ Baixando modelos de voz Piper ONNX (Português, Alemão, Inglês)..."
python download_piper_models.py

# 4. Criar diretórios estáticos
mkdir -p static/audio
mkdir -p piper_models

# 5. Iniciar a aplicação FastHTML
echo "✨ Instalação concluída com sucesso!"
echo "🌐 Iniciando LEO Translator no servidor http://localhost:5001..."
python app.py
