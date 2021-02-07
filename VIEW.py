# -*- coding: utf-8 -*-

# importation des modules
from tkinter import Frame, StringVar, Menu, Menubutton, Label
import tkinter.tix as TIX
import json
import os.path
import CONST
import SALLE
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
        self.th.add_widget("frame", self)
        
        # fixation du theme initial
        self.th.set_theme("")
        
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
        boss.th.add_widget("frame", self)
       
        
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
        self.root.th.add_widget("frame", self)
       
        ## liste des items du menu   
        lst = self.boss.item_lst
        nbr_item = len(lst) # separator inclus
        
        menuButton_lst=[] # liste des menubutton
        menu_lst=[] # liste des menus associés aux menubutton
        barre_lst  = [] # liste des barres verticales
        
        for key, value in self.boss.item_dic.items():
            # titre du menu
            mb= TIX.Menubutton(self, text=key.upper(), **KW_MENUBUTTON)
            menuButton_lst.append(mb)
            mb.pack(**PAD_MENUBUTTON)
            
            # lien du menu avec le menuButton
            me = TIX.Menu(mb, **KW_MENU)
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
                            me.add_command(label = item.capitalize(), underline=0, command=lambda:self.boss.corps.display(lst[0]))
                        elif nbr_item > 1 and item == lst[1]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda:self.boss.corps.display(lst[1]))
                        elif nbr_item > 2 and item == lst[2]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda:self.boss.corps.display(lst[2])) 
                        elif nbr_item > 3 and item == lst[3]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda:self.boss.corps.display(lst[3]))
                        elif nbr_item > 4 and item == lst[4]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda:self.boss.corps.display(lst[4]))    
                        elif nbr_item > 5 and item == lst[5]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda:self.boss.corps.display(lst[5])) 
                        elif nbr_item > 6 and item == lst[6]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda:self.boss.corps.display(lst[6]))
                        elif nbr_item > 7 and item == lst[7]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda:self.boss.corps.display(lst[7]))
                        elif nbr_item > 8 and item == lst[8]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda:self.boss.corps.display(lst[8]))    
                        elif nbr_item > 9 and item == lst[9]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda:self.boss.corps.display(lst[9])) 
                        elif nbr_item > 10 and item == lst[10]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda:self.boss.corps.display(lst[10]))
                        elif nbr_item > 11 and item == lst[11]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda:self.boss.corps.display(lst[11]))
        
        # ajout à droite de la gestion de fenêtre   
        b1 = Button(self, text="X ", command=self.root.croix, **KW_FERMETURE)
        b1.pack(**PAD_FERMETURE)
        b2 = Button(self, text=" —", command=self.root.barre, **KW_FERMETURE)
        b2.pack(**PAD_FERMETURE)
        
        # ajout des widgets au thème
        for mb in menuButton_lst:
            self.root.th.add_widget("menuButton", mb)
        for me in menu_lst:
            self.root.th.add_widget("menu", me)
        self.root.th.add_widget("exit", b1)
        self.root.th.add_widget("exit", b2)
        for barre in barre_lst:
            self.root.th.add_widget("barre", barre)
   
