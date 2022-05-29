# -*- coding: utf-8 -*-


from tkinter.font import BOLD
from CONST import *

import os.path
import json

KW_MENUBUTTON = dict(font=(POLICE, TAILLE_CAR), relief='flat', borderwidth=0)
PAD_MENUBUTTON = dict(padx=5, side='left')


KW_MENU = dict(font=(POLICE, TAILLE_MENU), tearoff=0, relief='flat', bd=0, activeborderwidth=0)

# séparateur entre les menuButton
KW_BARRE_VERTICALE = dict(text="|", font=(POLICE, TAILLE_MENU))

# button fermeture et réduction
KW_FERMETURE = dict(font=(POLICE, TAILLE_CAR),
                    relief='flat',
                    bd=0, 
                    takefocus=0)
PAD_FERMETURE = dict(padx=5, side=RIGHT)

KW_TITRE = dict(font = (POLICE, TAILLE_TITRE, "italic"))
PAD_TITRE = dict(pady=15)

KW_COMMENT = dict(font=(POLICE, TAILLE_CAR, 'italic'))
PAD_COMMENT = dict(pady=10)

KW_LISTBOX = dict(selectmode='browse', 
                  font=(POLICE, TAILLE_CAR),
                  takefocus=0,
                  activestyle= 'none', 
                  highlightthickness= 0,
                  relief='flat',
                  bd=0)

# listBox pour le service et le code dans facturation
KW_LISTBOX2 = dict(selectmode='browse', 
                  font=(POLICE, TAILLE_CAR, 'italic'),
                  takefocus=0,
                  activestyle= 'none', 
                  highlightthickness= 0,
                  relief='flat',
                  justify='center',
                  bd=0)
# kw_28 = {'selectmode': 'browse', 'bg': color_33, 'font': (police_1, taille_4),
#          'selectbackground': color_6, 'selectforeground': color_30, 'takefocus': 0,
#          'activestyle': 'none', 'highlightthickness': 0,
#          'relief': 'flat'}

PAD_LISTBOX = dict(pady=0)

KW_LABEL = dict(font=(POLICE, TAILLE_CAR))
PAD_LABEL = dict(padx=5, pady=5)

KW_BUTTON = dict(font=(POLICE, TAILLE_CAR, BOLD), relief='flat', bd=0, height=HEIGHT_BUTTON) 
PAD_BUTTON = dict(padx=20, side=LEFT)

KW_SMALL_BUTTON = dict(font=(POLICE, TAILLE_SMALL_CAR), relief='flat', bd=0) 
PAD_SMALL_BUTTON = dict()

KW_ENTRY = dict(font=(POLICE, TAILLE_CAR),         
                bd=0, 
                relief='flat',
                justify="center")
PAD_ENTRY = dict(padx=5, pady=0)
KW_CANVAS = dict(relief=FLAT, highlightthickness= 0, bd=0)
PAD_SALLE = dict(padx=MARGE_SALLE)
KW_SPINBOX = dict(font=(POLICE, TAILLE_CAR),justify='center',
                    state='readonly', 
                    relief='flat',
                    buttondownrelief='flat',
                    buttonuprelief='flat',
                    wrap=TRUE)
PAD_SPINBOX = dict(padx=5, pady=0)

class Theme:
    
    def __init__(self):
        
        # attributs
        self.widget_dic={}
        
        # récupération du dictionnaire des thèmes dans le fichier json
        with open(os.path.join(DATA_FILE, THEME_FILE), 'r', encoding = "utf-8") as read_file:
            self.dic_theme = json.load(read_file)

        # création du fichier mémoire du thème le cas échéant en y fixant le premier thème
        if not os.path.exists(os.path.join(DATA_FILE, LAST_THEME_FILE)):
            with open(os.path.join(DATA_FILE, LAST_THEME_FILE), "w", encoding='utf-8') as write_file:
                write_file.write(list(self.dic_theme.keys())[0])
            
        # récupération du thème courant dans le fichier txt:
        with open(os.path.join(DATA_FILE, LAST_THEME_FILE), 'r', encoding = "utf-8") as read_file:
            self.theme = read_file.read().strip() 
        if self.theme not in self.dic_theme:  # cas où le thème lu n'est pas dans le dictionnaire des themes (par exemple si il a été supprimé ou modifié)
            self.theme = list(self.dic_theme.keys())[0]
            with open(os.path.join(DATA_FILE, LAST_THEME_FILE), "w", encoding='utf-8') as write_file:
                write_file.write(list(self.dic_theme.keys())[0])
            
    def add_widget(self, key, wgt):
        """ajoute un widget au dictionnaire

        Args:
            key (str): cle du dictionnaire (type de widget)
            wgt (widget): widget à ajouter
        """
        if key in self.widget_dic:
            self.widget_dic[key].append(wgt)
        else:
            self.widget_dic[key] = [wgt]
            
        
    def set_theme(self, theme):
        """modifie le thème

        Args:
            theme (str): nom du thème à appliquer (si chaine vide, alors fixer le thème actuel)
        """       

        if theme:
            self.theme=theme
            with open(os.path.join(DATA_FILE, LAST_THEME_FILE), "w", encoding='utf-8') as write_file:
                write_file.write(self.theme)
        
        for key, lst in self.widget_dic.items():  
            if key == 'bac':
                # opérations sur les id du bac
                for canvas in lst:
                    for color in self.dic_theme[self.theme]['table']:
                        ids = canvas.find_withtag(color)
                        for id in ids:
                            canvas.itemconfigure(id, fill=self.dic_theme[self.theme]['table'][color])
            
            for wgt in lst:
                wgt.configure(**self.dic_theme[self.theme][key])
                
    # def change_theme(self, list_wgt, key):
    #     """modifie les caractères d'une liste de widget en les définissant avec la clé key

    #     Args:
    #         list_wgt (list): liste de widgets à modifier
    #         key (str): clé du dictionnaire (ex "entry", "table", ...)
    #     """
    #     for wgt in list_wgt:
    #         wgt.configure(**self.dic_theme[self.theme][key])
    
    def getColorWarning(self, choix = "fg"):
        """obtenir la couleur du caractère de entryWarning (par défaut "fg", ou choix autre caractéristique)
        """
        return self.dic_theme[self.theme]["entryWarning"][choix]
    
    def getColorOK(self, choix = "fg"):
        """obtenir la couleur du caractère de entryOK (par défaut "fg", ou choix autre caractéristique)
        """
        return self.dic_theme[self.theme]["entryOK"][choix]
    
    def getColorNormal(self, choix = "fg"):
        """obtenir la couleur du caractère de entry (par défaut "fg", ou choix autre caractéristique)
        """
        return self.dic_theme[self.theme]["entry"][choix]
                    
    def getColorTable(self):    
        """renvoie la liste des couleurs de la table
        """
        return list(self.dic_theme[self.theme]['table'].keys())
               
    def getColorT(self, couleur):
        """renvoie le code couleur pour une couleur(clé) de table
        """
        return  self.dic_theme[self.theme]['table'][couleur]
    
    def getForegroundListBox(self, transfert=0):
        """renvoie le foreground pour la listBox (recordF)
        """
        if transfert == 0:
            return  self.dic_theme[self.theme]['listBoxNormal']['fg']
        else:
            return  self.dic_theme[self.theme]['listBoxTransfert']['fg']

    def getValiderFocus(self, valider):
        """renvoie le background du bouton valider
        """
        if valider == 0:
                return  self.dic_theme[self.theme]['validerFocusOut']['bg']
        else:
            return  self.dic_theme[self.theme]['validerFocusIn']['bg']

