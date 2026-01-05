#!/bin/bash
# Script de vérification qualité du code
# Usage: ./scripts/check_quality.sh

echo "🔍 Vérification de la qualité du code..."
echo ""

# 1. Vérifier les naming conventions PEP 8
echo "1️⃣  Vérification PEP 8 naming conventions..."
python -m ruff check src/ tests/ --select N
NAMING_EXIT=$?

# 2. Vérifier toutes les règles (style, imports, bugs)
echo ""
echo "2️⃣  Vérification complète (style, imports, bugs)..."
python -m ruff check src/ tests/
RUFF_EXIT=$?

# 3. Vérifier le formatage
echo ""
echo "3️⃣  Vérification du formatage (Black)..."
python -m black --check src/ tests/
BLACK_EXIT=$?

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $NAMING_EXIT -eq 0 ] && [ $RUFF_EXIT -eq 0 ] && [ $BLACK_EXIT -eq 0 ]; then
    echo "✅ Tout est OK ! Votre code respecte toutes les conventions."
    exit 0
else
    echo "❌ Des problèmes ont été détectés."
    echo ""
    echo "💡 Pour corriger automatiquement :"
    echo "   python -m ruff check . --fix    # Corrections auto (imports, etc.)"
    echo "   python -m black .               # Formatage"
    echo ""
    echo "⚠️  Les problèmes de naming (N801, N802, etc.) doivent être"
    echo "   corrigés manuellement (renommer classes/fonctions)."
    exit 1
fi
