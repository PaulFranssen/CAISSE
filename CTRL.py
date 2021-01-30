#!/usr/bin/env python

# -*- coding: utf-8 -*-

# importation des modules
from CONST import *
from sqlite3 import *
from random import choice, randint, randrange
from os import startfile, listdir, getcwd, mkdir, rename
# from os.path import isdir, exists, splitext, isfile, join
import shutil
from collections import OrderedDict
import json
import os.path

class E(Exception):
    pass


class Base:

    def __init__(self):
        
        pass
        # attributs
       
    
        # self.database = None
        # self.database_path = None
        # self.connexion = None
        # self.curseur = None
        # self.cp = None
        
       
             
    def fermer(self):
        pass

    # def fix_cp(self, cp):
    #     self.cp = cp
    # # self.fix_exercice(date.today().year)

    # def fix_theme(self, theme):
    #     self.theme = theme
    #     # self.cp.fix_exercice(theme)

    # def fix_database(self, database):

    #     # fixer le nom de la database et le path
    #     self.database = database
    #     self.database_path = join('BASE', database + '.db')

    #     # afficher le nom à l'écran
    #     self.cp.fix_database(self.database)

    #     # création de la database ou ouverture simple
    #     self.ouvrir()

    #     # création éventuelle des tables
    #     self.create_cat()
    #     self.create_type()
    #     self.create_article()
    #     self.create_composition()
    #     self.create_tiers()
    #     self.create_workers()
    #     self.create_charge()
    #     self.create_factureA()
    #     self.create_recordA()
    #     self.create_vente()
    #     self.create_recordV()
    #     self.create_stocloture()
    #     self.create_correction()
    #     self.create_ponderation()
    #     self.create_fixecat()
    #     self.create_limitation()
    #     self.create_trace()

    #     # fermeture de la database
    #     self.fermer()

    #     # enregistrement dans le fichier f_base de la database de lancement
    #     with open(f_base, 'w', encoding='utf-8') as f:
    #         f.write(self.database)

    # def get_database(self):
    #     return self.database

    # def get_curseur(self):
    #     return self.curseur

    # def ouvrir(self):
    #     try:
    #         self.connexion = connect(self.database_path, detect_types=PARSE_DECLTYPES | PARSE_COLNAMES)
    #         self.connexion.execute("PRAGMA foreign_keys = 1")
    #         self.curseur = self.connexion.cursor()

    #     except Error as error:
    #         print("Error while connecting to sqlite", error)

    #     else:
    #         if self.connexion:
    #             # connexion à la base de données
    #             pass

    # def enregistrer(self):
    #     self.connexion.commit()

    # def fermer(self):
    #     self.connexion.close()

    # def create_f(self):

    #     # fixation de l'execice
    #     self.fix_exercice(date.today().year)

    #     # création des fichiers txt
    #     try:
    #         if not exists('BASE'):
    #             mkdir('BASE')
    #         elif not isdir('BASE'):
    #             mkdir('BASE')
    #         if not exists('MEM_file'):
    #             mkdir('MEM_file')
    #         elif not isdir('MEM_file'):
    #             mkdir('MEM_file')
    #         if not exists(f_partage):
    #             with open(f_partage, 'w', encoding='utf-8') as f:
    #                 f.write('')
    #         if not exists(f_sauvegarde):
    #             with open(f_sauvegarde, 'w', encoding='utf-8') as f:
    #                 f.write('')
    #         if not exists(f_dirImport):
    #             with open(f_dirImport, 'w', encoding='utf-8') as f:
    #                 f.write('')
    #         if not exists(f_dirImportVente):
    #             with open(f_dirImportVente, 'w', encoding='utf-8') as f:
    #                 f.write('')
    #         if not exists(f_nameImport):
    #             with open(f_nameImport, 'w', encoding='utf-8') as f:
    #                 f.write('')
    #         if not exists(f_ticket):
    #             with open(f_ticket, 'w', encoding='utf-8') as f:
    #                 f.write('')
    #         if not exists(f_base):
    #             with open(f_base, 'w', encoding='utf-8') as f:
    #                 f.write('baseX')
    #         with open(f_base, 'r', encoding='utf-8') as f:
    #             nom = f.readline()
    #         if not nom.strip():
    #             nom = "baseX"

    #     except OSError as error:
    #         print(error)
    #         # a revoir commentaire avant de débuter
    #         return False
    #     else:
    #         # database initiale
    #         self.fix_database(nom)

    # def create_article(self):
    #     chaine = """CREATE TABLE IF NOT EXISTS article (
    #                 art_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    #                 code TEXT,
    #                 des TEXT,
    #                 cat_id INTEGER,        
    #                 pv INTEGER,
    #                 stockmin INTEGER DEFAULT 0,
    #                 envente INTEGER DEFAULT 1,
    #                 ad INTEGER,
    #                 FOREIGN KEY(cat_id) REFERENCES categorie(cat_id))"""
    #     self.curseur.execute(chaine)
    #     self.enregistrer()
       