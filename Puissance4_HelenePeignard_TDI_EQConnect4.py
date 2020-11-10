#Code de Thomas Broun,Juliette Mahieu, Julie Mordacq et Hélène Peignard 

import math

#Nos variables globales
profondeurMax = 5
ordiJoue = True
nbCoup = 0

#Classe grille, permet de faire l'algorithme alpha beta, en observant toutes les versions possibles (a une certaine profondeurMax) au lieu de faire une liste
#La grille est une liste de 'largeur' sous-liste. Ces sous-listes représentent les colonnes, elles sont vides de base et se remplissent au fur et à mesure que les points sont posés
class GrilleClasse(object):
    hauteur = 6
    largeur = 12

    #constructeur
    def __init__(self, ACopier=None):
        #si un parametre ACopier à été envoyé, on crée un copie de l'instance grille (cela permet d'explorer toutes les possibilités sans modifier la grille finale)
        if(ACopier):
            self.grille = [list(col) for col in ACopier.grille]

        #si on ne demande pas une copie d'une instance, alors on veut creer une grille de zero
        else:
            self.grille = [[] for x in range(self.largeur)]

    #renvoie une liste de tous les coups possibles (un coup est sous la forme (a,b), a etant l'indice de la colonne, et b l'icone à jouer (1 ou 0))
    def CoupsPossibles(self, ordiJoue):
        listCoupsPossibles = []
        for i in range(self.largeur):
            #Regarde si on peut encore remplir la colonne (c'est à dire si il reste des cases vides vers le haut)
            if len(self.grille[i]) < self.hauteur:
                child = GrilleClasse(self)
                #jouer l'icone appropiée (1 ou 0) à un indice demandé dans l'instance grille
                icone = -1
                if ordiJoue:
                    icone = 0
                else:
                    icone = 1
                child.grille[i].append(icone)
                listCoupsPossibles.append((i, child))
        return listCoupsPossibles

    #Renvoit -1 si le jeu n'est pas fini, 0 s'il y a egalité, 1 si un des joueurs a gagné
    def TerminalTest(self):
        Xmax = self.largeur
        grille = self.grille
        for i in range(Xmax):
            for j in range(self.hauteur):
                #horizontale
                if i + 3 < Xmax and len(grille[i]) > j and len(grille[i+1]) > j and len(grille[i+2]) > j and len(grille[i+3]) > j:
                    if grille[i][j]  == grille[i+1][j] == grille[i+2][j] == grille[i+3][j]:
                        return 1
                #verticale
                if len(grille[i]) > j + 3:
                    if grille[i][j]  == grille[i][j+1] == grille[i][j+2] == grille[i][j+3]:
                        return 1
                #diagonale bas gauche, haut droite
                if i + 3 < Xmax and len(grille[i]) > j and len(grille[i + 1]) > j + 1 and len(grille[i + 2]) > j + 2 and len(grille[i + 3]) > j + 3:
                    if not j + 3 > self.hauteur and grille[i][j] == grille[i+1][j + 1] == grille[i+2][j + 2] == grille[i+3][j + 3]:
                        return 1
                #diagonale bas droite, haut gauche
                if i + 3 < Xmax and len(grille[i]) > j and len(grille[i + 1]) > j - 1 and len(grille[i + 2]) > j - 2 and len(grille[i + 3]) > j - 3:
                    if not j - 3 < 0 and grille[i][j] == grille[i+1][j - 1] == grille[i+2][j - 2] == grille[i+3][j - 3]:
                        return 1
        #Dit il n'y a plus de jeton à piocher (et donc la partie est finie) ou non
        if nbCoup == 42:
            return 0
        return -1

