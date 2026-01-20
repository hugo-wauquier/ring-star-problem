"""Gestion des données et opérateurs de voisinage pour le problème Ring Star.

Ce module fournit l'ensemble des fonctions utilitaires nécessaires à la
manipulation des solutions. Il prend en charge les entrées/sorties, la
construction de solutions initiales, le calcul de la fonction objectif
et la définition des opérateurs de voisinage utilisés par les
algorithmes d'optimisation.

Functions:
    load_data: Charge les matrices de coûts depuis un fichier d'instance.
    create_solution: Formate et écrit la solution finale dans un fichier.
    CalculCost: Évalue le coût total (Ring + Stars) d'une solution.
    OptimizedCost: Calcule le coût optimal d'insertion dans le Ring ou
        d'affectation à une Star (fonction gloutonne).
    InitSol: Génère une solution initiale valide (aléatoire ou gloutonne).
    IS_Iterate: Génère plusieurs solutions initiales pour ne conserver
        que la meilleure (stratégie de redémarrage).
    BestNeighbor: Explore le voisinage (Inversion, Transposition,
        Déplacement) pour trouver le meilleur mouvement améliorant.
    TabuNeighbors: Génère la liste complète des voisins pour
        l'algorithme de recherche tabou.
    FindMin: Trouve la solution ayant le coût minimum dans une liste.
"""

import random


def load_data(name):

    with open(name, "r") as f:
        N = int(f.readline())
        data = f.readlines()
        f.close()

    mat1, mat2 = [], []
    for i in range(N):
        mat1.append(list(map(int, data[i].split())))
        mat2.append(list(map(int, data[N + i].split())))

    output = [N, mat1, mat2]

    return output


def create_solution(name, sol):
    """Pour N sommets au total, sol est une liste contenant :
    
    - sol[0] : liste de n sommets formant le Ring principal
    - sol[1] : liste de (N-n) tuples, chacun représentant deux sommets connectés (les Stars)
    - sol[2] : coût total de la solution, composé de :
        1. Coût du Ring :   somme des coûts des arêtes de l'anneau principal
        2. Coût des Stars : somme des coûts d'affectation des nœuds hors-anneau
    """
    ring, star, cost = sol[0], sol[1], sol[2]
    file = f"RING {len(ring)}\n"
    for i in range(len(ring) - 1):
        file += f"{ring[i]} "
    file += f"{ring[-1]}"
    file += "\nSTAR"
    for i in range(len(star)):
        file += f"\n{star[i][0]} {star[i][1]}"
    file += f"\nCOST {cost}"

    with open(name, "w") as f:
        f.write(file)
        f.close()


def CalculCost(data, sol):

    mat1, mat2 = data[1], data[2]
    ring, star = sol[0], sol[1]
    cost = 0

    # Coûts liés au Ring (Matrice 1)
    for i in range(len(ring)):
        cost += mat1[ring[i] - 1][ring[i - 1] - 1]

    # Coûts liés aux dépôts (Matrice 2)
    for i in range(len(star)):
        cost += mat2[star[i][0] - 1][star[i][1] - 1]

    return cost


def OptimizedCost(data, val):

    mat1, mat2 = data[1], data[2]

    if type(val) == list:  # Ring (Matrice 1)

        output = []
        if len(val) < 3:
            output = val
        else:
            output.append(val[0])
            index = 0
            for i in range(len(val) - 1):
                verif = output[i]
                val.pop(index)
                temp = float("inf")
                for j in range(len(val)):
                    cost = mat1[verif - 1][val[j] - 1]
                    if cost < temp:
                        temp = cost
                        s = val[j]
                        index = j
                output.append(s)

    else:  # Star (Matrice 2)

        ring = data[3]
        temp = float("inf")
        for s in ring:
            cost = mat2[s - 1][val]
            if cost < temp:
                temp = cost
                output = s

    return output


# Solution initiale
def InitSol(data):

    N = data[0]

    # Ring aléatoire optimisé
    x = random.randint(1, N)
    ring = [1]
    i = 1
    while i < x:
        s = random.randint(2, N)
        if ring.count(s) == 0:
            ring.append(s)
            i += 1
    ring = OptimizedCost(data, ring)

    # Dépôts au coût optimal
    star = []
    newdata = data + [ring]
    for i in range(N):
        if ring.count(i + 1) == 0:
            star_i = OptimizedCost(newdata, i)
            star.append((i + 1, star_i))

    sol = [ring, star]
    cost = CalculCost(data, sol)
    sol.append(cost)

    return sol


def IS_Iterate(data, N):

    temp = float("inf")
    for _ in range(N):
        sol = InitSol(data)
        cost = sol[2]
        if cost < temp:
            temp = cost
            save = sol.copy()

    return save


