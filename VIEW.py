# -*- coding: utf-8 -*-

# importation des modules
from tkinter import Frame, StringVar, Label
import tkinter.tix as TIX
import json
import os.path
import CONST
import SALLE, FACTURE
from MODEL import *
from CTRL import *


class PF(Frame):
    """Classe Principale établissant les liens avec le contôle (clic), le thème (th), le cadre graphique (cadreGestion)

    Args:
        Frame (tk): frame de départ
    """
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
       
        
        # configuration de la fenêtre principale
        self.master.configure()
        self.master.wm_attributes('-fullscreen', 'true')
        self.master.resizable(width=False, height=False)
        self.configure()
        
        # attributs
        self.th = Theme()
        self.clic = Clic(self)
        
        self.cadreGestion = CadreGestion(self)
       
        # ajout du cadre au thème
        self.th.add_widget("frame", self)
        
        # fixation du theme initial
        self.th.set_theme("")
        
        # affichage du cadre principal
        self.pack(fill=BOTH, expand=Y)
       
    def display(self, cadre):
        if cadre == "cadreGestion":
            self.cadreGestion.display()
                   
        # w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        # print(w,h)
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
    """cadre constitué de 3 éléments : Entete (menu), Corps  et Comment (commentaire)

    Args:
        Frame (tk): fenêtre principale
    """
    
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        
        # configuration
        self.configure()
        boss.th.add_widget("frame", self)
       
        # attributs
        self.boss=boss
        self.item = StringVar()  # item est la clé du corps
        self.item.set("afficher la salle") # item de départ
        
        # récupération des différents item dans le fichier JSON
        with open(os.path.join(CONST.DATA_FILE, CONST.MENU_FILE), "r", encoding="utf-8") as read_file:
                self.item_dic = json.load(read_file)
        self.item_lst = []  # liste contenant les item
        for liste in self.item_dic.values():
            self.item_lst += liste
            
       
        
        ## structure générale : entete, cadre, comment
        
        self.entete = Entete(self)
        self.corps = Corps(self)
        self.comment = Comment(self)
    
        # affichage du corps initial
        self.corps.display(self.item.get())
        
        
        # calcul et fixation des dimensions du bac 
        marge = self.entete.b1.winfo_reqheight() + MARGE_HAUTE_SALLE + self.comment.label.winfo_reqheight() + PAD_COMMENT["pady"]*2
        height = self.boss.master.winfo_screenheight() - marge
        self.corps.contenu['afficher la salle'].bac.configure(height = height,
                                                              width =  self.boss.master.winfo_screenwidth()-2*MARGE_SALLE)
        self.corps.contenu['afficher la salle'].bac.setDimensions()
        
        # ajout des tables initiales au bac
        self.corps.contenu['afficher la salle'].bac.displayTablesInit()
        
    def display(self):
        # affichage du cadre
        self.pack(fill = BOTH, expand = 1)
        
    def hide(self):
        self.pack_forget()
     
class Entete(Frame):
    """constitutif du cadre de gestion et contenant le menu

    Args:
        Frame (tk): cadreGestion
    """
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        
        # configuration
        self.configure()
        self.pack(fill=X)
        
        # attributs
        self.boss = boss  # cadreGestion
        self.root = boss.master  # pF
    
        self.dic_position = {}  # clé : item ;  valeur : position (i, j) dans le menu
        self.menu_lst=[] # liste des menus associés aux buttons
        
        self.compoUI()
        
    def compoUI(self):
        """construction du menu
        """
        lst = self.boss.item_lst # liste des items du menu   
        nbr_item = len(lst) # separator inclus
        menuButton_lst=[] # liste des menubutton     
        barre_lst  = [] # liste des barres verticales
        
        for i, (key, value) in enumerate(self.boss.item_dic.items()):
            # titre du menu
            mb= TIX.Menubutton(self, text=key.upper(), **KW_MENUBUTTON)
            menuButton_lst.append(mb)
            mb.pack(**PAD_MENUBUTTON)
            
          
            
            # lien du menu avec le menuButton
            me = TIX.Menu(mb, **KW_MENU)
            self.menu_lst.append(me)
            mb.configure(menu=me)
            barre_verticale = Label(self, **KW_BARRE_VERTICALE)
            barre_lst.append(barre_verticale)
            barre_verticale.pack(side='left') # séparateur vertical entre les menus
            
            # ajout des items de chaque menu
            for j, item in enumerate(value):
                self.dic_position[item] = i, j
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
                        elif nbr_item > 12 and item == lst[12]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda:self.boss.corps.display(lst[12]))
                        elif nbr_item > 13 and item == lst[13]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda:self.boss.corps.display(lst[13]))
                        elif nbr_item > 14 and item == lst[14]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda:self.boss.corps.display(lst[14]))
                        elif nbr_item > 15 and item == lst[15]:
                            me.add_command(label = item.capitalize(), underline=0, command=lambda:self.boss.corps.display(lst[15]))
        
        # ajout à droite de la gestion de fenêtre   
        self.b1 = Button(self, text="X ", command=self.root.croix, **KW_FERMETURE)
        self.b1.pack(**PAD_FERMETURE)
        
       
        self.b2 = Button(self, text=" —", command=self.root.barre, **KW_FERMETURE)
        self.b2.pack(**PAD_FERMETURE)
        
        # ajout des widgets au thème
        self.root.th.add_widget("frame", self)
        for mb in menuButton_lst:
            self.root.th.add_widget("menuButton", mb)
        for me in self.menu_lst:
            self.root.th.add_widget("menu", me)
        self.root.th.add_widget("exit", self.b1)
        self.root.th.add_widget("exit", self.b2)
        for barre in barre_lst:
            self.root.th.add_widget("barre", barre)
            
    def desactive_item(self, item):
        
        """désactive l'item dans le menu

        Args:
            item (str): item à désactiver
        """
        i, j = self.dic_position[item]
        self.menu_lst[i].entryconfig(j, state = 'disabled')
        
    def active_item(self, item):
        """désactive l'item dans le menu

        Args:
            item (str): item à activer
            
        """
        i, j = self.dic_position[item]
        self.menu_lst[i].entryconfig(j, state = 'normal')
          
