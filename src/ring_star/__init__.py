"""Package de résolution pour le Ring Star Problem (RSP).

Ce package fournit des structures de données et des algorithmes
métaheuristiques pour l'optimisation combinatoire sur des graphes.

Algorithmes disponibles :
    - Recherche Locale (Local Search)
    - Recuit Simulé (Simulated Annealing)
    - Recherche Tabou (Tabu Search)
"""

from importlib.metadata import PackageNotFoundError, version

from .functions import create_solution, load_data
from .main import main
from .metaheuristics import (
    LS_Iterate as local_search,
    RecSim as simulated_annealing,
    TabuSearch as tabu_search,
)

try:
    __version__ = version("ring-star-problem")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = [
    "__version__",
    "create_solution",
    "load_data",
    "local_search",
    "main",
    "simulated_annealing",
    "tabu_search",
]