#Cette fonction est appelée avant le balayage alpha beta, elle permet de voir s'i'l n'y a pas une action urgente à faire, avant de jouer avec l'alpha beta
#Elle fonctionne par ordre de priorité. D'abord chercher s'il n'y a pas un coup qui peut immédiatement donner la victoire
#Ensuite cherche s'il n'y a pas un piège à déjouer (quand l'adversaire aligne deux points en ligne avec deux cases vides autour par exemple)
#Si les deux premiers cas ne sont pas vérifier, chercher si l'adversaire ne va pas gagner dans le prochain coup, et on le bloque
#Finalement si aucun de ces cas est dans la grille, VerifieVictoire renvoit -1 et le code va dans alpha beta après (voir la fonction Jeu pour l'ordre des choses)
def VerifieVictoire(grilleInst):
    grille = grilleInst.grille
    Xmax = grilleInst.largeur
    Ymax = grilleInst.hauteur
    for i in range(Xmax-1, -1, -1):
        for j in range(Ymax):
            indice = -1
            #Puisque les colonnnes de la grille sont vide avant d'être remplie, et pas remplie d'un espace par exemple, les tests sont pas grille[i][j] ==  ' ' par exemple, mais voila leurs équivalents
            #(len(grille[i]) <= j) signifie (case == vide), (len(grille[i]) > j) signifie (case != vide), (len(grille[i]) == j) signifie (case vide + case dessous pleine)
            #horizontale
            if i-2 >= 0 and len(grille[i]) > j and len(grille[i - 1]) > j and len(grille[i-2]) > j:
                if grille[i][j] == grille[i-1][j] == grille[i-2][j]:
                    if i+1 < Xmax and len(grille[i+1]) <= j: #s'il peut poser cote droit et gagner 
                        if len(grille[i+1]) > j-1 or j == 0: #regarde si la case d'en dessous est pleine, ou si on veut poser sur la premiere ligne
                            if (ordiJoue and grille[i][j] == 0) or (not ordiJoue and grille[i][j] == 1): #victoire
                                return (i+1)
                            else:
                                indice = i+1 #le garde en reserve mais regarde d'abord si on peut gagner
                    if i-3 >= 0 and len(grille[i-3]) <= j : #si il peut poser cote gauche et gagner 
                        if len(grille[i-3]) > j-1 or j == 0: #regarde si la case d'en dessous est pleine, ou si on veut poser sur la premiere ligne
                            if (ordiJoue and grille[i][j] == 0) or (not ordiJoue and grille[i][j] == 1): #victoire
                                return (i-3)
                            else:
                                indice = i-3
            #verticale
            if len(grille[i]) == j + 3: #len(grille[i]) > j + 2 and len(grille[i]) <= j + 3
                if grille[i][j] == grille[i][j + 1] == grille[i][j + 2]:
                    if (ordiJoue and grille[i][j] == 0) or (not ordiJoue and grille[i][j] == 1): #victoire
                        return (i)
                    else:
                        indice = i
            #diagonale d'en bas droite à haut gauche
            if i - 2 >= 0 and j + 2 < Ymax and len(grille[i]) > j and len(grille[i - 1]) > j + 1 and len(grille[i - 2]) > j + 2:
                if grille[i][j] == grille[i - 1][j + 1] == grille[i - 2][j + 2]:
                    if j + 3 < Ymax and i - 3 >= 0 and len(grille[i-3]) == j+3: #si on peut poser en haut à gauche et gagner (regarde pas que si la case d'en dessous et pleine, car pas possible que ce soit la première ligne)
                        if (ordiJoue and grille[i][j] == 0) or (not ordiJoue and grille[i][j] == 1): #victoire
                            return (i-3)
                        else:
                            indice = i-3
                    if j-1 >= 0 and i+1<Xmax and len(grille[i+1]) <= j-1 : #si on peut poser en bas à droite et gagner
                        #regarde si la case d'en dessous est pleine, ou si on veut poser sur la premiere ligne
                        if (j-2 >= 0 and len(grille[i+1]) > j-2) or (j-1 == 0):
                            if (ordiJoue and grille[i][j] == 0) or (not ordiJoue and grille[i][j] == 1): #victoire
                                return (i+1)
                            else:
                                indice = i+1
            #diagonale d'en bas droite à haut gauche avec un trou deuxieme case
            if i - 3 >= 0 and j + 3 < Ymax and len(grille[i]) > j and len(grille[i - 2]) > j + 2 and len(grille[i - 3]) > j + 3 :
                if grille[i][j] == grille[i - 3][j + 3] == grille[i - 2][j + 2]:
                    if len(grille[i-1]) == j+1: #si on peut poser dans la case vide au milieu de la diagonale et gagner (regarde pas que si la case d'en dessous et pleine, car pas possible que ce soit la première ligne)
                        if (ordiJoue and grille[i][j] == 0) or (not ordiJoue and grille[i][j] == 1): #victoire
                            return (i-1)
                        else:
                            indice = i-1
            #diagonale d'en bas droite à haut gauche avec un trou troisieme case
            if i - 3 >= 0 and j + 3 < Ymax and len(grille[i]) > j and len(grille[i - 1]) > j + 1 and len(grille[i - 3]) > j + 3 :
                if grille[i][j] == grille[i - 1][j + 1] == grille[i - 3][j + 3]:
                    if len(grille[i-2]) == j+2: #si on peut poser dans la case vide au milieu de la diagonale et gagner (regarde pas que si la case d'en dessous et pleine, car pas possible que ce soit la première ligne)
                        if (ordiJoue and grille[i][j] == 0) or (not ordiJoue and grille[i][j] == 1): #victoire
                            return (i-2)
                        else:
                            indice = i-2
            #diagonale d'en bas gauche à haut droite
            if i-2 >= 0 and j-2 >= 0 and len(grille[i]) > j and len(grille[i - 1]) > j - 1 and len(grille[i - 2]) > j - 2:
                if grille[i][j] == grille[i-1][j - 1] == grille[i-2][j - 2]:
                    if i-3 >= 0 and j-3 >= 0 and len(grille[i-3]) <= j-3 :
                        if (j-4 >= 0 and len(grille[i-3]) > j-4) or (j - 3 == 0): #pose en bas à gauche
                            if (ordiJoue and grille[i][j] == 0) or (not ordiJoue and grille[i][j] == 1): #victoire
                                return (i-3)
                            else:
                                indice = i-3
                    if i+1 < Xmax and j+1 < Ymax and len(grille[i+1])== j+1: #pose en haut à droite
                        if (ordiJoue and grille[i][j] == 0) or (not ordiJoue and grille[i][j] == 1): #victoire
                                return (i+1)
                        else:
                            indice = i+1
            #diagonale d'en bas gauche à haut droite avec deuxieme case vide
            if i-3 >= 0 and j-3 >= 0 and len(grille[i]) > j and len(grille[i - 2]) > j - 2 and len(grille[i - 3]) > j - 3 :
                if grille[i][j] == grille[i-2][j - 2] == grille[i-3][j - 3]:
                    if len(grille[i-1]) == j-1 :#regarde si peut poser à la bonne hauteur
                            if (ordiJoue and grille[i][j] == 0) or (not ordiJoue and grille[i][j] == 1): #victoire
                                return (i-1)
                            else:
                                indice = i-1
            #diagonale d'en bas gauche à haut droite avec troisieme case vide
            if i-3 >= 0 and j-3 >= 0 and len(grille[i]) > j and len(grille[i - 1]) > j - 1 and len(grille[i - 3]) > j - 3 :
                if grille[i][j] == grille[i-1][j - 1] == grille[i-3][j - 3]:
                    if len(grille[i-2]) == j-2 :#regarde si peut poser à la bonne hauteur
                            if (ordiJoue and grille[i][j] == 0) or (not ordiJoue and grille[i][j] == 1): #victoire
                                return (i-2)
                            else:
                                indice = i-2
            #S'il y a aucune victoire imminente possible, ni pour l'adversaire, ni pour le joueur, on essaye de déjouer les 'pièges' du à déjouer
            if indice == -1:
                #horizontale : deux alignés avec des cases vides de chaque coté (car veut déjouer ce piege)
                if i-1 >= 0 and len(grille[i]) > j and len(grille[i - 1]) > j:
                    if grille[i][j] == grille[i-1][j]:
                        if i+1 < Xmax and len(grille[i+1]) <= j  and (len(grille[i+1]) > j-1 or j == 0) and i-2 >= 0 and len(grille[i-2]) <= j and (len(grille[i-2]) > j-1 or j == 0): #si il peut poser cote droit ou à gauche (il y a un piège à déjouer)
                            if (not ordiJoue and grille[i][j] == 0) or (ordiJoue and grille[i][j] == 1): #piege à déjouer : à droite
                                return (i+1)
                            if (not ordiJoue and grille[i][j] == 0) or (ordiJoue and grille[i][j] == 1): #piege à déjouer : à gauche
                                return (i-2)
                #horizontale : une case remplie, puis une vide, puis une remplie, avec au moins une case vide d'un coté (car veut déjouer ce piege aussi)
                if i-2 >= 0 and len(grille[i]) > j and len(grille[i-2]) > j:
                    if grille[i][j] == grille[i-2][j] and len(grille[i-1]) <= j: #si les deux cases sont pareilles, et que celle du milieu est vide
                        if (i+1 < Xmax and len(grille[i+1]) <= j and (len(grille[i+1]) > j-1 or j == 0)) or (i-3 >= 0 and len(grille[i-3]) <= j and (len(grille[i-3]) > j-1 or j == 0)): #si il peut poser cote droit et nous pieger, ou à gauche et nous pieger
                            if len(grille[i-1]) > j-1 or j == 0: #regarde si non vide ou premiere ligne
                                if (not ordiJoue and grille[i][j] == 0) or (ordiJoue and grille[i][j] == 1): #piege à déjouer : pose au milieu
                                    return (i-1)
            if indice != -1:
                return indice
    return indice

