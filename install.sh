#!/usr/bin/bash

# =========================================================================
# LEO Translator - One-Liner Termux Installer via curl/wget | bash
# =========================================================================

echo "🚀 Baixando e Instalando LEO Translator no Termux..."

# 1. Instalar git e curl se não estiverem presentes
pkg update -y
pkg install -y git curl python

# 2. Clonar ou atualizar o repositório
REPO_DIR="leo-translator"
if [ ! -d "$REPO_DIR" ]; then
    echo "📥 Clonando repositório..."
    # Substituir pela URL do repositório público do GitHub
    git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git "$REPO_DIR"
fi

cd "$REPO_DIR" || exit 1
git pull origin main 2>/dev/null

# 3. Executar o script de setup completo
chmod +x setup_termux.sh
bash setup_termux.sh
