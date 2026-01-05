# Ticketing Starter 🎫 Module R4.01 Architecture logicielle (BUT2)

Année 2025/2026 - Enseignant : Marc Ennaji (marc.ennaji@univ-rennes.fr)

> **Template de démarrage** pour le projet pédagogique R4.01 — Architecture hexagonale

Ce dépôt est un **squelette d'application** prêt à l'emploi, pour le projet de gestion de tickets. Il fournit :
- ✅ L'arborescence des principaux répertoires du projet (domain, ports, adapters, application)
- ✅ La configuration automatique des outils (pre-commit, pytest, ruff)
- ✅ Des fichiers TODO à compléter progressivement
- ✅ Des tests exemples à décommenter

**Objectif** : Vous permettre de vous concentrer sur l'apprentissage de l'architecture hexagonale, sans perdre de temps sur la configuration initiale.

---

## 📚 Documentation complète

**Tous les guides et TDs sont dans le repository de ressources :**

👉 https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources

### Liens directs essentiels

- [📖 Guide de démarrage](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/td/guides/demarrage.md) ⚠️ **À suivre AVANT le TD0**
- [🔄 Workflow Git/GitHub](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/td/guides/workflow_de_developpement.md)
- [🧪 Guide des tests](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/td/guides/comment_tester.md)

---

## 🚀 Démarrage rapide

**Première utilisation ?** Suivez le [Guide de démarrage](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/td/guides/demarrage.md) pas à pas.

**Commandes essentielles** (après installation) :
```bash
# Initialiser l'environnement (à faire avant chaque TD)
source scripts/init.sh

# Lancer le serveur
uvicorn src.main:app --reload   # → http://localhost:8000

# Lancer les tests
pytest

# Vérifier la qualité du code (PEP 8, naming, etc.)
bash scripts/check_quality.sh
```

---

## 🏗️ Architecture du projet

Ce projet suit l'**architecture hexagonale** (aussi appelée "Ports & Adapters").

