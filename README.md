# 🇩🇪 LEO Translator & Pocket Dictionary (100% Offline) 🇵🇹

Aplicativo **FastHTML (100% Python)** com **Dicionário LEO**, **Modo Conversação Live para 2 Pessoas (Frente a Frente para Celular)**, **Flexionstabelle (Conjugação)**, **Sintetizador de Voz Neural Piper ONNX** e **Google Gemini AI**.

---

## ⚡ Instalação Super Rápida de 1 Linha no Termux (curl | bash)

Abra o seu **Termux** no celular, copie e cole **este único comando**:

```bash
curl -sSL https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPOSITORIO/main/install.sh | bash
```

> **O que este comando faz automaticamente:**
> 1. Atualiza o Termux e instala Python, Git, FFmpeg e os compiladores.
> 2. Baixa o projeto direto do seu GitHub público.
> 3. Instala as dependências Python (`FastHTML`, `Piper TTS`, `ArgosTranslate`).
> 4. Baixa os modelos neurais **Piper ONNX** (Português, Alemão, Inglês).
> 5. Abre o aplicativo automaticamente no seu navegador em `http://localhost:5001`.

---

## 📱 Método Alternativo (Manual no Termux)

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git leo-translator && cd leo-translator && bash setup_termux.sh
```

---

## 🛠️ Como Subir para o seu GitHub Público

No seu computador:

```bash
git add .
git commit -m "feat: Adicionado script de instalação de 1 linha (curl | bash) para Termux"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```
