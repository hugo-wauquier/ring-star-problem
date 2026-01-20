# 🔗 Résolution du Problème du Ring Star (RSP) par Métaheuristiques

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)

Ce projet universitaire implémente plusieurs **métaheuristiques** pour résoudre le problème du **Ring Star (RSP)**, un problème d'optimisation combinatoire classé **NP-difficile**.

L'objectif est de sélectionner un sous-ensemble de nœuds pour former un anneau (Ring) et de connecter les nœuds restants à cet anneau (Star) afin de minimiser le coût total des connexions.

## 📋 Description du projet

Le programme cherche à minimiser une fonction de coût composée de deux parties :

1. **Coût du Ring** : Somme des coûts des arêtes reliant les nœuds de l'anneau principal.
2. **Coût des Stars** : Somme des coûts d'affectation des nœuds hors-anneau vers les nœuds de l'anneau.

Trois approches d'optimisation ont été implémentées et comparées :

- **Recherche Locale Itérée (Iterated Local Search)**
- **Recuit Simulé (Simulated Annealing)**
- **Recherche Tabou (Tabu Search)**

## 📂 Structure du projet

L'organisation des fichiers suit le standard **`src` layout**. Le code source est encapsulé dans le package `ring_star`.

```text
ring-star-problem/
├── instances/                 # Instances du problème (.dat)
├── results/                   # Solutions générées
├── src/
│   └── ring_star/             # Package principal
│       ├── __init__.py        # Initialise le package
│       ├── __main__.py        # Point d'entrée du package
│       ├── functions.py       # Fonctions utilitaires
│       ├── main.py            # Fonction principale du programme
│       └── metaheuristics.py  # Algorithmes d'optimisation
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE                    # Licence MIT
├── pyproject.toml             # Configuration globale du projet
└── README.md                  # Documentation du projet
```

## 🚀 Installation

Ce projet est développé en **Python 3** et s'installe idéalement dans un environnement isolé afin d'éviter toute interférence avec votre système.

### 1. Récupérer le projet

Commencez par cloner ce dépôt puis accédez au répertoire :

```bash
git clone https://github.com/hugo-wauquier/ring-star-problem.git
cd ring-star-problem
```

### 2. Créer l'environnement virtuel

Il est recommandé d'utiliser un environnement virtuel :

```bash
python -m venv .venv
```

### 3. Activer l'environnement

Activez-le selon votre système d'exploitation :

- **Windows (PowerShell) :**

  ```powershell
  .venv\Scripts\Activate
  ```

- **macOS / Linux :**

  ```bash
  source .venv/bin/activate
  ```

### 4. Installer le projet

Installez le package en mode **éditable** pour garantir une résolution correcte des imports :

```bash
pip install -e .
```

> **Note :** Le projet n'utilise aucune dépendance externe, mais cette installation reste nécessaire avec le `src` layout. Le mode éditable permet de prendre en compte vos modifications sans réinstaller le package.

## ⚙️ Utilisation et paramétrage

Une fois l'installation terminée, vous pouvez lancer l'optimisation via la commande suivante :

```bash
ring-star
```

> Vous pouvez également utiliser `python -m ring_star`.

Le script chargera automatiquement les instances situées dans le dossier `instances`.

### 🔧 Changer de métaheuristique

Actuellement, la configuration s'effectue dans le code. Ouvrez le fichier `src/ring_star/main.py` et modifiez la variable `method_name` pour sélectionner la métaheuristique utilisée :

```python
# Dans `src/ring_star/main.py`, ligne 27
method_name = "local_search"

# Options disponibles : 
# - "local_search"
# - "simulated_annealing"
# - "tabu_search"
```

### ⏱️ Configuration des temps d'exécution

Les critères d'arrêt (temps limites) sont définis dans le fichier `src/ring_star/metaheuristics.py` (variable `finaltime` au début de chaque fonction).

## 🐍 Intégration Python

Ce module peut également être importé dans vos propres scripts ou notebooks afin d'exécuter les algorithmes sur vos données.

### Installation

Choisissez la méthode adaptée à votre situation :

