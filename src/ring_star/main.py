"""Module principal pour l'optimisation du problème du Ring Star (RSP).

Ce module charge des instances du RSP depuis le dossier `instances`,
applique une métaheuristique sélectionnée pour rechercher des
solutions de bonne qualité, puis sauvegarde les résultats dans
le dossier `results`.

Métaheuristiques disponibles :
    - Recherche Locale (Local Search)
    - Recuit Simulé (Simulated Annealing)
    - Recherche Tabou (Tabu Search)
"""

from pathlib import Path

from ring_star.functions import create_solution, load_data
from ring_star.metaheuristics import LS_Iterate, RecSim, TabuSearch


def main():
    """Exécute une métaheuristique sur 9 instances et sauvegarde les solutions.

    Pour chaque instance du dossier `instances`, applique la métaheuristique
    choisie, et sauvegarde le résultat dans le dossier `results`.
    """
    # Choix de la métaheuristique
    method_name = "local_search"  # Options : "local_search", "simulated_annealing", "tabu_search"

    # Correspondance entre noms et fonctions
    methods = {
        "local_search": LS_Iterate,
        "simulated_annealing": RecSim,
        "tabu_search": TabuSearch,
    }

    # Sélection de la métaheuristique
    metaheuristic = methods[method_name]

    # Création du dossier de résultats
    results = Path("results") / method_name
    results.mkdir(parents=True, exist_ok=True)

    for i in range(9):
        # Chargement des données
        data = load_data(f"instances/data{i + 1}.dat")
        sol = metaheuristic(data)

        # Affichage des résultats
        print(f"\n--- Solution {i + 1} terminée ---")
        print(f"  • Coût total : {sol[2]}")
        print(f"  • Proportion de nœuds dans l'anneau : {100 * len(sol[0]) / data[0]:.2f} %")
        # Optionnel : Aperçu détaillé de la solution
        # print(f"  • Détails de la solution :\n    - Ring : {sol[0]}\n    - Star : {sol[1]}")

        # Création du fichier de solution
        filename = f"solution_{i + 1}.txt"
        filepath = results / filename
        create_solution(filepath, sol)
