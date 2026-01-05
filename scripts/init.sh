#!/bin/bash
# Script d'initialisation de l'environnement de travail
# ⚠️ À exécuter avec : source scripts/init.sh

# Mode debug pour voir toutes les commandes (décommenter si besoin)
# set -x

# Vérifier que le script est sourcé, pas exécuté
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "❌ Erreur : Ce script doit être exécuté avec 'source'"
    echo ""
    echo "   Utilisez : source scripts/init.sh"
    echo "   Et non   : ./scripts/init.sh"
    echo ""
    exit 1
fi

echo "🚀 Initialisation de l'environnement de travail..."
echo ""

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Vérifier qu'on est dans le bon dossier
echo "🔍 Vérification du répertoire..."
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ Erreur : Ce script doit être exécuté à la racine du projet (où se trouve requirements.txt)${NC}"
    return 1
fi
echo -e "${GREEN}✅ Répertoire correct${NC}"
echo ""

# 2. Récupérer les dernières modifications
echo "📥 Récupération des dernières modifications..."
git pull origin main 2>/dev/null || git pull 2>/dev/null || echo -e "${YELLOW}⚠️  Impossible de pull (pas de remote configuré ou pas de connexion)${NC}"
echo ""

# 3. Créer l'environnement virtuel si nécessaire
echo "🔍 Vérification de l'environnement virtuel..."
if [ ! -f ".venv/bin/activate" ]; then
    # Supprimer venv incomplet s'il existe
    if [ -d ".venv" ]; then
        echo "⚠️  Venv incomplet détecté, suppression..."
        rm -rf .venv
    fi
    
    echo "🐍 Création de l'environnement virtuel..."
    echo "   Commande: python3 -m venv .venv"
    
    # Essayer de créer le venv (SANS masquer les erreurs)
    python3 -m venv .venv
    VENV_EXIT_CODE=$?
    
    echo "   Code retour: $VENV_EXIT_CODE"
    
    if [ $VENV_EXIT_CODE -ne 0 ]; then
        echo -e "${RED}❌ Erreur lors de python3 -m venv (code: $VENV_EXIT_CODE)${NC}"
        return 1
    fi
    
    if [ ! -f ".venv/bin/activate" ]; then
        echo -e "${RED}❌ Erreur : .venv/bin/activate n'existe pas après création${NC}"
        echo ""
        echo "Diagnostic:"
        echo "  - Le venv a été créé mais le fichier activate est manquant"
        echo "  - Cela indique généralement que python3-venv n'est pas installé"
        echo ""
        echo "Solution : Installez python3-venv avec :"
        echo "   sudo apt update && sudo apt install -y python3-venv"
        echo ""
        echo "Puis relancez : source scripts/init.sh"
        rm -rf .venv
        return 1
    fi
    
    echo -e "${GREEN}✅ Environnement virtuel créé${NC}"
else
    echo -e "${GREEN}✅ Environnement virtuel existant${NC}"
fi
echo ""

# 4. Activer l'environnement virtuel
echo "🔌 Activation de l'environnement virtuel..."
echo "   Commande: source .venv/bin/activate"

# Tenter l'activation (SANS masquer les erreurs)
source .venv/bin/activate
ACTIVATE_EXIT_CODE=$?

echo "   Code retour: $ACTIVATE_EXIT_CODE"

if [ $ACTIVATE_EXIT_CODE -ne 0 ]; then
    echo -e "${RED}❌ Erreur lors de l'activation (code: $ACTIVATE_EXIT_CODE)${NC}"
    return 1
fi

echo -e "${GREEN}✅ Environnement activé${NC}"
echo ""

# 5. Installer/mettre à jour les dépendances
echo "📦 Installation des dépendances..."
echo "   Commande: pip install -q -r requirements.txt"

pip install -q -r requirements.txt
PIP_EXIT_CODE=$?

echo "   Code retour: $PIP_EXIT_CODE"

if [ $PIP_EXIT_CODE -ne 0 ]; then
    echo -e "${RED}❌ Erreur lors de l'installation des dépendances (code: $PIP_EXIT_CODE)${NC}"
    return 1
fi

echo -e "${GREEN}✅ Dépendances installées${NC}"
echo ""

# 6. Configurer pre-commit si nécessaire
echo "🔧 Configuration de pre-commit..."
if [ ! -f ".git/hooks/pre-commit" ]; then
    echo "   Commande: pre-commit install"
    
    pre-commit install
    PRECOMMIT_EXIT_CODE=$?
    
    echo "   Code retour: $PRECOMMIT_EXIT_CODE"
    
    if [ $PRECOMMIT_EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✅ Pre-commit configuré${NC}"
    else
        echo -e "${YELLOW}⚠️  Erreur lors de la configuration pre-commit (non critique, code: $PRECOMMIT_EXIT_CODE)${NC}"
    fi
else
    echo -e "${GREEN}✅ Pre-commit déjà configuré${NC}"
fi
echo ""

# 7. Lancer les tests pour vérifier
echo "🧪 Vérification avec les tests..."
echo "   Commande: pytest -q"

pytest -q
PYTEST_EXIT_CODE=$?

echo "   Code retour: $PYTEST_EXIT_CODE"

if [ $PYTEST_EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Tous les tests passent !${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  Certains tests échouent (code: $PYTEST_EXIT_CODE). Vérifiez votre code.${NC}"
fi
echo ""

echo "=========================================="
echo -e "${GREEN}🎉 Environnement prêt !${NC}"
echo ""
echo "Commandes utiles :"
echo "  pytest                         → Lancer les tests"
echo "  uvicorn src.main:app --reload  → Démarrer le serveur"
echo "=========================================="
