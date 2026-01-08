# 🔗 Optimisation du Problème Ring Star (RSP)

Ce projet universitaire implémente plusieurs **métaheuristiques** pour résoudre le problème du **Ring Star (RSP)**, un problème d'optimisation combinatoire classé **NP-difficile**.

L'objectif est de sélectionner un sous-ensemble de nœuds pour former un anneau (Ring) et de connecter les nœuds restants à cet anneau (Star) afin de minimiser le coût total des connexions.

## 📋 Description du Projet

Le programme cherche à minimiser une fonction de coût composée de deux parties :

1. **Coût du Ring** : Somme des coûts des arêtes reliant les nœuds de l'anneau principal.
2. **Coût des Stars** : Somme des coûts d'affectation des nœuds hors-anneau vers les nœuds de l'anneau.

Trois approches d'optimisation ont été implémentées et comparées :

* **Recherche Locale Itérée (Iterated Local Search)**
* **Recuit Simulé (Simulated Annealing)**
* **Recherche Tabou (Tabu Search)**

## 📂 Structure du Projet

L'organisation des fichiers est la suivante. Le code source se situe dans le répertoire `src`.

```text
ring-star-problem/
├── data/                  # Instances du problème (.dat)
├── results/               # Solutions générées
├── src/                   # Code source
│   ├── __init__.py
│   ├── functions.py       # Fonctions utilitaires
│   ├── main.py            # Point d'entrée du script
│   └── metaheuristics.py  # Algorithmes d'optimisation
├── .gitignore
├── requirements.txt
└── README.md              # Documentation du projet
```

## 🚀 Installation et Prérequis

Ce projet est écrit en **Python 3**. Il ne nécessite aucune bibliothèque externe complexe (utilise uniquement les librairies standards : `copy`, `math`, `pathlib`, `random`, `time`).

1. Assurez-vous d'avoir Python installé.
2. Clonez ou téléchargez ce dépôt.
3. Les instances de test sont déjà présentes dans le dossier `data`. Vous pouvez y ajouter vos propres fichiers `.dat`.

## ⚙️ Utilisation

Pour lancer l'optimisation, exécutez le script principal. Il est recommandé de lancer la commande depuis la racine du projet :

```bash
python src/main.py
```

### Changer de métaheuristique

Par défaut, le programme peut être configuré pour utiliser l'une des trois méthodes. Ouvrez le fichier `src/main.py` et modifiez la variable `method_name` :

```python
# Dans src/main.py, ligne 27
method_name = "local_search"

# Options disponibles : 
# - "local_search"
# - "simulated_annealing"
# - "tabu_search"
```

### Configuration des temps d'exécution

Les temps limites de calcul (critères d'arrêt) sont définis directement dans le fichier `src/metaheuristics.py` (variable `finaltime` au début de chaque fonction).

## 🧠 Algorithmes et Voisinages

Les métaheuristiques explorent l'espace des solutions en utilisant trois opérateurs de voisinage définis dans `src/functions.py` (fonction `BestNeighbor`) :

1. **Swap Adjacent (Inversion)** : Permutation de deux nœuds consécutifs dans l'anneau.
2. **Swap Général (Transposition)** : Échange de deux nœuds quelconques dans l'anneau.
3. **Insertion (Déplacement)** : Déplacement d'un nœud à une autre position dans l'anneau.

### Détails des méthodes

* **Initialisation** : Une solution gloutonne aléatoire est générée (`InitSol`), créant un anneau aléatoire optimisé localement, puis affectant les dépôts au coût optimal.
* **Recherche Locale** : Effectue des descentes stochastiques dans les voisinages jusqu'à un optimum local, puis redémarre (Iterated Local Search).
* **Recuit Simulé** : Accepte parfois des solutions dégradantes selon une probabilité dépendant de la température (refroidissement géométrique) pour échapper aux optimums locaux.
* **Recherche Tabou** : Utilise une liste mémoire pour interdire de revenir sur des solutions récemment visitées.

## 📄 Format des Données

### Entrée (`data/dataX.dat`)

Le fichier doit suivre le format suivant :

* Ligne 1 : Nombre de sommets $N$.
* Lignes suivantes : Matrice des coûts du Ring (Matrice 1).
* Lignes suivantes : Matrice des coûts d'affectation (Matrice 2).

### Sortie (`results/method/solution_X.txt`)

Le fichier de solution généré contient :

* La liste des sommets formant le **RING**.
* La liste des affectations **STAR** (couple `sommet_hors_ring sommet_ring`).
* Le **COST** total de la solution.

## 👥 Auteur

Projet réalisé en **2022** par :

* **Hugo Wauquier**
* Étudiant en **Ingénieur en Informatique** *(MSc in Computer Science & Engineering)*
* Spécialisation : **Intelligence Artificielle**

---

*Projet réalisé dans le cadre du cours d'**Optimisation Combinatoire** à la **Faculté Polytechnique de l'Université de Mons (UMONS)**.*