class Corps(Frame):
    """éléments du cadre Gestion et contenant un dictionnaire de Titre, Contenu et Bouton, item étant la clé

    Args:
        Frame (tk): cadreGestion
    """
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
            
            # cas particulier de la salle
            self.canvas.pack()
            
        else:
            
            # cas général
            self.label.configure(text=self.item.upper())
            self.label.pack(**PAD_TITRE)
        
        self.pack()
        
    def hide(self):
        self.pack_forget()
                
class Contenu(Frame):
    """constitutif du corps, contient les widgets entre le Titre et le Bouton

    Args:
        Frame (tk): corps
    """
    def __init__(self, boss, item):
        Frame.__init__(self, boss)
        self.configure()
        
       
        # attributs
        self.boss = boss
        self.root = boss.master.master
        self.item = item
        
        self.compoUI()
        
    def compoUI(self):
        """Ajout des widgets au contenu
        """
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
        
       
        
        
   
        ## salle : contenu particulier car il n' a ni titre ni bouton 
       
       
       # facture
        self.fac = FACTURE.Fac(self)
        self.bac = SALLE.Bac(self, width=0, height=0)
        # liens entre objets
        
        
        # intégration des widgets selon l'item
        if self.item == 'nouvelle caisse':
        
            pass

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
            lst = self.root.th.getColorTable()
            wdth = 0
            for elem in lst:
                wdth = max(wdth, len(elem))
            self.spinBox.configure(values=lst, width = wdth + 2)
            self.spinBox_var.set(value=lst[0])
            self.spinBox.pack(**PAD_SPINBOX)
            
        if self.item == "afficher la salle":  
            # affichage du bac   
            self.bac.pack(fill=BOTH, expand=1)
            
            # ajout du canvas au root.clic
            self.root.clic.setBac(self.bac)
            
        if self.item == "facturation":
            # affichage de la facture
            # cadre.pack(side = LEFT)
            self.fac.pack(side=LEFT)
            # ajout du canvas au root.clic
            self.root.clic.setFac(self.fac)  
            
                            
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
            
         # ajout des widgets aux themes
        self.root.th.add_widget("frame", self)
        self.root.th.add_widget("frame", cadreBox)
        self.root.th.add_widget("frame", cadre)
        self.root.th.add_widget("bac", self.bac)
        self.root.th.add_widget("frame", self.fac)
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
                                      fac = self.fac,                          
                                      spinBox = self.spinBox,
                                      spinBox_var = self.spinBox_var)
        
        # affichage
        if self.item =="afficher la salle":
            self.pack()
        else:      
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
        self.boss = boss
        self.item = item
        
        # widgets
        self.bouton1 = Button(self, width = WIDTH_BUTTON, **KW_BUTTON)
        self.bouton1.bind('<Return>', lambda _:(self.commandBouton(1)))
        self.bouton1.bind('<ButtonRelease-1>', lambda _:(self.commandBouton(1)))
        self.bouton2 = Button(self, width = WIDTH_BUTTON, **KW_BUTTON)
        self.bouton2.bind('<Return>', lambda _:(self.commandBouton(2)))
        self.bouton2.bind('<ButtonRelease-1>', lambda _:(self.commandBouton(2)))
        canvas = Canvas(self, height=self.bouton1.winfo_reqheight(), **KW_CANVAS)  # cas de l'absence de button
        
        # ajout des widgets aux thèmes
        self.root.th.add_widget("frame", self)
        self.root.th.add_widget("button", self.bouton1)
        self.root.th.add_widget("button", self.bouton2)
        self.root.th.add_widget("canvas", canvas)
        
        # widgets selon item
        if self.item == "nouvelle caisse":
            self.bouton1.configure(text="commencer".upper())
            self.bouton1.pack(**PAD_BUTTON)
        
        if self.item == "modifier le thème":
            canvas.pack(side=LEFT)
            
        # if self.item == "facturation":
        #     self.bouton1.configure(text="retour".upper())
        #     self.bouton1.pack(**PAD_BUTTON)
            
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
        self.com = StringVar()
        self.com.set('  ')
        
        # liaison du com avec clic
        self.root.clic.setCom(self.com)
        
        # structure
        self.label =  Label(self, textvariable= self.com, **KW_COMMENT)
        self.label.pack(**PAD_COMMENT)
        
        # ajout des wdgets dans le theme
        self.root.th.add_widget("com", self.label)
        self.root.th.add_widget("frame", self)
       
    def fix_comment(self, com):
        self.com.set(com)
    
        



    