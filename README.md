# 🇩🇪 LEO Translator & Pocket Dictionary (100% Offline) 🇵🇹

Aplicativo **FastHTML (100% Python)** com **Dicionário LEO**, **Modo Conversação Live para 2 Pessoas (Frente a Frente para Celular)**, **Flexionstabelle (Conjugação)**, **Sintetizador de Voz Neural Piper ONNX** e **Google Gemini AI**.

---

## 📱 Instalação Automática de 1 Clique no Termux (Android)

Abra o seu **Termux** no celular, copie e cole o comando abaixo:

```bash
git clone <URL_DO_SEU_REPOSITORIO_GITHUB> leo-translator && cd leo-translator && bash setup_termux.sh
```

O script irá:
1. Atualizar o Termux e instalar Python, Git, FFmpeg e compiladores.
2. Instalar todas as dependências Python (`FastHTML`, `Piper TTS`, `ArgosTranslate`).
3. Baixar os modelos neurais **Piper ONNX** (Português, Alemão, Inglês).
4. Iniciar o servidor automaticamente em `http://localhost:5001`.

---

## ⚡ Recursos do Projeto

- **📱 Modo Conversação 2 Pessoas (Frente a Frente)**:
  - **Pessoa A (Metade Superior)**: Girada em 180° para quem está do outro lado da mesa.
  - **Pessoa B (Metade Inferior)**: Orientação normal (0°) virada para você.
  - **Voz Neural Piper ONNX**: Fala a tradução em voz alta em tempo real!

- **📖 Dicionário LEO Multi-Idioma**:
  - Filtro por **Verbos**, **Expressões**, **Substantivos** (com artigos `das/die/der`) e **Exemplos**.
  - Tabela de conjugação **Flexionstabelle** em 1 clique (Präsens, Perfekt, Präteritum, Plusquamperfekt, Futur I).
  - Correção gramatical Duden para evitar plurais disfarçados de verbos.
  - Desambiguação por contexto (ex: *correr* $\rightarrow$ *rennen* `[alta velocidade]`, *laufen* `[jogging/a pé]`, *fließen* `[líquidos]`).

- **✨ Integração Gemini AI**:
  - Explicações gramaticais detalhadas diretamente salvas no `.env`.

---

## 🛠️ Como Subir para o seu GitHub

No seu computador:

```bash
git add .
git commit -m "feat: LEO Translator FastHTML com Modo Conversação 2 Pessoas e Piper ONNX para Termux"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
git push -u origin main
```
