#!/usr/bin/env python

# -*- coding: utf-8 -*-

# importation des modules
import DB
from CONST import *
import datetime
from random import choice, randint, randrange
from os import startfile, listdir, getcwd, mkdir, rename
# from os.path import isdir, exists, splitext, isfile, join
import shutil
from collections import OrderedDict
import json
import os.path

class E(Exception):
    
    def __init__(self, com, s, msg):
        Exception.__init__(self)
        self.s = s
        self.msg = msg
        self.com = com
        

    def affiche(self):
        print(f"Erreur {self.s} : {self.msg}")
        self.com.set(f"Erreur {self.s} : {self.msg}")


class Clic:

    def __init__(self, boss=None):
        self.com = None
        self.boss = boss
        self.db = DB.Database()
        self.bac = None
        
    def setCom(self, com):
        self.com=com
       
    def setBac(self, bac):
        self.bac = bac
        self.bac.setDb(self.db)
       
        
    def displayContenu(self, **KW):
        if KW['item'] == "ajouter une table":
            KW['entry2_var'].set('')
            KW['entry2'].focus_set()

        elif KW['item'] == "afficher la salle":
            
            KW['bac'].focus_set()
            
        elif KW['item'] == "modifier le thème":
            theme_lst = [" "+item for item in self.boss.th.dic_theme.keys()]
            theme = " " + self.boss.th.theme
            KW['listBox_lst'].clear()
            KW['listBox_lst'].extend(theme_lst)
            wth=0
            for item in theme_lst:
                if len(item)>wth:
                    wth = len(item)
            KW['listBox'].configure(height=min(len(theme_lst), HEIGHT_LISTBOX), width=wth+1)
            KW['listBox_var'].set(theme_lst)
            KW['listBox'].selection_set(theme_lst.index(theme))
            KW['listBox'].focus_set()
            
        elif KW['item'] == "ajouter un employé":
            KW['entry2_var'].set('')
            KW['entry2'].focus_set()
            
        elif KW['item'] == "éditer les employés":
            KW['entry2_var'].set('')
            KW['entry2']['state']=DISABLED
            employe_lst = [' Jacques', ' Norbert', ' Andrea']
            KW['listBox_lst'].clear()
            KW['listBox_lst'].extend(employe_lst)
            KW['listBox'].configure(height=min(len(employe_lst), HEIGHT_LISTBOX), width=LENGTH_CODE+2)
            KW['listBox_var'].set(employe_lst)
            KW['listBox'].selection_set(0)
            KW['listBox'].focus_set()
          
        elif KW['item'] == "ajouter un article":
            KW['entry2_var'].set('')
            KW['entry3_var'].set('')
            KW['entry4_var'].set('')
            KW['entry2'].focus_set()  
            
    def commandBouton(self, contenu, numeroBouton):
        if contenu.item == "nouvelle caisse":
            # désactiver la touche dans le menu
            self.boss.cadreGestion.entete.desactive_item('nouvelle caisse')
            
            # ajouter un id dans la base de données, avec le statut 1 (ouvert)
            self.db.base1(dat = datetime.datetime.now())
            
            # afficher la salle
            self.boss.cadreGestion.corps.display("afficher la salle")
            
        if contenu.item == "ajouter une table":
            nom, largeur, hauteur, couleur = contenu.entry2_var.get().strip(), contenu.entry3_var.get().strip(), contenu.entry4_var.get().strip(), contenu.spinBox_var.get()
            table_names = self.bac.find_withtag(nom)
            
            test =''
            try:
                 # le nom de la table doit être unique (utiliser la base de données ou le canvas)
                if nom in table_names:
                    raise E(self.com, 'NOM', 'nom déjà utilisé')  
                if not nom :
                    raise E(self.com, 'NOM', 'pas de nom')
                if len(nom) > LENGTH_TABLE:
                    raise E(self.com, 'NOM', f"nom trop long (max {LENGTH_TABLE} caractères)")
                
                # largeur et hauteur conforme (voir les constantes)
                test = "LARGEUR"
                if not 1 <= float(largeur) <= self.bac.getNbrMaxTable("width"):
                    raise E(self.com, 'LARGEUR', f'largeur comprise entre 1 et {self.bac.getNbrMaxTable("width")}') 
                test = "HAUTEUR"
                if not 1 <= float(hauteur) <= self.bac.getNbrMaxTable("height"):
                    raise E(self.com, 'HAUTEUR', f'hauteur comprise entre 1 et {self.bac.getNbrMaxTable("height")}')
            
            except E as e:
                e.affiche()
                
            except ValueError:
                E(self.com, test, 'non-conforme').affiche()
            
            else:    
                # récupérer la couleur par rapport aux thèmes (th se trouve dans le root)
                couleur = self.boss.th.getColorT(couleur)
                
                # supprimer le message
                self.com.set('  ')
                
                # ajouter une table au milieu du canvas
                tup = self.bac.create_table(largeur=float(largeur),
                                                hauteur=float(hauteur), 
                                                couleur=couleur, 
                                                tableName=nom)
        
                # basculer l'affichage dans la table
                self.boss.cadreGestion.corps.display("afficher la salle")
            
    def commandListBox(self, **KW):    
        print(KW['listBox'].curselection(), KW['item'])
        if not KW['listBox'].curselection():
            return
        if KW['item'] == "modifier le thème":
            index = int(KW['listBox'].curselection()[0])
            theme = KW['listBox'].get(index).strip()
            self.boss.th.set_theme(theme)
        
        if KW['item'] == "éditer les employés":
            KW['entry2_var'].set('')
            KW['entry2']['state'] = DISABLED
            
    def commandSpinBox(self, **KW):
        pass
                
    def returnListBox(self, **KW):
        if KW['item'] == "éditer les employés":
            index = int(KW['listBox'].curselection()[0])
            employe = KW['listBox'].get(index).strip()
            KW['entry2']['state'] = NORMAL
            KW['entry2_var'].set(employe)
            KW['entry2'].focus_set()
             
   
       