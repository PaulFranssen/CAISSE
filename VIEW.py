# -*- coding: utf-8 -*-

# importation des modules
from tkinter import Frame, StringVar, Menu, Menubutton, Label
import json
import os.path
import CONST
from MODEL import *

class PF(Frame):
    def __init__(self, base, boss=None):
        Frame.__init__(self, boss)
        # self.master.colormap = 'red'
        
        # configuration
        self.master.configure()
        self.master.wm_attributes('-fullscreen', 'true')
        self.master.resizable(width=False, height=False)
        self.configure()
        self.pack(fill=BOTH, expand=Y)
        
        # attributs
        self.base = base
        self.cadreGestion = CadreGestion(self)
        
    def display(self, cadre):
        if cadre == "cadreGestion":
            self.cadreGestion.display()
                   
        # w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        # merge_x, merge_y = int((w - 1500) / 2), int((h - 800) / 2)
        # if merge_x < 0 or merge_y < 0:
        #     print('écran non conforme')
        #     # exit(0)
        # # dim = "{}x{}+{}+{}".format(1500, 800, merge_x, merge_y)      
        # # self.master.geometry(dim)
        # # self.master.overrideredirect(True)
        
        # def fix_database(self, database):
        #     self.database.set(database)
        
    def croix(self):
        self.base.fermer()
        self.master.destroy()

    def barre(self):
        self.master.wm_iconify()
        
class CadreGestion(Frame):
    
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.configure()
        
        # attributs
        self.item = StringVar()
        self.item.set("ouvrir")
        
        ## structure générale : entete, cadre, comment
        self.entete = Entete(self)
        self.corps = Corps(self)
        self.corps.display(self.item.get())
        self.comment = Comment(self)
        self.comment.fix_comment('initial')
        
    def display(self):
        self.pack(fill = BOTH, expand = Y)
    
    def hide(self):
        self.pack_forget()

        