![Architecture conceptuelle](https://raw.githubusercontent.com/Marcennaji/architecture-logicielle-BUT2-ressources/main/docs/architecture/01_vue_conceptuelle.png)

### Principe clé

**Le domaine métier ne dépend de RIEN.**

Toutes les dépendances pointent **vers** le domaine, jamais l'inverse. Le domaine ne connaît ni FastAPI, ni SQLite, ni aucun framework.

### Progression par jalons

Vous construirez cette architecture progressivement :

| Jalon | Composant | Contenu | Objectif |
|-------|--------|---------|----------|
| **TD1** | Domain | `Ticket`, `User`, `Status` | Entités métier pures + règles métier |
| **TD2** | Ports | `TicketRepository` (ABC) | Interfaces abstraites (contrats) |
| **TD3** | Application | `CreateTicket`, `ListTickets` | Use cases (orchestration) |
| **TD4** | Adapters | `FastAPIRouter`, `SQLiteRepository` | Implémentations concrètes |
| **TD5+** | Intégration | `main.py` | Câblage et injection de dépendances |

### Les 5 composants

L'architecture est **concentrique** : tout dépend du domaine au centre.

- **Domain** (`domain/`) : Cœur métier — entités, règles métier, value objects
- **Ports** (`ports/`) : Interfaces abstraites définies par le métier
- **Application** (`application/`) : Use cases orchestrant le domaine
- **Adapters** (`adapters/`) : Implémentations concrètes (API, DB)
- **Composition Root** (`main.py`) : Câblage et injection des dépendances

**Flux d'exécution** : Requête API → Use Case → Domaine  
**Flux de dépendances** : Adapters → Application → Domain ← Ports (tout pointe vers le centre)

💡 Voir le [diagramme conceptuel](https://raw.githubusercontent.com/Marcennaji/architecture-logicielle-BUT2-ressources/main/docs/architecture/01_vue_conceptuelle.png) et le [CM sur l'architecture hexagonale](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/cm/CM1_Fondamentaux_architecture.md) pour comprendre l'organisation concentrique.

---

## 📁 Structure du projet

```
ticketing_starter/
├── docs/               # Documentation spécifique au projet
├── scripts/            # Scripts utilitaires (init.sh)
├── tests/              # Tests par couche (domain, application, e2e)
├── src/
│   ├── domain/         # Logique métier pure (aucune dépendance externe)
│   ├── ports/          # Interfaces abstraites (ABC)
│   ├── application/    # Cas d'utilisation (use cases)
│   ├── adapters/       # Implémentations concrètes (API, BDD)
│   └── main.py         # Racine de composition (câblage des dépendances)
├── requirements.txt    # Dépendances Python
├── pyproject.toml      # Configuration projet (ruff, pytest)
└── .pre-commit-config.yaml  # Hooks de formatage automatique
```

Chaque dossier contient un `README.md` rappelant son rôle et ses règles.

Pour comprendre l'architecture en détail, consultez le [CM sur l'architecture hexagonale](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/cm/CM1_Fondamentaux_architecture.md#-4-architecture-hexagonale-ports--adapters).

### 📐 Arborescence obligatoire

⚠️ **IMPORTANT** : L'arborescence de base (`src/domain/`, `src/ports/`, `src/application/`, `src/adapters/`, `tests/`) est **obligatoire et identique pour tous les étudiants**.

**✅ Autorisé** : Créer des sous-dossiers à l'intérieur (ex: `src/domain/entities/`, `src/adapters/db/repositories/`)

**❌ Interdit** : Renommer, déplacer ou supprimer les dossiers principaux

Cette contrainte permet à tous de travailler sur une base commune et facilite l'accompagnement pédagogique.

---

## 🎯 Objectifs pédagogiques

- Comprendre la séparation Domain / Application / Adapters
- Implémenter des ports (interfaces) et leurs adapters
- Appliquer l'**inversion de dépendances** et le câblage dans `main.py`
- Écrire des tests par couche (unitaires, intégration, end-to-end)

---

## � Vérification qualité du code

**Avant chaque commit**, le code est automatiquement vérifié et formaté par les pre-commit hooks :
- **Black** : Formatage automatique du code
- **Ruff** : Vérification PEP 8, imports, naming conventions

### Vérifier manuellement votre code

```bash
# Vérifier tous les problèmes (sans les corriger)
python -m ruff check .

# Vérifier seulement les naming conventions PEP 8
python -m ruff check . --select N

# Corriger automatiquement ce qui peut l'être
python -m ruff check . --fix

# Formater le code
python -m black .
```

### Erreurs de naming courantes

❌ **À éviter :**
```python
class Status_ticket(Enum):    # Underscores dans nom de classe
    pass                      # Pass inutile dans classe non vide
    OPEN = "open"

class Statut_project(Enum):   # Nom en français (anglais obligatoire)
    STARTED = "started"

def MyFunction():             # Majuscules dans nom de fonction
    MyVar = 42                # Majuscules dans nom de variable
```

✅ **Correct :**
```python
class TicketStatus(Enum):     # UpperCamelCase
    """Status values for tickets."""  # Documentation
    OPEN = "open"
    CLOSED = "closed"

class ProjectStatus(Enum):    # Nom en anglais
    """Status for project lifecycle."""
    STARTED = "started"

def my_function():            # snake_case
    my_var = 42               # snake_case
```

**Règles PEP 8 obligatoires :**
- Classes : `UpperCamelCase` (ex: `TicketStatus`, `User`)
- Fonctions/variables : `snake_case` (ex: `create_ticket`, `user_name`)
- Constantes : `UPPER_CASE` (ex: `MAX_RETRY`)
- **Anglais uniquement** dans le code (commentaires en français autorisés)

📋 **[Guide complet des conventions de code](.github/CONVENTIONS.md)**

---

## 📋 Bonnes pratiques attendues

| Pratique | Description |
|----------|-------------|
| **Commits fréquents** | Un commit = une unité de travail logique (fonction, fix, refactoring) |
| **Refactoring continu** | Améliorez le code au fur et à mesure (renommages, extractions, nettoyage) |
| **Messages de commits clairs** | Décrivez ce qui a été fait, pas comment |
| **Conventions PEP 8** | Vérifiez avec `ruff check .` avant chaque commit |

Voir le [Guide de workflow](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/td/guides/workflow_de_developpement.md) pour le processus complet de rendu via tags Git.
