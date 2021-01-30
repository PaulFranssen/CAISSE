# -*- coding: utf-8 -*-

# importation des modules

# from func import *
#from tkinter import *

# variables dynamiques
## hauteur des listbox
#h_03i = Tk().IntVar()

#h_15i, h_27i, h_08i, h_09i, h_10i = IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar() 


from CONST import *

# ##################################################
# kw_master = {'bg': color_30}


# ################ f ################################
# kw_pf = {'bg': color_32}
# pad_pf = {'pady': 0, 'padx': 0, 'fill': 'both', 'expand': 1}

# kw_f1 = {'bg': color_32}
# pad_f1 = {'padx': 0, 'pady': 0, 'fill': 'x'}

# kw_f2 = {'bg': color_32}  # 18
# pad_f2 = {'padx': 0, 'pady': p_02, 'fill': 'y', 'expand': 1}

# kw_fx = {'bg': color_32}  # 18
# pad_fx = {'fill': 'y', 'expand': 1}


# ################### c #############################################
# kw_c0 = {'bg': color_33}
# pad_c0 = {'padx': 0, 'pady': 20}

# kw_c1 = {'bg': color_32}  # 32
# pad_c1 = dict(fill='y', expand=1)

# kw_c2 = {'bg': color_32}
# pad_c2 = {'padx': 0, 'pady': 5}

# kw_c3 = {'bg': color_4}
# pad_c3 = {'padx': 5, 'pady': 5}

# kw_c4 = {'bg': color_5}
# pad_c4 = {'padx': 5, 'pady': 5}

# kw_c5 = {'bg': color_7}
# pad_c5 = {'padx': 5, 'pady': 5}

# # cadre pour c7 c8
# kw_cx = dict(bg=color_32)

# # cadre pour 2 colonnes
# kw_c6 = dict(bg=color_32)
# pad_c6 = dict(padx=75)

# # cadre de ligne label entry label entry
# kw_c7 = {'bg': color_32}
# pad_c7 = {'padx': 0, 'pady': p_05, 'fill': 'x', 'expand': 1}

# kw_c8 = {'bg': color_32}
# pad_c8 = {'padx': 0, 'pady': p_05, 'fill': 'x', 'expand': 1}

# # labelframe
# kw_c9 = {'bg': color_32, 'fg': color_37}
# pad_c9 = {'padx': 0, 'pady': p_05, 'fill': 'x'}

# kw_c10 = {'bg': color_10}
# pad_c10 = {'padx': 0, 'pady': 5}

# kw_c11 = {'bg': color_33}
# pad_c11 = {'padx': 0, 'pady': 5, 'fill': 'y', 'expand': 1}

# kw_c12 = {'bg': color_32}
# pad_c12 = {'padx': 0, 'pady': 5, 'fill': 'x', 'expand': 1}

# kw_c13 = {'bg': color_32}
# pad_c13 = {'padx': 0, 'pady': 20, 'fill': 'x'}

# kw_c14 = {'bg': color_32}
# pad_c14 = {'padx': 0, 'pady': 0}

# kw_c22 = {'bg': color_32}
# pad_c22 = {'padx': 0, 'pady': 5, 'fill': 'x', 'expand': 1, 'anchor': 'n'}

# kw_c44 = {'bg': color_5}
# pad_c44 = {'padx': 5, 'pady': 25}

# kw_c15 = {'bg': color_32}
# pad_c15 = {'padx': 5, 'pady': 5, 'fill': 'x'}

# kw_c16 = {'bg': color_32}
# pad_c16 = {'padx': 5, 'pady': 5, 'fill': 'x'}

# kw_c17 = {'bg': color_32}
# pad_c17 = {'pady': 5, 'fill': 'x'}

# kw_c20 = {'bg': color_32}
# pad_c20 = {'padx': 0, 'pady': 0}

# ###################### s #############################
# s1 = 10
# s2 = 10

# ######################### widget ###################################

# menubutton
KW_MENUBUTTON = dict(font=(POLICE, TAILLE_CAR), relief='flat', bd=0)
PAD_MENUBUTTON = dict(padx=5, side='left')

# menu
KW_MENU = dict(font=(POLICE, TAILLE_MENU), tearoff=0, relief='flat')

# séparateur menu
KW_BARRE_VERTICALE = dict(text="|", font=(POLICE, TAILLE_MENU))

# # button fermeture et réduction
KW_FERMETURE = dict(font=(POLICE, TAILLE_CAR),
                    relief='flat',
                    bd=0, 
                    takefocus=0)
PAD_FERMETURE = dict(padx=5, side=RIGHT)

KW_TITRE = dict(font = (POLICE, TAILLE_TITRE, "italic"))

# kw_10 = {'font': (police_1, taille_4)}
# pad_10 = {'padx': 0, 'pady': 0}

# # label avant entry
# kw_11 = dict(font=(police_1, taille_4), bg=color_32, fg=color_37)
# pad_11 = dict(padx=5, pady=0)

# # entry
# kw_12 = dict(
#     font=(police_1, taille_4), 
#     bg=color_37, 
#     fg=color_30, 
#     bd=0, 
#     relief='flat',
#     disabledbackground=color_33, 
#     disabledforeground=color_30, 
#     insertbackground=color_30,
#     selectbackground=color_6, 
#     selectforeground=color_30, 
#     justify="center")