#attribut un score en fonction de tout ce qui trouve dans le tableau,
#plus c'est favorable au joueur en cours plus le score final est positif, plus c'est favorable à l'aversaire plus c'est negatif
#plus le score est proche de zero moins ca aura d'impacte
def Heuristique(grilleInst):
    heuristique = 0
    grille = grilleInst.grille
    Xmax = grilleInst.largeur
    Ymax = grilleInst.hauteur
    #on parcout la grille à partir de en bas à gauche 
    for i in range(Xmax-1, -1, -1):
        for j in range(Ymax):
            #alignements horizontaux
            #si y'en a potentiellement 2 alignés
            if i - 1 >= 0 and len(grille[i]) > j and len(grille[i - 1]) > j:
                if grille[i][j] == grille[i - 1][j] == 0:
                    heuristique += 2
                if grille[i][j] == grille[i - 1][j] == 1:
                    heuristique -= 1
                #si y'en a potentiellement 3 alignés
                if i - 2 >= 0 and len(grille[i-2]) > j:
                    if grille[i][j] == grille[i - 1][j] == grille[i - 2][j] == 0:
                        heuristique += 3
                    if grille[i][j] == grille[i - 1][j] == grille[i - 2][j] == 1:
                        heuristique -= 2
                    #si y'en a potentiellement 4 alignés
                    if i - 3 >= 0 and len(grille[i-3]) > j:
                        if grille[i][j] == grille[i-1][j] == grille[i-2][j] == grille[i-3][j] == 0:
                            heuristique += 6
                        if grille[i][j] == grille[i-1][j] == grille[i-2][j] == grille[i-3][j] == 1:
                            heuristique -= 5
            #alignements verticaux 
            if len(grille[i]) > j + 1:
                #on test s'il y en a potentiellement 2, puis 3, puis 4 alignés et modifie le score de l'heuristique en fonction
                if grille[i][j] == grille[i][j + 1] == 0:
                    heuristique += 1
                if grille[i][j] == grille[i][j + 1] == 1:
                    heuristique -= 1
                if len(grille[i]) > j + 2:
                    if grille[i][j] == grille[i][j + 1] == grille[i][j + 2] == 0:
                        heuristique += 2
                    if grille[i][j] == grille[i][j + 1] == grille[i][j + 2] == 1:
                        heuristique -= 2
                    if len(grille[i]) > j + 3:
                        if grille[i][j] == grille[i][j+1] == grille[i][j+2] == grille[i][j+3] == 0:
                            heuristique += 5
                        if grille[i][j] == grille[i][j+1] == grille[i][j+2] == grille[i][j+3] == 1:
                            heuristique -= 5
            #alignements diagonaux de en bas à droite à en haut à gauche (on test pour 2, 3 et 4)
            if i - 1 >= 0 and j+1 < Ymax and len(grille[i]) > j and len(grille[i - 1]) > j + 1:
                if grille[i][j] == grille[i- 1][j + 1] == 0:
                    heuristique += 1
                if i - 2 >= 0  and j+2 < Ymax and len(grille[i - 2]) > j + 2:
                    if grille[i][j] == grille[i - 1][j + 1] == grille[i - 2][j + 2] == 0:
                        heuristique += 1
                    if grille[i][j] == grille[i - 1][j + 1] == grille[i - 2][j + 2] == 1:
                        heuristique -= 1
                    if i - 3 >= 0  and j+3 < Ymax and len(grille[i - 3]) > j + 3:
                        if grille[i][j] == grille[i-1][j + 1] == grille[i-2][j + 2] == grille[i-3][j + 3] == 0:
                            heuristique += 4
                        if grille[i][j] == grille[i-1][j + 1] == grille[i-2][j + 2] == grille[i-3][j + 3] == 1:
                            heuristique -= 4
            #alignements diagonaux de en bas à gauche à en haut à droite (on test pour 2, 3 et 4)
            if i - 1 >= 0  and j-1 >=0 and len(grille[i]) > j and len(grille[i - 1]) > j - 1:
                if grille[i][j] == grille[i-1][j - 1] == 0:
                    heuristique += 1
                if i - 2 >= 0 and j-2 >=0 and len(grille[i - 2]) > j - 2:
                    if grille[i][j] == grille[i-1][j - 1] == grille[i-2][j - 2] == 0:
                        heuristique += 1
                    if grille[i][j] == grille[i-1][j - 1] == grille[i-2][j - 2] == 1:
                        heuristique -= 1
                    if i - 3 >= 0 and j-3 >=0 and len(grille[i - 3]) > j - 3:
                        if grille[i][j] == grille[i-1][j - 1] == grille[i-2][j - 2] == grille[i-3][j - 3] == 0:
                            heuristique += 4
                        if grille[i][j] == grille[i-1][j - 1] == grille[i-2][j - 2] == grille[i-3][j - 3] == 1:
                            heuristique -= 4
    return heuristique #on retourne l'utilité finale de l'action