class Entete(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        
        # configuration
        self.configure()
        self.pack(fill=X)
        
        # attributs
        self.boss = boss
        self.root = boss.master
        
        # construction des menus
        with open(os.path.join(CONST.DATA_FILE, CONST.MENU_FILE), "r", encoding="utf-8") as read_file:
            data = json.load(read_file)
        
        ## liste des items du menu
        lst = []
        for dic in list(data.values()):
            lst += list(dic.keys())
            
        for key, value in data.items():
            # titre du menu
            mb= Menubutton(self, text=key.upper(), **kw_1)
            mb.pack(**pad_1)
            
            # lien du menu avec le menuButton
            me = Menu(mb, **kw_3)
            mb.configure(menu=me)
            Label(self, **kw_50).pack(side='left') # séparateur vertical entre les menus
            
            # ajout des items de chaque menu
            for cle, item in value.items():
                if cle == "separator":
                    me.add_separator()
                else:
                        if cle == lst[0]:
                            me.add_command(label = cle, underline=0, command=lambda : self.boss.corps.display(lst[0]), **kw_2)
                        elif cle == lst[1]:
                            me.add_command(label = cle, underline=0, command=lambda : self.boss.corps.display(lst[1]), **kw_2)
                        elif cle == lst[2]:
                            me.add_command(label = cle, underline=0, command=lambda : self.boss.corps.display(lst[2]), **kw_2) 
                        elif cle == lst[3]:
                            me.add_command(label = cle, underline=0, command=lambda : self.boss.corps.display(lst[3]), **kw_2)
                        elif cle == lst[4]:
                            me.add_command(label = cle, underline=0, command=lambda : self.boss.corps.display(lst[4]), **kw_2)    
                        
        # ajout à droite de la gestion de fenêtre   
        b1 = Button(self, text="X ", command=self.root.croix, **kw_51)
        b1.pack(padx=5, side=RIGHT)
        b2 = Button(self, text=" —", command=self.root.barre, **kw_51)
        b2.pack(padx=5, side=RIGHT)
        
        
class Corps(Frame):
    def __init__(self, boss):
        Frame.__init__(self, boss)
        
        # configuration
        self.configure()
        self.pack(fill=Y, expand=Y)
        
        #attributs
        self.boss = boss
        self.titre = {}
        self.contenu = {}
        self.bouton = {}
        
        # construction des titres, boutons et contenu
        with open(os.path.join(CONST.DATA_FILE, CONST.MENU_FILE), "r", encoding="utf-8") as read_file:
                data = json.load(read_file)
        for _ , value in data.items():
            for cle, valeur in value.items():
                if cle != "separator":
                    self.titre[cle] = Titre(self, valeur['titre'])
                    self.contenu[cle] = Contenu(self, valeur['contenu'])
                    self.bouton[cle] = Bouton(self, valeur['bouton'])   
        
        # affichage du titre, du contenu et du bouton initiaux
        self.titre[boss.item.get()].display()
        self.contenu[boss.item.get()].display()
        self.bouton[boss.item.get()].display()
        
       
    def display(self, item):
        """affiche les élements du corps relatif à l'item

        Args:
            item (str): item(intitulé d'un item du menu)
        """
        # oublier le titre, contenu et bouton de l'item précédent
        self.titre[self.boss.item.get()].hide()
        self.contenu[self.boss.item.get()].hide()
        self.bouton[self.boss.item.get()].hide()
        
        # modification de l'item en cours
        self.boss.item.set(item)
        
        # affichage du titre, contenu et bouton actuels
        self.titre[item].display()
        self.contenu[item].display()
        self.bouton[item].display()
        
class Titre(Frame):
    def __init__(self, boss, titre):
        Frame.__init__(self, boss)
        self.configure()
        
        # construction du corps
        Label(self, text = titre).pack()
        
    def display(self):
        self.pack()
        
    def hide(self):
        self.pack_forget()
                
class Contenu(Frame):
    def __init__(self, boss, contenu):
        Frame.__init__(self, boss)
        self.configure()
        
        # construction du corps
        Label(self, text = contenu[0]).pack(side=LEFT)
    
    def display(self):
        self.pack(fill=Y, expand=Y)
        
    def hide(self):
        self.pack_forget()
        
class Bouton(Frame):
    def __init__(self, boss, bouton):
        Frame.__init__(self, boss)
        self.configure()
        
        # construction du bouton
        Button(self, text= bouton[0]).pack()
           
    def display(self):
        self.pack()
        
    def hide(self):
        self.pack_forget()

class Comment(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        
        #configuration
        self.configure()
        self.pack()
        
        # attributs
        self.com = StringVar()
        self.com.set('')
        
        # structure
        Label(self, textvariable= self.com).pack()
        
    def fix_comment(self, com):
        self.com.set(com)
    
               
            
            
    
        

                
                
#         # DONNEES
#         mb = Menubutton(self, text="données".upper(), **kw_1)
#         mb.pack(**pad_1)
#         Label(self, **kw_50).pack(side='left')
#         me = Menu(mb, **kw_3)
#         me.add_command(label='Articles', underline=0, command=self.command10, **kw_2)
#         me.add_command(label='Employés', command=self.command22, **kw_2)
#         me.add_command(label='Pin', command=self.command13, **kw_2)
#         mb.configure(menu=me)

#         # ENCODAGE
#         mb = Menubutton(self, text="CAISSE", **kw_1)
#         mb.pack(**pad_1)
#         Label(self, **kw_50).pack(side='left')
#         me = Menu(mb, **kw_3)
#         me.add_command(label='Nouvelle', underline=0, command=self.command3, **kw_2)
#         me.add_command(label='Sélection', underline=0, command=self.command12, **kw_2)
#         me.add_command(label='Cloture', underline=0, command=self.command9, **kw_2)
#         me.add_command(label='état', underline=0, command=self.command9, **kw_2)
#         mb.configure(menu=me)

#         # PARAMETRES
#         mb = Menubutton(self, text="paramètres".upper(), **kw_1)
#         mb.pack(**pad_1)
#         Label(self, **kw_50).pack(side='left')
#         me = Menu(mb, **kw_3)
#         me.add_command(label='Thèmes', underline=0, command=self.command9, **kw_2)
#         self.me2.add_separator()
#         me.add_command(label="Créer database", underline=0, command=self.command16, **kw_2)
#         me.add_command(label='Sélectioner database', underline=0, command=self.command9, **kw_2)
#         self.me2.add_separator()
#         me.add_command(label='Modifier PIN', underline=0, command=self.command9, **kw_2)
#         mb.configure(menu=me)

#         # EXIT
#         b1 = Button(self, text="X ", command=self.command40, **kw_51)
#         b1.pack(padx=5, side=RIGHT)
#         b2 = Button(self, text=" —", command=self.command41, **kw_51)
#         b2.pack(padx=5, side=RIGHT)

#     def active(self, year):
#         # if year != date.today().year:
#         if True:
#             # le premier paramètre me donne l'indice de l'élément dans le menu
#             self.me1.entryconfig(0, foreground=color_33, activeforeground=color_33)
#             self.me1.entryconfig(3, foreground=color_33, activeforeground=color_33)
#             self.me1.entryconfig(5, foreground=color_33, activeforeground=color_33)
#             self.me2.entryconfig(0, foreground=color_33, activeforeground=color_33)
#             self.me2.entryconfig(1, foreground=color_33, activeforeground=color_33)
#         else:
#             self.me1.entryconfig(0, foreground=color_37, activeforeground=color_30)
#             self.me1.entryconfig(3, foreground=color_37, activeforeground=color_30)
#             self.me1.entryconfig(5, foreground=color_37, activeforeground=color_30)
#             self.me2.entryconfig(0, foreground=color_37, activeforeground=color_30)
#             self.me2.entryconfig(1, foreground=color_37, activeforeground=color_30)

#     def add_display(self, number, dis):
#         self.list_display[number] = dis

#     def command0(self):
#         self.list_display[0].display()

#     def command4(self, arg):
#         self.list_display[self.num_display].hide()
#         self.num_display = 4
#         self.list_display[4].display(arg)

#     def command5(self, arg=False):
#         self.list_display[self.num_display].hide()
#         self.num_display = 5
#         self.list_display[5].display(arg)
        



    