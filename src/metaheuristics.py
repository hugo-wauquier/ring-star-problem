import copy
import math
import random
import time

from functions import BestNeighbor, FindMin, IS_Iterate, TabuNeighbors


# Recherche locale
def LocalSearch(data, sol):

    max_no_improve = 100
    count_no_improve = 0
    bestsol = copy.deepcopy(sol)

    if len(sol[0]) > 3:
        while count_no_improve < max_no_improve:
            x = random.choices([1, 2, 3], weights=[0.2, 0.5, 0.3])[0]
            sol = BestNeighbor(data, sol, x)
            if sol[2] < bestsol[2]:
                bestsol = sol.copy()
                # print("[INFO] Best cost solution:", bestsol[2])
                count_no_improve = 0
            else:
                count_no_improve += 1
    
    return bestsol


# Itération de la recherche locale
def LS_Iterate(data):

    temp = float("inf")

    # Temps total (Minutes * 60 secondes)
    finaltime = 0.5 * 60
    start = time.time()

    while time.time() - start < finaltime:

        sol = IS_Iterate(data, 10)
        sol = LocalSearch(data, sol)
        cost = sol[2]
        if cost < temp:
            temp = cost
            bestsol = sol.copy()

    return bestsol


# Recuit simulé
def RecSim(data):

    sol = IS_Iterate(data, 1000)
    bestsol = copy.deepcopy(sol)

    # Temps total (Minutes * 60 secondes)
    finaltime = 0.5 * 60
    start = time.time()

    while time.time() - start < finaltime:

        T = random.randint(50, 300)
        Tf = random.random() * random.randint(1, 3)
        coeff = random.randint(50, 90) / 100
        while T > Tf:

            if len(sol[0]) > 3:
                for _ in range(10):
                    x = random.choices([1, 2, 3], weights=[0.2, 0.4, 0.4])[0]
                    newsol = BestNeighbor(data, sol, x)
                    delta = newsol[2] - sol[2]
                    if delta < 0:
                        sol = newsol.copy()
                        if sol[2] < bestsol[2]:
                            bestsol = copy.deepcopy(sol)
                    else:
                        p = math.exp(-delta / T)
                        if random.random() < p:
                            sol = newsol.copy()
            T *= coeff
        sol = IS_Iterate(data, 100)

    return LocalSearch(data, bestsol)


# Recherche tabou
def TabuSearch(data):

    len_init = 50
    len_max = 100
    best_global_sol = IS_Iterate(data, 1000)

    # Temps total (Minutes * 60 secondes)
    finaltime = 0.5 * 60
    start = time.time()

    while time.time() - start < finaltime:

        initsol = IS_Iterate(data, 100)
        tabu = []
        Sol = []

        if len(initsol[0]) > 3:
            x = random.choices([1, 2, 3], weights=[0.2, 0.4, 0.4])[0]
            listsol = TabuNeighbors(data, initsol, x)
        else:
            listsol = [copy.deepcopy(initsol)]

        times = 0
        while listsol and times < len_init:

            best_neighbor, i = FindMin(listsol)
            tabu.append(best_neighbor)
            Sol.append(best_neighbor[2])
            listsol.pop(i)
            times += 1

        while len(tabu) < len_max:

            if time.time() - start > finaltime:
                break

            newtabu = copy.deepcopy(tabu)
            s_cur, _ = FindMin(newtabu)

            # Si le ring est trop petit, on ne peut pas optimiser davantage
            if len(s_cur[0]) < 3:
                break

            x = random.choices([1, 2, 3], weights=[0.2, 0.4, 0.4])[0]
            listsol = TabuNeighbors(data, s_cur, x)

            # On trie les voisins (du meilleur au pire)
            verif = []
            while listsol:
                b_sol, idx = FindMin(listsol)
                verif.append(b_sol)
                listsol.pop(idx)

            found_new = False
            for candidate in verif:
                if candidate[2] not in Sol:  # Vérification simple sur le coût
                    tabu.append(candidate)
                    Sol.append(candidate[2])
                    found_new = True
                    break

            if not found_new:
                break

        if tabu:
            local_best, _ = FindMin(tabu)
            if local_best[2] < best_global_sol[2]:
                best_global_sol = copy.deepcopy(local_best)

    return LocalSearch(data, best_global_sol)