def BestNeighbor(data, sol, choice):

    mat1 = data[1]
    ring, initcost = sol[0], sol[2]
    cost = initcost

    # Inversion
    if choice == 1:
        index = -2
        # Permutation de l'élément i du ring avec son précédant
        for i in range(len(ring)):
            if i == len(ring) - 1:
                i = -1
            beforecost = (
                mat1[ring[i] - 1][ring[i + 1] - 1]
                + mat1[ring[i - 1] - 1][ring[i - 2] - 1]
            )
            aftercost = (
                mat1[ring[i] - 1][ring[i - 2] - 1]
                + mat1[ring[i - 1] - 1][ring[i + 1] - 1]
            )
            new_cost = initcost - beforecost + aftercost
            if new_cost < cost:
                index, cost = i, new_cost

        if index > -2:
            ring[index], ring[index - 1] = ring[index - 1], ring[index]
            sol[2] = cost
        else:
            a = random.randint(0, len(ring) - 1)
            ring[a], ring[a - 1] = ring[a - 1], ring[a]
            cost = CalculCost(data, sol)
            sol[2] = cost

    # Transposition
    elif choice == 2:
        index_i = -1
        # Permutation de l'élément i du ring avec tous les suivants
        for i in range(len(ring) - 1):
            for j in range(i + 1, len(ring)):
                if j == len(ring) - 1:
                    j = -1
                beforecost = (
                    mat1[ring[i] - 1][ring[i - 1] - 1]
                    + mat1[ring[i] - 1][ring[i + 1] - 1]
                )
                beforecost += (
                    mat1[ring[j] - 1][ring[j - 1] - 1]
                    + mat1[ring[j] - 1][ring[j + 1] - 1]
                )
                newring = ring.copy()
                newring[i], newring[j] = newring[j], newring[i]
                aftercost = (
                    mat1[newring[i] - 1][newring[i - 1] - 1]
                    + mat1[newring[i] - 1][newring[i + 1] - 1]
                )
                aftercost += (
                    mat1[newring[j] - 1][newring[j - 1] - 1]
                    + mat1[newring[j] - 1][newring[j + 1] - 1]
                )
                new_cost = initcost - beforecost + aftercost
                if new_cost < cost:
                    index_i, index_j, cost = i, j, new_cost

        if index_i > -1:
            ring[index_i], ring[index_j] = ring[index_j], ring[index_i]
            sol[2] = cost
        else:
            a = random.randint(0, len(ring) - 2)
            b = random.randint(a + 1, len(ring) - 1)
            ring[a], ring[b] = ring[b], ring[a]
            cost = CalculCost(data, sol)
            sol[2] = cost

    # Déplacement
    elif choice == 3:
        index_i = -2
        index_j = -2
        # Déplacement de l'élément i du ring avec chaque groupe d'éléments suivants
        for i in range(len(ring)):
            if i == len(ring) - 1:
                i = -1
            for j in range(len(ring)):
                if j == len(ring) - 1:
                    j = -1
                # Cas où le déplacement a déjà été fait
                if i == j or i - 1 == j or (i == -1 and j == 0):
                    continue
                # Cas où le déplacement se fait à l'envers
                if (j < i and j > -1) or i == -1:
                    beforecost = (
                        mat1[ring[i] - 1][ring[i - 1] - 1]
                        + mat1[ring[i] - 1][ring[i + 1] - 1]
                    )
                    beforecost += mat1[ring[j] - 1][ring[j - 1] - 1]
                    newring = ring.copy()
                    if i == -1:
                        newring[j], newring[j + 1 :] = newring[i], newring[j:i]
                    else:
                        newring[j], newring[j + 1 : i + 1] = newring[i], newring[j:i]
                    aftercost = mat1[newring[i] - 1][newring[i + 1] - 1]
                    aftercost += (
                        mat1[newring[j] - 1][newring[j - 1] - 1]
                        + mat1[newring[j] - 1][newring[j + 1] - 1]
                    )
                # Cas où le déplacement se fait vers l'avant
                else:
                    beforecost = (
                        mat1[ring[i] - 1][ring[i - 1] - 1]
                        + mat1[ring[i] - 1][ring[i + 1] - 1]
                    )
                    beforecost += mat1[ring[j] - 1][ring[j + 1] - 1]
                    newring = ring.copy()
                    if j == -1:
                        newring[j], newring[i:j] = newring[i], newring[i + 1 :]
                    else:
                        newring[j], newring[i:j] = newring[i], newring[i + 1 : j + 1]
                    aftercost = mat1[newring[i] - 1][newring[i - 1] - 1]
                    aftercost += (
                        mat1[newring[j] - 1][newring[j - 1] - 1]
                        + mat1[newring[j] - 1][newring[j + 1] - 1]
                    )

                new_cost = initcost - beforecost + aftercost
                if new_cost < cost:
                    index_i, index_j, cost = i, j, new_cost

        if (index_j < index_i and index_j > -1) or index_i == -1:
            if index_i == -1:
                ring[index_j], ring[index_j + 1 :] = (
                    ring[index_i],
                    ring[index_j:index_i],
                )
            else:
                ring[index_j], ring[index_j + 1 : index_i + 1] = (
                    ring[index_i],
                    ring[index_j:index_i],
                )
            sol[2] = cost
        else:
            if index_j == -1:
                ring[index_j], ring[index_i:index_j] = (
                    ring[index_i],
                    ring[index_i + 1 :],
                )
            else:
                ring[index_j], ring[index_i:index_j] = (
                    ring[index_i],
                    ring[index_i + 1 : index_j + 1],
                )
            sol[2] = cost

    return sol


