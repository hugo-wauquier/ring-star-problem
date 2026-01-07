"""Module principal pour l'optimisation du problème du Ring Star (RSP).

Ce module charge des instances du RSP depuis le dossier `data`,
applique une métaheuristique sélectionnée pour rechercher des
solutions de bonne qualité, puis sauvegarde les résultats dans
le dossier `results`.

Les métaheuristiques disponibles incluent :
- la recherche locale (Local Search),
- le recuit simulé (Simulated Annealing),
- la recherche tabou (Tabu Search).
"""

from pathlib import Path

from functions import create_solution, load_data
from metaheuristics import LS_Iterate, RecSim, TabuSearch


def main():
    """Exécute une métaheuristique sur 9 instances et sauvegarde les solutions.

    Pour chaque instance du dossier `data`, applique la métaheuristique choisie,
    et sauvegarde le résultat dans le dossier `results`.
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
        data = load_data(f"data/data{i + 1}.dat")
        sol = metaheuristic(data)

        # Affichage des résultats
        print(f"\nSolution {i + 1} terminée → coût = {sol[2]}")
        # print(f"Détails de la solution :\n    - Ring : {sol[0]}\n    - Star : {sol[1]}")  # Aperçu détaillé de la solution
        print(f"Proportion de nœuds du ring : {100 * len(sol[0]) / data[0]:.2f} %")

        # Création du fichier de solution
        filename = f"solution_{i + 1}.txt"
        filepath = results / filename
        create_solution(filepath, sol)


if __name__ == "__main__":
    main()