#trouve le meilleur indice de colonne où poser le pion de l'ordinateur
def AlphaBeta(grilleInst, profondeur, ordiJoue, alpha, beta):
    if nbCoup == 42:
        return -math.inf if ordiJoue else math.inf, -1
    elif profondeur == 0:
        return Heuristique(grilleInst), -1
    #initialise le meilleur score au minimum (ou maximum) en fonction du joueur qui joue
    if ordiJoue:
        meilleurHeuri = -math.inf
    else:
        meilleurHeuri = math.inf
    meilleurIndice = -1
    #cherche tous les coups possibles puis pour chaque possibilité calcule son heuristique et les compare toutes à la fin
    listCoupsPossibles = grilleInst.CoupsPossibles(ordiJoue)
    #on parcourt en partant du milieu 
    moitie = (int)(len(listCoupsPossibles) / 2)
    for i in range(moitie-1, -1, -1):
        childInst = listCoupsPossibles[i]
        indice, childgrille = childInst
        #on diminue la profondeur de 1 à chaque fois (car on remonte dans les possibilités)
        #on change de joueur à chaque tour (pour simuler une vraie partie)
        temp = AlphaBeta(childgrille, profondeur-1, not ordiJoue, alpha, beta)[0]
        if (temp > meilleurHeuri and ordiJoue) or (temp < meilleurHeuri and not ordiJoue):
            meilleurHeuri = temp
            meilleurIndice = indice
        if ordiJoue:
            alpha = max(alpha, temp)
        else:
            beta = min(beta, temp)
        #on coupe la branche
        if alpha >= beta:
            break
    #on parcourt l'autre moitié
    for i in range(moitie, len(listCoupsPossibles)):
        childInst = listCoupsPossibles[i]
        indice, childgrille = childInst
        #on diminue la profondeur de 1 à chaque fois (car on remonte dans les possibilités)
        #on change de joueur à chaque tour (pour simuler une vraie partie)
        temp = AlphaBeta(childgrille, profondeur-1, not ordiJoue, alpha, beta)[0]
        if (temp > meilleurHeuri and ordiJoue) or (temp < meilleurHeuri and not ordiJoue):
            meilleurHeuri = temp
            meilleurIndice = indice
        if ordiJoue:
            alpha = max(alpha, temp)
        else:
            beta = min(beta, temp)
        #on coupe la branche
        if alpha >= beta:
            break    
    return meilleurHeuri, meilleurIndice #on retourne l'action qui a la meilleure utilité

