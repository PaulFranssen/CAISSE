# -*- coding: utf-8 -*-

# directory
DATA_FILE = "DATA_FILE"

# file_name
MENU_FILE = "menu_file.json"
THEME_FILE = "theme_file.json"
LAST_THEME_FILE = "last_theme.txt"

# tailles des caractères
TAILLE_TITRE = 25
TAILLE_CAR = 18
TAILLE_MENU = 16

# largeur et hauteur widgets
HEIGHT_BUTTON = 1
WIDTH_BUTTON = 12
HEIGHT_LISTBOX = 20  # à moduler suivant les dimensions de l'écran
LENGTH_CODE = 15

# écarts
ECART_DOUBLE_CADRE_VERTICAL = 150

# police
POLICE = "Consolas"












from tkinter import *
import sys
from os.path import join

# détermination des paramètres de l'affichage
fenetre = Tk()
w, h = fenetre.winfo_screenwidth(), fenetre.winfo_screenheight()

# test à réaliser pour la conformité de l'affichage
if h not in {1080, 900}:
    print(f"paramètres d'affichage {w}x{h} non pris en compte")
    sys.exit()

# liste des couleurs non-utilisées
color_1 = 'wheat1'
color_2 = 'pink'
color_3 = 'blue'
color_4 = 'green'
color_5 = 'yellow'
color_7 = 'purple'
color_8 = 'black'
color_9 = 'white'
color_10 = 'wheat3'
color_11 = 'alice blue'
color_13 = 'wheat2'
color_14 = 'yellow4'
color_15 = 'ivory3'
color_16 = "wheat4"
color_17 = 'khaki3'
color_18 = 'SteelBlue1'
color_19 = 'DarkSeaGreen1'
color_20 = 'VioletRed1'
color_21 = 'VioletRed3'
color_29 = 'grey0'
color_30 = "black"  # aj
color_31 = 'grey10'
color_34 = 'grey40'
color_35 = 'grey50'
color_36 = 'grey60'
color_38 = 'grey80'


# largeur des labels et entry
l_couplage = 1
l_pc = 5 # longueur pour pourcentage
l_code = 15
l_des = 30
l_base = 15
l_baseC = l_base - 8
l_pv = 7
l_min = 4
l_alerte = 2
l_actif = 2
l_contact = 35
l_date = 12             # date sans le jour ou sans l'année
l_date2 = 14            # date avec le jour
l_path = 50
l_filename = 30
l_num = 10
l_descript = 50         # description de la charge
l_prix = 11
l_qte = 6
l_type = 20
l_explication = 52
l_proportion = len(' proportion ')

# largeur button de base
l_button1 = len('enregistrer')+1

# nombre de jours de traçage
n_trace = 14

# titre et bas des colonnes en label, ainsi que largeur de ces labels

ligne_2 = '{:^' + str(l_date) + '}   {:^' + str(l_num) + '}   {:^' + str(l_code) + '}   {:^' + str(l_prix) + '}'
l_2 = len(ligne_2.format('DATE', 'N°PIÈCE', 'TIERS', 'TOTAL'))

# éditer les charges
ligne_3 = '{:^' + str(l_date) + '}   {:^' + str(l_num) + '}   {:^' + str(l_type) + '}   {:^' + str(
    l_code) + '}   {:^' + str(l_prix) + '}   {:^' + '3' + '}'
l_3 = len(ligne_3.format('DATE', 'N°PIÈCE', 'TYPE', 'TIERS', 'MONTANT', ' '*3))

ligne_4 = '{:^' + str(l_date) + '}   {:^' + str(l_code) + '}   {:^' + str(l_prix) + '}'
l_4 = len(ligne_4.format('DATE', 'CAISSIER(ÈRE)', 'TOTAL'))

ligne_5 = '{:^' + str(l_date) + '}   {:^' + str(l_code) + '}   {:^' + str(
    l_qte) + '}   {:^' + str(l_explication) + '}'
l_5 = len(ligne_5.format('DATE', 'CODE', '+/-', 'EXPLICATION'))

ligne_7 = '{:^' + str(l_code) + '}   {:^' + str(l_des) + '}   {:^' + str(l_proportion) + '}'
l_7 = len(ligne_7.format('CODE', 'DÉSIGNATION', 'PROPORTION'))

ligne_8 = '{:^' + str(l_code) + '}   {:^' + str(l_des) + '}   {:^' + str(l_qte) + '}   {:^' + str(l_prix) + '}'
l_8 = len(ligne_8.format('CODE', 'DÉSIGNATION', 'QTÉ', 'PRIX'))

# réglages finaux
taille_4 = 18       # taille des caractères normaux
taille_3 = 16       # taille de l'exercice et de la base en haut à droite et du menu
taille_5 = 22       # taille du titre
taille_7 = 13       # taille petit checkbutton (par défaut)
taille_8 = 100       # taille logo



# distanciation entre cadres selon paramètres d'affichage
if h == 1080:
    p_02 = 40
elif h == 900:
    p_02 = 25
p_03 = 60
p_04 = 10
p_05 = 15

# hauteur de box selon paramètres d'affichage
if h == 1080:
    h_03 = 20       # 20 pour 1920 listbox choix avec selection et button nouveau en bas
    h_15 = 13       # 13 listbox de facture de vente
    h_27 = h_15 - 0     # -0 idem
    h_08 = 23       # 23 pour 1920 lisbox choix avec selevction mais sans button ni comment en bas
    h_09 = 5        # lisbox composition
    h_10 = 21       # 21 pour 1920 listbox sans button mais avec comment
elif h == 900:
    h_03 = 15       # 20 pour 1920 listbox choix avec selection et button nouveau en bas
    h_15 = 10       # 13 listbox de facture de vente
    h_27 = h_15 -2     # -0 idem
    h_08 = 18       # 23 pour 1920 lisbox choix avec selevction mais sans button ni comment en bas
    h_09 = 5        # lisbox composition
    h_10 = 16       # 21 pour 1920 listbox sans button mais avec comment

# fixation des hauteurs pour écran 1080
# couleur
color_32 = 'grey15'         # fond écran
color_37 = 'grey80'         # écriture claire
color_6 =  'tomato'         # 'lime green' sélection
color_33 = 'grey30'         # disabled
color_30 = 'black'          # écriture foncée

# police de caractère
police_1 = "Consolas"

# NOMS DE FICHIERS

f_partage = join("MEM_FILE", "share_file.txt")
f_sauvegarde = join("MEM_FILE", "save_file.txt")
f_base = join("MEM_FILE", "base_file.txt")
f_dirImport = join("MEM_FILE", "dirImport_file.txt")
f_dirImportVente = join("MEM_FILE", "dirImportVente_file.txt")
f_nameImport = join("MEM_FILE", "nameImport_file.txt")
f_ticket = join("MEM_FILE", "ticket_file.txt")

# temps d'attente
attenteLongue = 1000
attenteCourte = 700

# réglage distance entre les entry sous les listbox
reglage_1 = 33
reglage_2 = 33
reglage_3 = 65

# coefficient de placement des composés dans la liste générée
# indique la proportion minimale et maximale d'article inventorié à prendre en compte pour G
coef_compose_inf, coef_compose_sup = 0.2, 0.4
# maximum de recherche itérations pour générer
max_iteration = 3000
# nombre de catégories fixées (pour générer)
nbr_categorie_fix = 5

# encoding 

encoDoc = 'latin-1'

encoTic = 'latin-1'















