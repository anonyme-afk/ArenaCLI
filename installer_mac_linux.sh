#!/bin/bash
set -euo pipefail

echo ""
echo "=========================================="
echo "  Arena.ai CLI V2 - Installation"
echo "=========================================="
echo ""

# Vérifie Python
if ! command -v python3 &>/dev/null; then
    echo "[ERREUR] Python 3 n'est pas installé."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Installe-le avec : brew install python3"
        echo "Ou télécharge-le sur https://www.python.org/downloads/"
    else
        echo "Installe-le avec : sudo apt install python3 python3-venv python3-pip"
    fi
    exit 1
fi

echo "[OK] Python 3 détecté : $(python3 --version)"
echo ""

# Crée un venv (propre, pas de conflits système)
echo "[1/4] Création de l'environnement virtuel..."
python3 -m venv .venv

# Active le venv
source .venv/bin/activate

echo "[2/4] Mise à jour de pip..."
python -m pip install --upgrade pip --quiet

echo "[3/4] Installation des dépendances depuis requirements.txt..."
python -m pip install -r requirements.txt --quiet

echo "[4/4] Téléchargement du navigateur Chromium..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    python -m playwright install chromium
else
    python -m playwright install --with-deps chromium
fi

echo ""
echo "=========================================="
echo "  Installation terminée !"
echo "=========================================="
echo ""
echo "  Pour utiliser Arena CLI :"
echo ""
echo "    source .venv/bin/activate"
echo "    python arena.py"
echo ""
echo "  Astuce : ajoute un alias dans ton ~/.bashrc ou ~/.zshrc :"
echo "    alias arena='cd $(pwd) && source .venv/bin/activate && python arena.py'"
echo ""

read -p "Lancer maintenant ? (y/N) " launch_now
if [[ "$launch_now" =~ ^[Yy]$ ]]; then
    python arena.py
fi