class Corps(Frame):
    def __init__(self, boss):
        Frame.__init__(self, boss)
        
        # configuration
        self.configure()
        self.pack(fill=Y, expand=Y)
        
        #attributs
        self.boss = boss
        self.root = boss.master
        self.root.th.add_widget("frame", self)
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
        self.item = item
        
        # construction du corps
        self.label = Label(self, **KW_TITRE)
        self.canvas=Canvas(self, height=MARGE_HAUTE_SALLE,**KW_CANVAS)
        
        # ajout widget à la base
        self.root.th.add_widget("titre", self.label)
        self.root.th.add_widget("canvas", self.canvas)
        self.root.th.add_widget("frame", self)
         
    def display(self):
        if self.item == "afficher la salle":
            self.canvas.pack()
        else:
            self.label.configure(text=self.item.upper())
            self.label.pack(**PAD_TITRE)
        
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
        self.entry1_var = StringVar()
        self.entry2_var = StringVar()
        self.entry3_var = StringVar()
        self.entry4_var = StringVar()
        self.spinBox_var = StringVar()
        
        # widgets
        ## cadreBox parallèle avec listbox
        cadreBox = Frame(self) 
        label1 = Label(cadreBox, **KW_LABEL)
        self.entry1 = Entry(cadreBox, textvariable=self.entry1_var,**KW_ENTRY)
        self.listBox = Listbox(cadreBox, listvariable=self.listBox_var, **KW_LISTBOX)
        self.listBox.bind('<<ListboxSelect>>', self.commandListBox)
        self.listBox.bind('<Return>', self.returnListBox)   
        
        ## séparateur des cadres parallèles
        canvas = Canvas(self, width=ECART_DOUBLE_CADRE_VERTICAL, **KW_CANVAS) #séparateur
        
        ## cadre  
        cadre = Frame(self)  
        label2 = Label(cadre,**KW_LABEL)
        self.entry2 = Entry(cadre, textvariable=self.entry2_var,**KW_ENTRY)
        label3 = Label(cadre,**KW_LABEL)
        self.entry3 = Entry(cadre, textvariable=self.entry3_var,**KW_ENTRY)
        label4 = Label(cadre,**KW_LABEL)
        self.entry4 = Entry(cadre, textvariable=self.entry4_var,**KW_ENTRY)
        label5 = Label(cadre, **KW_LABEL)
        self.spinBox=Spinbox(cadre, values=(), textvariable=self.spinBox_var, **KW_SPINBOX)
        
        canvas2 = Canvas(cadre, width=10, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        canvas3 = Canvas(cadre, width=10, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        canvas4 = Canvas(cadre, width=10, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        
        ## salle
        self.bac = SALLE.Bac(self, width = self.root.master.winfo_screenwidth()-2*MARGE_SALLE)
         
        # ajout des widgets aux themes
        self.root.th.add_widget("frame", self)
        self.root.th.add_widget("frame", cadreBox)
        self.root.th.add_widget("frame", cadre)
        self.root.th.add_widget("bac", self.bac)
        self.root.th.add_widget("spinBox", self.spinBox)   
        self.root.th.add_widget("canvas", canvas)
        self.root.th.add_widget("canvas", canvas2)
        self.root.th.add_widget("canvas", canvas3)
        self.root.th.add_widget("canvas", canvas4)
        self.root.th.add_widget("label", label1)
        self.root.th.add_widget("label", label2)
        self.root.th.add_widget("label", label3)
        self.root.th.add_widget("label", label4)
        self.root.th.add_widget("label", label5)
        self.root.th.add_widget("entry", self.entry1)
        self.root.th.add_widget("entry", self.entry2)
        self.root.th.add_widget("entry", self.entry3)
        self.root.th.add_widget("entry", self.entry4)
        self.root.th.add_widget("listBox", self.listBox)
        
        # widgets selon l'item
        if self.item == 'ajouter une table':
            cadre.pack(side=LEFT)
            
            label2.configure(text="nom de la table".upper())
            label2.pack(**PAD_LABEL)
            self.entry2.configure(width = LENGTH_TABLE)
            self.entry2.pack(**PAD_ENTRY)
            canvas2.pack()
            
            label3.configure(text="largeur".upper())
            label3.pack(**PAD_LABEL)
            self.entry3.configure(width = LENGTH_DIMENSION_TABLE)
            self.entry3_var.set("1")
            self.entry3.pack(**PAD_ENTRY)
            canvas3.pack()
            
            label4.configure(text="hauteur".upper())
            label4.pack(**PAD_LABEL)
            self.entry4.configure(width = LENGTH_DIMENSION_TABLE)
            self.entry4_var.set("1")
            self.entry4.pack(**PAD_ENTRY)
            canvas4.pack()
            
            label5.configure(text="couleur".upper())
            label5.pack(**PAD_LABEL)
            self.spinBox.pack(**PAD_SPINBOX)
            
        if self.item == "afficher la salle":     
            self.bac.pack(fill=BOTH, expand=1)
            
        if self.item == "modifier le thème": 
            cadreBox.pack(side=LEFT)
            label1.configure(text = "sélection".upper())
            label1.pack(**PAD_LABEL)   
            self.listBox.pack(**PAD_LISTBOX)
            
        elif self.item == "ajouter un employé":
            cadre.pack(side=LEFT)
            
            label2.configure(text="nom de l'employé".upper())
            label2.pack(**PAD_LABEL)
            self.entry2.configure(width = LENGTH_CODE)
            self.entry2.pack(**PAD_ENTRY)
            
        elif self.item == "éditer les employés":
            cadreBox.pack(side=LEFT)           
            canvas.pack(side=LEFT)
            cadre.pack(side=LEFT)
            
            label1.configure(text = "sélection + enter".upper())
            label1.pack(**PAD_LABEL)   
            self.listBox.configure(width=LENGTH_CODE)
            self.listBox.pack(**PAD_LISTBOX)
            label2.configure(text="nom de l'employé".upper())
            label2.pack(**PAD_LABEL)
            self.entry2.configure(width = LENGTH_CODE)
            self.entry2.pack()
            
        elif self.item == "ajouter un article":
            cadre.pack(side=LEFT)
            
            label2.configure(text="code de l'article".upper())
            label2.pack(**PAD_LABEL)
            self.entry2.configure(width = LENGTH_CODE)
            self.entry2.pack(**PAD_ENTRY)
            canvas2.pack()
            
            label3.configure(text="description".upper())
            label3.pack(**PAD_LABEL)
            self.entry3.configure(width = LENGTH_DESCRIPTION)
            self.entry3.pack(**PAD_ENTRY)
            canvas3.pack()
            
            label4.configure(text="prix de vente".upper())
            label4.pack(**PAD_LABEL)
            self.entry4.configure(width = LENGTH_PRIX)
            self.entry4.pack(**PAD_ENTRY)
            
    def display(self):    
        # display selon l'item
        self.root.clic.displayContenu(listBox=self.listBox,
                                      listBox_lst=self.listBox_lst,
                                      listBox_var=self.listBox_var,
                                      entry1=self.entry1,
                                      entry1_var=self.entry1_var,
                                      entry2=self.entry2,
                                      entry2_var=self.entry2_var,
                                      entry3=self.entry3,
                                      entry3_var=self.entry3_var,
                                      entry4=self.entry4,
                                      entry4_var=self.entry4_var,
                                      item=self.item,
                                      bac = self.bac,
                                      spinBox = self.spinBox,
                                      spinBox_var = self.spinBox_var)
        self.pack(fill=Y, expand=Y)
        
    def commandListBox(self, evt):
        w = evt.widget
        self.root.clic.commandListBox(item = self.item,
                                      entry2 = self.entry2,
                                      entry2_var = self.entry2_var,
                                      listBox = w)
    def commandSpinBox(self, evt):
        w = evt.widget
        self.root.clic.commandSpinBox(item = self.item,
                                      spinBox_var = self.spinBox_var,
                                      spinBox = w)
        
        
    def returnListBox(self, evt):
        w = evt.widget
        self.root.clic.returnListBox(item = self.item,
                                     entry2 = self.entry2,
                                     entry2_var = self.entry2_var,
                                     listBox = w)
        
    def hide(self):
        self.pack_forget()
        
class Bouton(Frame):
    def __init__(self, boss, item):
        Frame.__init__(self, boss)
        self.configure()
        
        # attributs
        self.root = boss.master.master
        self.item = item
        
        # widgets
        self.bouton1 = Button(self, width = WIDTH_BUTTON, **KW_BUTTON)
        self.bouton1.bind('<Return>', lambda:(self.commandBouton(1)))
        self.bouton2 = Button(self, width = WIDTH_BUTTON, **KW_BUTTON)
        self.bouton1.bind('<Return>', lambda:(self.commandBouton(2)))
        canvas = Canvas(self, height=self.bouton1.winfo_reqheight(), **KW_CANVAS)  # cas de l'absence de button
        
        # ajout des widgets aux thèmes
        self.root.th.add_widget("frame", self)
        self.root.th.add_widget("button", self.bouton1)
        self.root.th.add_widget("button", self.bouton2)
        self.root.th.add_widget("canvas", canvas)
        
        # widgets selon item
        
        if self.item == "modifier le thème":
            canvas.pack(side=LEFT)
            
        if self.item in {"ajouter un employé", "ajouter une table", "ajouter un article"}:
            self.bouton1.configure(text="ajouter".upper())
            self.bouton1.pack(**PAD_BUTTON)
            
        if self.item == "éditer les employés":
            self.bouton1.configure(text="supprimer".upper())
            self.bouton1.pack(**PAD_BUTTON)
            self.bouton2.configure(text="modifier".upper())
            self.bouton2.pack(**PAD_BUTTON)
        
            
    def display(self):
        self.pack()
        
    def hide(self):
        self.pack_forget()
        
    def commandBouton(self, numeroBouton):
        self.root.clic.commandBouton(contenu = self.boss.contenu[self.item],
                                     numeroBouton=numeroBouton)
        
class Comment(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        
        #configuration
        self.configure()
        self.pack()
        
        # attributs
        self.root = boss.master
        self.root.th.add_widget("frame", self)
        
        self.com = StringVar()
        self.com.set('')
        
        # structure
        label =  Label(self, textvariable= self.com, **KW_COMMENT)
        label.pack(**PAD_COMMENT)
        
        # ajout du label dans le theme
        self.root.th.add_widget("com", label)
       
        
    def fix_comment(self, com):
        self.com.set(com)
    
        



    