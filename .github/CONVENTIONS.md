# Conventions de code - R4.01 Architecture logicielle

Ce document liste les conventions de code **obligatoires** pour le projet. Le non-respect de ces conventions entraîne des pénalités lors de l'évaluation.

## 🎯 Vérification automatique

Avant chaque commit, lancez :
```bash
bash scripts/check_quality.sh
```

**Les pre-commit hooks vérifient et corrigent automatiquement** la plupart des problèmes. Assurez-vous qu'ils sont activés :
```bash
pre-commit install
```

---

## ✅ Règles PEP 8 - Naming conventions

### Classes : `UpperCamelCase`

❌ **Incorrect :**
```python
class ticket_Status(Enum):     # snake_case
    pass

class Status_ticket(Enum):     # Underscores
    pass

class TICKETSTATUS(Enum):      # Tout en majuscules
    pass
```

✅ **Correct :**
```python
class TicketStatus(Enum):      # UpperCamelCase
    """Status values for tickets."""
    OPEN = "open"
    CLOSED = "closed"
```

**Règle Ruff :** `N801` - Détecté par `ruff check . --select N`

---

### Fonctions et méthodes : `snake_case`

❌ **Incorrect :**
```python
def CreateTicket():            # UpperCamelCase
    pass

def create_Ticket():           # mixedCase
    pass
```

✅ **Correct :**
```python
def create_ticket():           # snake_case
    """Create a new ticket."""
    pass
```

**Règle Ruff :** `N802` - Détecté par `ruff check . --select N`

---

### Variables : `snake_case`

❌ **Incorrect :**
```python
def my_function():
    UserName = "John"          # UpperCamelCase
    ticket_ID = 123            # mixedCase
```

✅ **Correct :**
```python
def my_function():
    user_name = "John"         # snake_case
    ticket_id = 123
```

**Règle Ruff :** `N806` - Détecté par `ruff check . --select N`

---

### Constantes : `UPPER_CASE`

❌ **Incorrect :**
```python
max_retries = 3                # snake_case pour constante
MaxRetries = 3                 # UpperCamelCase
```

✅ **Correct :**
```python
MAX_RETRIES = 3                # UPPER_CASE
DEFAULT_TIMEOUT = 30
```

**Règle Ruff :** `N803` - Détecté par `ruff check . --select N`

---

## 🌍 Langue : Anglais obligatoire

**Le code (noms de classes, fonctions, variables) DOIT être en anglais.**

❌ **Incorrect :**
```python
class Statut_project(Enum):    # Français
    EN_COURS = "en_cours"
    TERMINE = "termine"

def creer_ticket():            # Français
    pass
```

✅ **Correct :**
```python
class ProjectStatus(Enum):     # Anglais
    """Status for project lifecycle."""
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

def create_ticket():           # Anglais
    """Create a new ticket."""
    pass
```

**Note :** Les commentaires et docstrings peuvent être en français.

**Détection :** Notre système d'évaluation détecte automatiquement l'usage de mots français courants (statut, projet, utilisateur, etc.)

---

## 🧹 Pass inutiles

Les instructions `pass` dans des classes/fonctions **non vides** sont considérées comme du code mort.

❌ **Incorrect :**
```python
class Status(Enum):
    pass                       # Inutile, la classe contient déjà des membres
    OPEN = "open"
    CLOSED = "closed"
```

✅ **Correct :**
```python
class Status(Enum):
    """Ticket status values."""
    OPEN = "open"
    CLOSED = "closed"
```

**Cas valide :** `pass` est accepté uniquement pour les classes/fonctions **vides** (stub):
```python
class AbstractRepository(ABC):
    pass  # OK : classe vide servant de marqueur
```

---

## 📚 Documentation des Enums

Chaque Enum **doit avoir une docstring** expliquant son rôle.

❌ **Incorrect :**
```python
class Priority(Enum):          # Pas de docstring
    LOW = "low"
    HIGH = "high"
```

✅ **Correct :**
```python
class Priority(Enum):
    """
    Ticket priority levels.
    
    LOW: Normal tickets, no urgency
    HIGH: Urgent tickets requiring immediate attention
    """
    LOW = "low"
    HIGH = "high"
```

---

## 🏗️ Classes orphelines

**Les classes du domaine doivent être utilisées.**

Une classe orpheline est une classe définie mais jamais importée/référencée par d'autres classes du domaine.

❌ **Problème :**
```python
# src/domain/project.py
class Project:              # Définie mais jamais utilisée
    pass

# src/domain/ticket.py
class Ticket:
    pass                    # N'utilise pas Project
```

✅ **Solution :**
```python
# src/domain/ticket.py
from src.domain.project import Project

class Ticket:
    """Ticket linked to a project."""
    def __init__(self, project: Project):
        self.project = project
```

**Note :** Cette règle ne s'applique qu'aux classes du `src/domain/`. Les adapters, use cases, etc. ne sont pas concernés.

---

## 🚨 Pénalités lors de l'évaluation

Le système d'évaluation automatique détecte ces violations et applique :

**-1 point par TYPE de violation détecté** (max -5 points)

Types de violations :
1. ❌ Noms de classes non conformes PEP 8
2. ❌ Usage du français dans le code
3. ❌ Pass inutiles dans classes non vides
4. ❌ Classes orphelines (non utilisées)
5. ❌ Enums sans documentation

**Exemple :** Un code avec 3 classes mal nommées + 2 usages français = **-2 points** (2 types différents)

---

## 🛠️ Outils de vérification

### Vérification complète (recommandé)
```bash
bash scripts/check_quality.sh
```

### Vérification manuelle par type

```bash
# Naming conventions PEP 8
python -m ruff check . --select N

# Tous les problèmes (imports, bugs, style)
python -m ruff check .

# Formatage
python -m black --check .
```

### Corrections automatiques

```bash
# Corriger imports, types modernes, etc.
python -m ruff check . --fix

# Formater le code
python -m black .
```

⚠️ **Les problèmes de naming doivent être corrigés manuellement** (renommer classes, fonctions, variables).

---

## 📖 Ressources

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Ruff - Documentation des règles](https://docs.astral.sh/ruff/rules/)
- [Black - The uncompromising code formatter](https://black.readthedocs.io/)

**Questions ?** Consultez le [Guide de démarrage](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/td/guides/demarrage.md) ou demandez à l'enseignant.
