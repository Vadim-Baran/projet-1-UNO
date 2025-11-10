import random

# ------------------------------
# Définition des cartes UNO
# ------------------------------

couleurs = ["Rouge", "Jaune", "Vert", "Bleu"]
valeurs = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Inversion", "Saut", "+2"]
speciales = ["Joker", "+4"]

def creer_paquet():
    paquet = []
    for c in couleurs:
        for v in valeurs:
            paquet.append((c, v))
            if v != "0":
                paquet.append((c, v))
    for s in speciales:
        paquet += [("Noir", s)] * 4
    random.shuffle(paquet)
    return paquet

# ------------------------------
# Fonctions utilitaires
# ------------------------------

def carte_valide(carte, carte_sommet):
    c1, v1 = carte
    c2, v2 = carte_sommet
    return c1 == c2 or v1 == v2 or c1 == "Noir"

def afficher_main(main):
    return ", ".join([f"{i+1}:{c[0]} {c[1]}" for i, c in enumerate(main)])

# ------------------------------
# Jeu principal
# ------------------------------

def jouer_uno():
    nb_joueurs = int(input("Combien de joueurs ? (2-4) : "))
    paquet = creer_paquet()
    mains = [[paquet.pop() for _ in range(7)] for _ in range(nb_joueurs)]
    pile = [paquet.pop()]

    sens = 1
    joueur_actuel = 0

    while True:
        carte_sommet = pile[-1]
        print(f"\nCarte sur la pile : {carte_sommet[0]} {carte_sommet[1]}")
        print(f"Main du joueur {joueur_actuel+1} : {afficher_main(mains[joueur_actuel])}")

        main = mains[joueur_actuel]
        coups_possibles = [c for c in main if carte_valide(c, carte_sommet)]

        if not coups_possibles:
            print("Aucune carte valide, vous piochez.")
            if paquet:
                main.append(paquet.pop())
            else:
                print("Le paquet est vide ! Fin du jeu.")
                break
        else:
            # Choix automatique (tu peux le remplacer par input)
            carte = random.choice(coups_possibles)
            print(f"Le joueur {joueur_actuel+1} joue : {carte[0]} {carte[1]}")
            main.remove(carte)
            pile.append(carte)

            # Effets des cartes spéciales
            if carte[1] == "Inversion":
                sens *= -1
            elif carte[1] == "Saut":
                joueur_actuel = (joueur_actuel + sens) % nb_joueurs
            elif carte[1] == "+2":
                cible = (joueur_actuel + sens) % nb_joueurs
                for _ in range(2):
                    mains[cible].append(paquet.pop())
                print(f"Le joueur {cible+1} pioche 2 cartes !")
            elif carte[1] == "+4":
                cible = (joueur_actuel + sens) % nb_joueurs
                for _ in range(4):
                    mains[cible].append(paquet.pop())
                print(f"Le joueur {cible+1} pioche 4 cartes !")
                nouvelle_couleur = random.choice(couleurs)
                pile[-1] = (nouvelle_couleur, carte[1])
                print(f"Le joueur {joueur_actuel+1} change la couleur en {nouvelle_couleur}")
            elif carte[1] == "Joker":
                nouvelle_couleur = random.choice(couleurs)
                pile[-1] = (nouvelle_couleur, carte[1])
                print(f"Le joueur {joueur_actuel+1} change la couleur en {nouvelle_couleur}")

        # Vérification de la victoire
        if not main:
            print(f"\n🎉 Le joueur {joueur_actuel+1} a gagné ! 🎉")
            break

        joueur_actuel = (joueur_actuel + sens) % nb_joueurs

if __name__ == "__main__":
    jouer_uno()