- **Depuis GitHub** (Recommandé pour les notebooks ou scripts autonomes)

  Si vous n'avez pas le code source sur votre machine :

  ```bash
  pip install "git+https://github.com/hugo-wauquier/ring-star-problem.git"
  ```

- **Depuis votre dossier local** (Recommandé si cloné localement)

  Si vous avez déjà récupéré le dépôt, pointez simplement vers son dossier :

  ```bash
  # Remplacez le chemin par la localisation réelle du projet
  pip install -e /chemin/vers/ring-star-problem
  ```

  Cela évite de retélécharger le projet et garde votre librairie synchronisée avec vos modifications locales.

### Exemple minimal

Assurez-vous de disposer d'un fichier d'instance valide au format `.dat` pour exécuter le flux complet :

```python
import ring_star

# Charger une instance
data = ring_star.load_data("chemin/vers/mon_instance.dat")

# Lancer une résolution
solution = ring_star.local_search(data)

# Sauvegarder la solution
ring_star.create_solution("solution.txt", solution)
```

### Métaheuristiques disponibles

- `ring_star.local_search(data)`
- `ring_star.simulated_annealing(data)`
- `ring_star.tabu_search(data)`

## 📄 Format des données

### Entrée (`instances/*.dat`)

Le fichier doit respecter strictement la structure suivante :

- **Ligne 1** : Nombre de sommets $N$ (entier).
- **Lignes 2 à $N + 1$** : Matrice des coûts du Ring (taille $N \times N$).
- **Lignes $N + 2$ à $2N + 1$** : Matrice des coûts d'affectation (taille $N \times N$).

### Sortie (`results/<method>/*.txt`)

Le fichier de solution généré contient :

- La liste des sommets formant le **RING**.
- La liste des affectations **STAR** (couple `sommet_hors_ring` `sommet_ring`).
- Le **COST** total de la solution.

## 🧠 Stratégie de résolution

La résolution du problème s'appuie sur un schéma classique en deux phases : une **construction** initiale suivie d'une **amélioration** par métaheuristiques.

### 1. Phase de construction

Cette étape préliminaire est commune aux trois méthodes. Une heuristique constructive :

- Génère une solution gloutonne aléatoire, créant un anneau optimisé localement.
- Affecte les nœuds restants (Stars) aux nœuds de l'anneau au coût optimal.

### 2. Phase d'amélioration

À partir de la solution construite, l'algorithme cherche à minimiser le coût global via l'une des métaheuristiques suivantes :

- **Recherche Locale (ILS)** : Effectue des descentes stochastiques vers un optimum local, puis applique une perturbation pour explorer de nouvelles régions de l'espace de recherche.
- **Recuit Simulé (SA)** : Accepte parfois des solutions dégradantes selon une probabilité décroissante (refroidissement géométrique), permettant d'échapper aux optimums locaux.
- **Recherche Tabou (TS)** : Utilise une mémoire à court terme (liste tabou) pour interdire le retour vers des solutions récemment visitées et éviter les cycles.

### 📐 Opérateurs de voisinage

Pour explorer l'espace des solutions durant la phase d'amélioration, les métaheuristiques utilisent trois opérateurs de voisinage définis dans `src/ring_star/functions.py` :

1. **Swap Adjacent (Inversion)** : Permutation de deux nœuds consécutifs dans l'anneau.
2. **Swap Général (Transposition)** : Échange de deux nœuds quelconques dans l'anneau.
3. **Insertion (Déplacement)** : Déplacement d'un nœud à une autre position dans l'anneau.

## 👤 Auteur

**Hugo Wauquier** | Ingénieur en Informatique (MSc) | Intelligence Artificielle

- 🐙 **GitHub :** [@hugo-wauquier](https://github.com/hugo-wauquier)
- 💼 **LinkedIn :** [Hugo Wauquier](https://linkedin.com/in/hugo-wauquier)

## 📜 Contexte du projet

> *Ce projet a été réalisé en 2022 dans le cadre du cours d'**Optimisation Combinatoire** à la **Faculté Polytechnique de l'Université de Mons** (UMONS).*
