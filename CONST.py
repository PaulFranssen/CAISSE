from tkinter import *
import sys
from os.path import join

# -*- coding: utf-8 -*-

# directory
DATA_FILE = "DATA_FILE"

# file_name
MENU_FILE = "menu_file.json"
THEME_FILE = "theme_file.json"
LAST_THEME_FILE = "last_theme.txt"
DATABASE_FILE = "bdd.db"
VENTEX = "DOCUMENTS/ventex.csv"
ARTICLES_FILE="articles"


# tailles des caractères
TAILLE_TITRE = 25
TAILLE_CAR = 18
SEPARATEUR_HORIZONTAL = 36
SEPARATEUR_DANS_CADRE = 20
TAILLE_SMALL_CAR = 12
TAILLE_MENU = 16

# temps d'attente
attenteLongue = 1500
attenteCourte = 500

# constantes dans la salle
ROUGE = "#FF0000"  # encaisséE
VERT = "#FFFFFF"   # en cours
VERT2="grey80"      # modifiée
ORANGE = "#FF000D" #39FF14"  # facturé            #FD6C9E" #FF0001"

DIC_STATUT = {VERT:"EN COURS", VERT2:"MODIFIé".upper(), ORANGE : "FACTURé".upper(), ROUGE:"CLOTURé".upper()}

COEF_DILATATION = 1.5
COEF_REMPLISSAGE = 0.95  # pourcentage de remplissage de l'écran pour une table de dimension maximale
DECOUPAGE_HEIGHT = 18   # ce découpage me donnera le nombre de pixel par table , par la formule winfo_screenheight/découpage_height+coef_dilatation

HEIGHT_FACTURE = 20 #24
HAUTEUR_TEXTE_SALLE = 14
MARGE_SALLE = 10
MARGE_HAUTE_SALLE = 10
CURSOR = "crosshair"

LENGTH_TABLE = 12  # longeur maximale d'un nom de table
LENGTH_WORKER = 15  # longeur maximale d'un worker
LENGTH_DIMENSION_TABLE = 4
CAPTURE_DANS_TABLE = "find_enclosed"#"find_overlapping" #: touche la table, "find_enclosed" : intérieur à la table

# largeur et hauteur widgets
HEIGHT_BUTTON = 1
WIDTH_BUTTON = 12
HEIGHT_LISTBOX = 19  # à moduler suivant les dimensions de l'écran
HEIGHT_LISTBOX2 = 4 # liste de choix des articles
HEIGHT_LISTBOX3 = 2 # liste de choix des workers
ESPACE_VERTICAL_BUTTON_VALIDER = 0
LENGTH_CODE = 15
LENGTH_DESCRIPTION = 30
LENGTH_PRIX = 10
LENGTH_NUMERO = 5
LENGTH_QTE = 5
LENGTH_PU = 10
LENGTH_ETAT_FACTURE = 9
LENGTH_DATE = 21
F = lambda x : f"{x[0]:^15}   {x[1]:^30}   {x[2]:^10}   {x[3]:^5}   {x[4]:^10}   {x[5]:^10}" 
FOREGROUND_TRANSFERT = "grey25" # devrait se trouver dans le theme

# écarts
ECART_DOUBLE_CADRE_VERTICAL = 100

# police
POLICE = "Consolas"
POLICE_SALLE = "Bahnschrift Condensed" #"Helvetica"
POLICE_TABLE = "Bahnschrift" #"Helvetica"
POLICE_FIRST = "consolas" # écran d'acceuil
TAILLE_FIRST = 110

# nombre de jours de mémoire pour la caisse
MEMORY = 7

# constantes pour ticket

TIRET='-'*31
BARRE="_"*31
TICKET_FILE = "ticket"
ETOILE='*'*31
NOM_BAR=' T G V   L O U N G E   B A R '
NUM_TEL='TEL:62291515/95566592'
POLITESSE="Merci et à bientôt au TGV!"
IMPR = 'edit' # 'print'
JOUR_SEM = [ 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

# fonction lambda pour les prix
fpx = lambda p : "{:,}".format(int(p)).replace(",", ".")

# détermination des paramètres de l'affichage
fenetre = Tk()
w, h = fenetre.winfo_screenwidth(), fenetre.winfo_screenheight()

# test à réaliser pour la conformité de l'affichage
if h not in {1080, 900}:
    print(f"paramètres d'affichage {w}x{h} non pris en compte")
    sys.exit()















