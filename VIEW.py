# -*- coding: utf-8 -*-

# importation des modules
from tkinter import Frame, StringVar, Menu, Menubutton, Label
import json
import os.path
import CONST
from MODEL import *
from CTRL import *

class PF(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        # self.master.colormap = 'red'
        
        # configuration
        self.master.configure()
        self.master.wm_attributes('-fullscreen', 'true')
        self.master.resizable(width=False, height=False)
        self.configure()
        self.pack(fill=BOTH, expand=Y)
        
        # attributs
        self.clic = Clic(self)
        self.th = Theme()
        self.cadreGestion = CadreGestion(self)
        
        # ajout du cadre au thème
        self.th.add_frame(self)
        
        # fixation du theme initial
        self.th.modify_theme("")
        
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
        # self.base.fermer()
        self.master.destroy()

    def barre(self):
        self.master.wm_iconify()
        
class CadreGestion(Frame):
    
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        
        # configuration
        self.configure()
        boss.th.add_frame(self)
       
        
        # attributs
        self.item = StringVar()
        self.item.set("ouvrir")
        with open(os.path.join(CONST.DATA_FILE, CONST.MENU_FILE), "r", encoding="utf-8") as read_file:
                self.item_dic = json.load(read_file)
        self.item_lst = []
        for liste in self.item_dic.values():
            self.item_lst += liste
            
        
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
        self.root.th.add_frame(self)
       
        ## liste des items du menu
        
        lst = self.boss.item_lst
        nbr_item = len(lst) # separator inclus
        
        menuButton_lst=[] # liste des menubutton
        menu_lst=[] # liste des menus associés aux menubutton
        barre_lst  = [] # liste es barres verticales
        for key, value in self.boss.item_dic.items():
            # titre du menu
            mb= Menubutton(self, text=key.upper(), **KW_MENUBUTTON)
            menuButton_lst.append(mb)
            mb.pack(**PAD_MENUBUTTON)
            
            # lien du menu avec le menuButton
            me = Menu(mb, **KW_MENU)
            menu_lst.append(me)
            mb.configure(menu=me)
            barre_verticale = Label(self, **KW_BARRE_VERTICALE)
            barre_lst.append(barre_verticale)
            barre_verticale.pack(side='left') # séparateur vertical entre les menus
            
            # ajout des items de chaque menu
            for item in value:
                if item == "separator":
                    me.add_separator()
                else:
                        if nbr_item > 0 and item == lst[0]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda : self.boss.corps.display(lst[0]))
                        elif nbr_item > 1 and item == lst[1]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda : self.boss.corps.display(lst[1]))
                        elif nbr_item > 2 and item == lst[2]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda : self.boss.corps.display(lst[2])) 
                        elif nbr_item > 3 and item == lst[3]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda : self.boss.corps.display(lst[3]))
                        elif nbr_item > 4 and item == lst[4]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda : self.boss.corps.display(lst[4]))    
                        elif nbr_item > 5 and item == lst[5]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda : self.boss.corps.display(lst[5])) 
                        elif nbr_item > 6 and item == lst[6]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda : self.boss.corps.display(lst[6]))
                        elif nbr_item > 7 and item == lst[7]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda : self.boss.corps.display(lst[7]))
                        elif nbr_item > 8 and item == lst[8]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda : self.boss.corps.display(lst[8]))    
                        elif nbr_item > 9 and item == lst[9]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda : self.boss.corps.display(lst[9])) 
                        elif nbr_item > 10 and item == lst[10]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda : self.boss.corps.display(lst[10]))
                        elif nbr_item > 11 and item == lst[11]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda : self.boss.corps.display(lst[11]))
        
        # ajout à droite de la gestion de fenêtre   
        b1 = Button(self, text="X ", command=self.root.croix, **KW_FERMETURE)
        b1.pack(**PAD_FERMETURE)
        b2 = Button(self, text=" —", command=self.root.barre, **KW_FERMETURE)
        b2.pack(**PAD_FERMETURE)
        
        # ajout des widgets au thème
        self.root.th.add_menuButton(menuButton_lst)
        self.root.th.add_menu(menu_lst)
        self.root.th.add_fermeture(b1)
        self.root.th.add_fermeture(b2)
        self.root.th.add_barre(barre_lst)
   
class Corps(Frame):
    def __init__(self, boss):
        Frame.__init__(self, boss)
        
        # configuration
        self.configure()
        self.pack(fill=Y, expand=Y)
        
        #attributs
        self.boss = boss
        self.root = boss.master
        self.root.th.add_frame(self)
        self.titre = {}
        self.contenu = {}
        self.bouton = {}
        
        # construction des titres, boutons et contenu
        for lst in self.boss.item_dic.values():
            for item in lst:
                if item != "separator":
                    self.titre[item] = Titre(self, item)
                    self.contenu[item] = Contenu(self, item)
                    self.bouton[item] = Bouton(self, item)   
        
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
    def __init__(self, boss, item):
        Frame.__init__(self, boss)
        self.configure()
        
        # attributs
        self.root = boss.master.master
        self.root.th.add_frame(self)
        
        # construction du corps
        label = Label(self, text = item.upper(), **KW_TITRE)
        label.pack(**PAD_TITRE)
        
        # ajout widget à la base
        self.root.th.add_titre(label)
        
    def display(self):
        self.pack()
        
    def hide(self):
        self.pack_forget()
                
class Contenu(Frame):
    def __init__(self, boss, item):
        Frame.__init__(self, boss)
        self.configure()
        
        # attributs
        self.boss = boss
        self.root = boss.master.master
        self.item = item
        self.listBox_lst = []
        self.listBox_var = StringVar(value=self.listBox_lst)
        # widgets
        cadre = Frame(self) #cadre adapté au contenu
        cadre.pack(side=LEFT)
        label1 = Label(cadre,text = "sélection".upper(), **KW_LABEL)
        self.listBox = Listbox(cadre, listvariable=self.listBox_var, 
                               command=self.commandListBox, **KW_LISTBOX)
        
        # ajout des widgets aux themes
        self.root.th.add_frame(self)
        self.root.th.add_frame(cadre)
        self.root.th.add_label(label1)
        self.root.th.add_listBox(self.listBox)
        
        
        # affichage des widgets selon l'item
        if self.item == "modifier le thème": 
            
            label1.pack(**PAD_LABEL)   
            self.listBox.pack(**PAD_LISTBOX)
           
        
        
    
    def display(self):    
        self.root.clic.displayContenu(listBox=self.listBox,
                                      listBox_lst=self.listBox_lst,
                                      listBox_var=self.listBox_var,
                                      item=self.item)
        self.pack(fill=Y, expand=Y)
        
    def commandListBox(self):
        self.root.clic.commandListBox(self.item)
        
        
    def hide(self):
        self.pack_forget()
        
class Bouton(Frame):
    def __init__(self, boss, bouton):
        Frame.__init__(self, boss)
        self.configure()
        
        # attributs
        self.root = boss.master.master
        self.root.th.add_frame(self)
        
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
        self.root = boss.master
        self.root.th.add_frame(self)
        
        self.com = StringVar()
        self.com.set('')
        
        # structure
        label =  Label(self, textvariable= self.com, **KW_COMMENT)
        label.pack(**PAD_COMMENT)
        
        # ajout du label dans le theme
        self.root.th.add_com(label)
       
        
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
        



    