def TabuNeighbors(data, sol, choice):

    S = []
    mat1 = data[1]
    ring = sol[0]
    initcost = sol[2]

    # 1. Inversion (Swap adjacent)
    if choice == 1:
        for i in range(len(ring)):
            if i == len(ring) - 1:
                i = -1

            beforecost = (
                mat1[ring[i] - 1][ring[i + 1] - 1]
                + mat1[ring[i - 1] - 1][ring[i - 2] - 1]
            )
            aftercost = (
                mat1[ring[i] - 1][ring[i - 2] - 1]
                + mat1[ring[i - 1] - 1][ring[i + 1] - 1]
            )
            new_cost = initcost - beforecost + aftercost

            newring = ring.copy()
            newring[i], newring[i - 1] = newring[i - 1], newring[i]

            # On ajoute le voisin à la liste
            S.append([newring, sol[1], new_cost])

    # 2. Transposition (Swap général)
    elif choice == 2:
        for i in range(len(ring) - 1):
            for j in range(i + 1, len(ring)):
                if j == len(ring) - 1:
                    j = -1

                beforecost = (
                    mat1[ring[i] - 1][ring[i - 1] - 1]
                    + mat1[ring[i] - 1][ring[i + 1] - 1]
                )
                beforecost += (
                    mat1[ring[j] - 1][ring[j - 1] - 1]
                    + mat1[ring[j] - 1][ring[j + 1] - 1]
                )

                newring = ring.copy()
                newring[i], newring[j] = newring[j], newring[i]

                aftercost = (
                    mat1[newring[i] - 1][newring[i - 1] - 1]
                    + mat1[newring[i] - 1][newring[i + 1] - 1]
                )
                aftercost += (
                    mat1[newring[j] - 1][newring[j - 1] - 1]
                    + mat1[newring[j] - 1][newring[j + 1] - 1]
                )

                new_cost = initcost - beforecost + aftercost
                S.append([newring, sol[1], new_cost])

    # 3. Déplacement (Insertion)
    elif choice == 3:
        # Déplacement de l'élément i vers la position j
        for i in range(len(ring)):
            if i == len(ring) - 1:
                i = -1
            for j in range(len(ring)):
                if j == len(ring) - 1:
                    j = -1

                # Cas interdits (déplacement sur soi-même ou équivalent)
                if i == j or i - 1 == j or (i == -1 and j == 0):
                    continue

                # Cas A : Le déplacement se fait "vers l'arrière" ou cas spécial fin de liste
                if (j < i and j > -1) or i == -1:
                    beforecost = (
                        mat1[ring[i] - 1][ring[i - 1] - 1]
                        + mat1[ring[i] - 1][ring[i + 1] - 1]
                    )
                    beforecost += mat1[ring[j] - 1][ring[j - 1] - 1]

                    newring = ring.copy()
                    # Logique de slicing python pour l'insertion
                    if i == -1:
                        newring[j], newring[j + 1 :] = newring[i], newring[j:i]
                    else:
                        newring[j], newring[j + 1 : i + 1] = newring[i], newring[j:i]

                    aftercost = mat1[newring[i] - 1][newring[i + 1] - 1]
                    aftercost += (
                        mat1[newring[j] - 1][newring[j - 1] - 1]
                        + mat1[newring[j] - 1][newring[j + 1] - 1]
                    )

                # Cas B : Le déplacement se fait "vers l'avant"
                else:
                    beforecost = (
                        mat1[ring[i] - 1][ring[i - 1] - 1]
                        + mat1[ring[i] - 1][ring[i + 1] - 1]
                    )
                    beforecost += mat1[ring[j] - 1][ring[j + 1] - 1]

                    newring = ring.copy()
                    if j == -1:
                        newring[j], newring[i:j] = newring[i], newring[i + 1 :]
                    else:
                        newring[j], newring[i:j] = newring[i], newring[i + 1 : j + 1]

                    aftercost = mat1[newring[i] - 1][newring[i - 1] - 1]
                    aftercost += (
                        mat1[newring[j] - 1][newring[j - 1] - 1]
                        + mat1[newring[j] - 1][newring[j + 1] - 1]
                    )

                new_cost = initcost - beforecost + aftercost

                S.append([newring, sol[1], new_cost])

    return S


def FindMin(L):

    cost = float("inf")
    for i in range(len(L)):
        if L[i][2] < cost:
            index = i
            cost = L[i][2]

    return L[index], index