# pad_12 = dict(padx=5, pady=0)

# # label écran d'accueil
# kw_13 = dict(font=(police_1, taille_8, 'italic'), bg=color_32, fg=color_6)

# # comment
# kw_14 = dict(font=(police_1, taille_4, 'italic'), bg=color_32, fg=color_6)
# pad_14 = dict(pady=p_04)

# kw_27 = {'font': (police_1, taille_4)}
# pad_27 = {'padx': 0, 'pady': 10}

# # listbox
# kw_28 = {'selectmode': 'browse', 'bg': color_33, 'font': (police_1, taille_4),
#          'selectbackground': color_6, 'selectforeground': color_30, 'takefocus': 0,
#          'activestyle': 'none', 'highlightthickness': 0,
#          'relief': 'flat'}
# pad_28 = {'pady': 0}

# # spinbox de l'exercice
# kw_32 = {'fg': color_32, 'font': (police_1, taille_4), 'justify': 'center',
#          'state': 'readonly', 'readonlybackground': color_37,
#          'buttonbackground': color_37, 'relief': 'flat', 'takefocus': 0,
#          'buttondownrelief': 'flat',
#          'buttonuprelief': 'flat'}

# # titre des listbox
# kw_40 = {'font': (police_1, taille_4), 'bg': color_32, 'fg': color_37}
# pad_40 = dict()

# # titre de la fenêtre
# kw_42 = {'font': (police_1, taille_5, 'italic'), 'bg': color_32, 'fg': color_37}
# pad_42 = dict()

# # button (enregistrer, ...
# kw_45 = {'font': (police_1, taille_4), 'bg': color_33, 'fg': color_30, 'relief': 'flat',
#          'bd': 0, 'activeforeground': color_30, 'activebackground': color_6,
#          'highlightcolor': color_6}
# pad_45 = {'padx': 20}


# # checkbutton d encodage (en vente, amortissement, ...)
# kw_47 = {'selectcolor': color_32, 'font': (police_1, taille_4), 'bg': color_32, 'fg': color_37, 'bd': 0,
#          'activebackground': color_32, 'relief': 'flat', 'highlightthickness': 0, 'highlightcolor': color_32,
#          'activeforeground': color_37, 'takefocus': 0}
# kw_47b = {'font': (police_1, taille_4), 'bg': color_32, 'fg': color_32, 'bd': 0
#          , 'relief': 'flat'}
# pad_47 = {}

# # checkbutton dans la fixation de catégorie (g)
# pad_47c = dict(padx = 30, side = 'right')

# # checkbutton d encodage (en vente, amortissement, ...) dans situation à 2 colonnes
# pad_48 = dict(side='left')


# # checkbutton (définir par défaut , checkbutton plus petit)
# kw_49 = {'selectcolor': color_32, 'font': (police_1, taille_7), 'bg': color_32, 'fg': color_37, 'bd': 0,
#          'activebackground': color_32, 'relief': 'flat', 'highlightthickness': 0, 'highlightcolor': color_32,
#          'activeforeground': color_37, 'takefocus': 0}

# # séparation dans le menu
# kw_50 = dict(text="|", fg=color_6, font=(police_1, taille_3), bg=color_32)

# # button fermeture et réduction
# kw_51 = dict(font=(POLICE, TAILLE_CAR), bg=color_32, fg=color_6, relief='flat',
#              bd=0, activeforeground=color_6, activebackground=color_32, takefocus=0)

# # exercice et database affichés à droite
# kw_52 = dict(font=(police_1, taille_3), fg=color_37, bg=color_32)
# # database
# kw_52b = dict(font=(police_1, taille_4), fg=color_6, bg=color_32)

# # cadre englobant erercice et database
# kw_53 = dict(bg=color_32)
# pad_53 = dict(padx=30)

# # color paramètres G select
# kw_54 = {'col_spec' : color_6}

# #########################################################
# lst = []  # liste des dictionnaires contenant les paramètres
# lst = lst + [kw_master]
# lst = lst +[kw_pf, kw_f1, kw_f2, kw_fx, kw_c0, kw_c1, kw_c2, kw_c3, kw_c4, kw_c5, kw_cx, kw_c6, kw_c7]
# lst = lst + [kw_pf, kw_f1, kw_f2, kw_fx, kw_c0, kw_c1, kw_c2, kw_c3, kw_c4, kw_c5, kw_cx, kw_c6, kw_c7]
# lst = lst + [kw_c8, kw_c9, kw_c10, kw_c11, kw_c12, kw_c13, kw_c14, kw_c22, kw_c44, kw_c15, kw_c16, kw_c17, kw_c20]

# lst = lst + [kw_1, kw_2, kw_3, kw_10, kw_11, kw_12, kw_13, kw_14, kw_27, kw_28, kw_32, kw_40, kw_42]
# lst = lst + [kw_45, kw_47, kw_47b, kw_49, kw_50, kw_51, kw_52, kw_52b, kw_53, kw_54]

# def modif_1(x):
#     """modifie la couleur de la base

#     Args:
#         x (str): nouvelle couleur
#     """
#     for dico in lst:
#         for cle, valeur in dico.items():
#             if type(valeur) == str and valeur == color_6:
#                 dico[cle] = x