#retourne l'indice de colonne choisit pas l'utilisateur
def IndicePlayer(grilleInst):
    reponse = -1
    reponse = eval(input("Indiquez l'indice auquel vous voulez jouer : "))
    #on vérifie que l'indice choisit existe dans la grille
    while grilleInst.largeur < reponse or reponse < 1:
        reponse = eval(input("Echec... Veuillez choisir parmis les nombres proposés en dessous du tableau : "))
    return reponse -1


#retourne le meilleur indice de colonne ou poser le pion de l'ordinateur
def IndiceOrdi(grilleInst):
    return AlphaBeta(grilleInst, profondeurMax, ordiJoue, -math.inf, math.inf)[1] #le premiere parametre est le score max de l'heuristique, mais nous on veut que le deuxieme -> l'indice ou placer le piont

#affiche la grille avec un affichage dynamique
def Afficher(grilleInst):
    print()
    #on part de la fin car on veut afficher de bas en haut or la console fonction de haut en bas
    for i in range(grilleInst.hauteur - 1, -1, -1):
        print("-", "----" * grilleInst.largeur, sep ='')
        print("|", end='')
        for j in range(grilleInst.largeur):
            if len(grilleInst.grille[j]) > i:
                icone = grilleInst.grille[j][i]
                #on met les symboles correspondant à 0, 1
                iconeForm = 'O'
                if icone == 0:
                    iconeForm = 'X'
                print(" " + iconeForm + " ", end = '')
            else:
                print("   ", end="")
            print("|", end="")
        print()
    print("-", "----" * grilleInst.largeur, sep ='')
    print("  ", end ='')
    for i in range(1, grilleInst.largeur +1):
        print(i,"  " if i < 10 else " ", end='')
    print(end = '\n\n')
    

