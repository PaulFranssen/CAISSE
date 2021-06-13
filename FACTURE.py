
from tkinter import Frame, StringVar, Label, Entry
import CONST
from MODEL import *


class Fac(Frame):
    """Classe qui représente le contenu d'une facture (pas les buttons)

    Args:
        Frame (Contenu): Héritage de la classe Contenu
    """
    def __init__(self, boss):
        Frame.__init__(self, boss)
        
        # attributs
        self.boss = boss
        self.root = boss.root
        self.clic = self.root.clic
        # self.db = self.clic.db
        self.width = None
        
        self.height = None
        self.number = 0  # numéro de la facture actuelle (0 donc pas de facture)
        self.color = CONST.VERT
        self.id_lastFacture = None
        
        # variables des widgets
        self.entry1_var = StringVar()
        self.entry2_var = StringVar()
        self.entry3_var = StringVar()
        
        # widgets 
        cadre = Frame(self)  
        label1 = Label(cadre,text = "N° FACTURE", **KW_LABEL)
        self.entry1 = Entry(cadre, textvariable=self.entry1_var,**KW_ENTRY)
        label2 = Label(cadre,text = "TABLE",**KW_LABEL)
        self.entry2 = Entry(cadre, textvariable=self.entry2_var,**KW_ENTRY)
        label3 = Label(cadre, text = " Service", **KW_LABEL)
        self.entry3 = Entry(cadre, textvariable=self.entry3_var,**KW_ENTRY)
        
        # configuration des widgets
        self.entry1.configure(width = LENGTH_NUMERO)
        
        # intégration des widgets
        label1.pack(**PAD_LABEL)
        self.entry1.pack(**PAD_ENTRY)
        label2.pack(**PAD_LABEL)
        self.entry2.pack(**PAD_ENTRY)
        label3.pack(**PAD_LABEL)
        self.entry3.pack(**PAD_ENTRY)
        cadre.pack(side=LEFT)
        
       # ajouts des widgets au thème
        self.root.th.add_widget("frame", cadre)
        self.root.th.add_widget("label", label1)
        self.root.th.add_widget("label", label2)
        self.root.th.add_widget("label", label3)
        self.root.th.add_widget("entry", self.entry1)
        self.root.th.add_widget("entry", self.entry2)
        self.root.th.add_widget("entry", self.entry3)
        
    