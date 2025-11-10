import random
import os
import time
from colorama import Fore, Style, init

init(autoreset=True)

# ------------------------------
# Couleurs rétro et polices
# ------------------------------

def retro(text, color=Fore.GREEN):
    return f"{color}{text}{Style.RESET_ALL}"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# ------------------------------
# Définition du jeu UNO
# ------------------------------

couleurs = ["Rouge", "Jaune", "Vert", "Bleu"]
valeurs = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Inversion", "Saut", "+2"]
speciales = ["Joker", "+4"]

couleur_texte = {
    "Rouge": Fore.RED,
    "Jaune": Fore.YELLOW,
    "Vert": Fore.GREEN,
    "Bleu": Fore.CYAN,
    "Noir": Fore.MAGENTA
}


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


def afficher_carte_ascii(carte):
    """Carte UNO style rétro ASCII"""
    c, v = carte
    col = couleur_texte[c]
    val = v.center(9)
    coul = c.center(9)
    ligne = retro("┌───────────┐", col) + "\n" + \
            retro(f"│ {val} │", col) + "\n" + \
            retro(f"│ {coul} │", col) + "\n" + \
            retro("└───────────┘", col)
    return ligne


def afficher_main(main):
    return "  ".join([f"{i+1}:{couleur_texte[c[0]]}{c[0][0]} {c[1]}{Style.RESET_ALL}" for i, c in enumerate(main)])


def reconstituer_paquet(paquet, pile):
    if not paquet:
        paquet = pile[:-1]
        random.shuffle(paquet)
        pile = [pile[-1]]
        print(retro("🔁 Reformation du paquet...", Fore.YELLOW))
    return paquet, pile


# ------------------------------
# Interface rétro
# ------------------------------

def afficher_plateau(noms, mains, pile, joueur_actuel, sens, log=""):
    clear()
    print(retro("╔══════════════════════════════════════════════════╗", Fore.CYAN))
    print(retro("║                ██████  UNO RETRO ██████          ║", Fore.CYAN))
    print(retro("╠══════════════════════════════════════════════════╣", Fore.CYAN))
    print(retro(f"║   Ordre du jeu : {'→ HORAIRE' if sens==1 else '← ANTI-HORAIRE'}{' ' * 17}║", Fore.CYAN))
    print(retro("╠══════════════════════════════════════════════════╣", Fore.CYAN))

    print(retro("║                    [PILE]                        ║", Fore.CYAN))
    carte_affiche = afficher_carte_ascii(pile[-1]).splitlines()
    for ligne in carte_affiche:
        print(retro(f"║ {ligne.ljust(48)}║", Fore.CYAN))
    print(retro("╠══════════════════════════════════════════════════╣", Fore.CYAN))

    for i, nom in enumerate(noms):
        indicateur = "▶" if i == joueur_actuel else " "
        print(retro(f"║ {indicateur} {nom.ljust(15)} | Cartes: {len(mains[i])}".ljust(49) + "║", Fore.CYAN))
    print(retro("╠══════════════════════════════════════════════════╣", Fore.CYAN))
    print(retro(f"║ {log.ljust(48)}║", Fore.CYAN))
    print(retro("╚══════════════════════════════════════════════════╝", Fore.CYAN))
    print()


# ------------------------------
# Effets de carte
# ------------------------------

def appliquer_effet(carte, joueur_actuel, mains, nb_joueurs, paquet, pile, noms, sens):
    couleur, valeur = carte

    def cible():
        return (joueur_actuel + sens) % nb_joueurs

    log = ""
    if valeur == "Inversion":
        sens *= -1
        log = "🔄 Inversion du sens"
    elif valeur == "Saut":
        log = f"⏭️ {noms[cible()]} saute son tour"
        joueur_actuel = (joueur_actuel + sens) % nb_joueurs
    elif valeur == "+2":
        paquet, pile = reconstituer_paquet(paquet, pile)
        for _ in range(2):
            mains[cible()].append(paquet.pop())
        log = f"💥 {noms[cible()]} pioche 2 cartes"
    elif valeur == "+4":
        paquet, pile = reconstituer_paquet(paquet, pile)
        for _ in range(4):
            mains[cible()].append(paquet.pop())
        nouvelle_couleur = random.choice(couleurs)
        pile[-1] = (nouvelle_couleur, valeur)
        log = f"🎨 +4 → {nouvelle_couleur}"
    elif valeur == "Joker":
        nouvelle_couleur = random.choice(couleurs)
        pile[-1] = (nouvelle_couleur, valeur)
        log = f"🎨 Joker → {nouvelle_couleur}"
    return sens, log


# ------------------------------
# Jeu principal
# ------------------------------

def jouer_uno():
    clear()
    print(retro("██████  BIENVENUE DANS UNO RETRO TERMINAL  ██████", Fore.CYAN))
    nb_joueurs = int(input(retro("Combien de joueurs au total ? (2-4): ", Fore.GREEN)))
    nb_humains = int(input(retro(f"Combien d'humains ? (1-{nb_joueurs}): ", Fore.GREEN)))

    paquet = creer_paquet()
    mains = [[paquet.pop() for _ in range(7)] for _ in range(nb_joueurs)]
    pile = [paquet.pop()]

    sens = 1
    joueur_actuel = 0
    noms = [f"🧍 Joueur {i+1}" if i < nb_humains else f"🤖 Bot {i+1}" for i in range(nb_joueurs)]
    log = "Partie lancée !"

    while True:
        afficher_plateau(noms, mains, pile, joueur_actuel, sens, log)
        main = mains[joueur_actuel]
        carte_sommet = pile[-1]
        joueur_nom = noms[joueur_actuel]
        coups_possibles = [c for c in main if carte_valide(c, carte_sommet)]

        # --- Tour humain ---
        if joueur_actuel < nb_humains:
            print(retro("Votre main :", Fore.GREEN))
            print(retro(afficher_main(main), Fore.GREEN))
            print()
            choix = input(retro("Numéro de carte ou 'p' pour piocher : ", Fore.YELLOW)).strip()
            if choix.lower() == "p":
                paquet, pile = reconstituer_paquet(paquet, pile)
                main.append(paquet.pop())
                log = "Pioche effectuée"
            else:
                try:
                    carte = main[int(choix)-1]
                    if carte_valide(carte, carte_sommet):
                        main.remove(carte)
                        pile.append(carte)
                        sens, log = appliquer_effet(carte, joueur_actuel, mains, nb_joueurs, paquet, pile, noms, sens)
                        log = f"{joueur_nom} joue {carte[0]} {carte[1]}"
                    else:
                        log = "❌ Carte invalide"
                except (ValueError, IndexError):
                    log = "Entrée invalide"
        else:
            # --- Tour bot ---
            time.sleep(1)
            coups = [c for c in main if carte_valide(c, carte_sommet)]
            if not coups:
                main.append(paquet.pop())
                log = f"{joueur_nom} pioche"
            else:
                carte = random.choice(coups)
                main.remove(carte)
                pile.append(carte)
                sens, log = appliquer_effet(carte, joueur_actuel, mains, nb_joueurs, paquet, pile, noms, sens)
                log = f"{joueur_nom} joue {carte[0]} {carte[1]}"
            time.sleep(1)

        # Vérifie la victoire
        if not main:
            afficher_plateau(noms, mains, pile, joueur_actuel, sens, retro(f"{joueur_nom} a gagné la partie ! 🏆", Fore.YELLOW))
            break

        joueur_actuel = (joueur_actuel + sens) % nb_joueurs


# ------------------------------
# Lancer le jeu
# ------------------------------

if __name__ == "__main__":
    jouer_uno()