#lance la partie et alterne les joueurs jusqu'a victoire ou nombre de pions max atteint 
def Jeu():
    global ordiJoue, nbCoup
    reponseValide = False
    #demande qui va joueur en premier 
    print("Qui joue en premier ?")
    print("Entrez '1' pour l'ordinateur")
    print("Entrez '2' pour le joueur réél")
    while(not reponseValide):
        choix = int(input('> '))
        if choix == 1:
            reponseValide = True
            ordiJoue = True
        elif choix == 2:
            reponseValide = True
            ordiJoue = False
        else:
            print("Veuillez entrer soit 1, soit 2")
    
    grilleInst = GrilleClasse()
    #le joueur correspond à 1 et le bot à 0
    Afficher(grilleInst)
    FinJeu = False
    while(not FinJeu):
        if ordiJoue:
            nomJoueur = "L'ordinateur"
            move = VerifieVictoire(grilleInst)
            #si on ne peut pas gagner immediatement
            if move == -1:
                move = IndiceOrdi(grilleInst)
        else:
            nomJoueur = "Le joueur réel"
            move = IndicePlayer(grilleInst)

        #place le pion
        icone = -1
        if ordiJoue:
            icone = 0
        else:
            icone = 1
        grilleInst.grille[move].append(icone)
        Afficher(grilleInst)
        nbCoup = nbCoup +1
        print(nomJoueur, " a joué à l'indice : ", move + 1, "\nNombre de coups total : ", nbCoup)

        #determine si le Jeu est fini ou non 
        isOver = grilleInst.TerminalTest()
        if isOver == 0:
            print("Il n'y a plus de jetons dans la pioche, personne n'a gagné")
            FinJeu = True
        elif isOver == 1:
            print(nomJoueur + " a gagné !")
            FinJeu = True
        else:
            #c'est à l'autre joueur de jouer
            ordiJoue = not ordiJoue



if __name__ == "__main__":
    Jeu()
