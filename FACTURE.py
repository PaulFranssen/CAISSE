
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
        
        # construis une chaine à partir d'un tuple x (éléments de la box)
        self.f=lambda x : f"{x[0]:^15}   {x[1]:^30}   {x[2]:^8}   {x[3]:^5}   {x[4]:^8}   {x[5]:^10}" 
        
        self.compoUI() # définition des widgets
    
    def setDb(self, db):
        self.db = db
        
    def commandListBox():
            pass
    def returnListBox():
        pass
        
        
        
    def compoUI(self):
        """Ajout des widgets au contenu
        """
        # variables des widgets
        self.entry1_var = StringVar()
        self.entry2_var = StringVar()
        self.entry3_var = StringVar()
        self.entry4_var = StringVar()
        self.entry5_var = StringVar()
        self.listBox_var = StringVar()
        self.entryPU_var = StringVar()
        self.entryQTE_var = StringVar()
        self.entryCode_var = StringVar()
        self.entryRemise_var = StringVar()
        self.entryTotal_var = StringVar()
        self.entryDescription_var = StringVar()
        self.listBox2_var = StringVar()
        
        # widgets
        
        ## cadre gauche et droite 
        self.frameLeft = Frame(self) 
        canvas = Canvas(self, width=ECART_DOUBLE_CADRE_VERTICAL, **KW_CANVAS) #séparateur
        self.frameRight = Frame(self)
        
        
        ## gauche
        
        ##line
        line1 = Frame(self.frameLeft)
        line2 = Frame(self.frameLeft)
        text = self.f(("CODE", "DESCRIPTION", "P.U.", "QTE", "REMISE", "TOTAL"))
        self.listBox1 = Listbox(self.frameLeft, listvariable=self.listBox_var, width=len(text), height=HEIGHT_LISTBOX, **KW_LISTBOX)
        self.label6 = Label(self.frameLeft, text = text, **KW_LABEL)
        line3 = Frame(self.frameLeft)
        line4 = Frame(self.frameLeft) # contient la listBox2
       
        
        
        ##composants
        self.label1 = Label(line1, text = "N° FACTURE", **KW_LABEL)
        self.entry1 = Entry(line1, textvariable=self.entry1_var, width = LENGTH_NUMERO, **KW_ENTRY)
        self.button1 = Button(line1, text="GO", **KW_SMALL_BUTTON)
        
        
        
        self.label2 = Label(line1, text = "TABLE", **KW_LABEL)
        self.entry2 = Entry(line1, textvariable=self.entry2_var, width = LENGTH_TABLE,**KW_ENTRY)
        
        self.label3 = Label(line1, text = " SERVICE", **KW_LABEL)
        self.entry3 = Entry(line1, textvariable=self.entry3_var, width = LENGTH_WORKER,**KW_ENTRY)
        
        eH = 27
        sepH6 = Canvas(line1, width=eH, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        sepH7 = Canvas(line1, width=eH, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
       
        
        self.label4 = Label(line2, text = "ETAT", **KW_LABEL)
        self.entry4 = Entry(line2, textvariable=self.entry4_var, width = LENGTH_ETAT_FACTURE, **KW_ENTRY)
        
        self.label5 = Label(line1, text = "TRANSERT >", **KW_LABEL)
        self.entry5 = Entry(line1, textvariable=self.entry5_var, width = LENGTH_NUMERO, **KW_ENTRY)
        self.button5 = Button(line1, text = "GO", **KW_SMALL_BUTTON)
        eH = 26 # espacement horizontal entre les entry code, description, ...
        sepH1 = Canvas(line3, width=eH, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        sepH2 = Canvas(line3, width=eH, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        sepH3 = Canvas(line3, width=eH, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        sepH4 = Canvas(line3, width=eH, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        sepH5 = Canvas(line3, width=eH, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        self.entryCode = Entry(line3, textvariable=self.entryCode_var, width = LENGTH_CODE, **KW_ENTRY)
        self.entryDescription = Entry(line3, textvariable=self.entryDescription_var, width = LENGTH_DESCRIPTION, **KW_ENTRY)
        self.entryPU = Entry(line3, textvariable=self.entryPU_var, width = LENGTH_PU, **KW_ENTRY)
        self.entryQTE = Entry(line3, textvariable=self.entryQTE_var, width = LENGTH_QTE, **KW_ENTRY)
        self.entryRemise = Entry(line3, textvariable=self.entryRemise_var, width = LENGTH_PU, **KW_ENTRY)
        self.entryTotal = Entry(line3, textvariable=self.entryTotal_var, width = LENGTH_PRIX, **KW_ENTRY)
        
        self.listBox2 = Listbox(line4, listvariable=self.listBox2_var, width=LENGTH_CODE, height=HEIGHT_LISTBOX2, **KW_LISTBOX)
        self.buttonValider = Button(line4, text = "VALIDER", width= 14, **KW_BUTTON)
       
        
        
        # droite
        
        # label2 = Label(cadre,**KW_LABEL)
        # self.entry2 = Entry(cadre, textvariable=self.entry2_var,**KW_ENTRY)
        # label3 = Label(cadre,**KW_LABEL)
        # self.entry3 = Entry(cadre, textvariable=self.entry3_var,**KW_ENTRY)
        # label4 = Label(cadre,**KW_LABEL)
        # self.entry4 = Entry(cadre, textvariable=self.entry4_var,**KW_ENTRY)
        # label5 = Label(cadre, **KW_LABEL)
        # self.spinBox=Spinbox(cadre, values=(), textvariable=self.spinBox_var, **KW_SPINBOX)
        
        # canvas2 = Canvas(cadre, width=10, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        # canvas3 = Canvas(cadre, width=10, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        # canvas4 = Canvas(cadre, width=10, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal 
        
        # canvas2 = Canvas(cadre, width=10, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
          
        # configuration des widgets
       
        
        # intégration des widgets
        
        # gauche
        # N FACTURE
        self.label1.pack(side=LEFT, **PAD_LABEL)
        self.entry1.pack(side=LEFT, **PAD_ENTRY)
        self.button1.pack(side=LEFT, **PAD_SMALL_BUTTON)
        sepH6.pack(side=LEFT)
        # table
        self.label2.pack(side=LEFT,**PAD_LABEL)
        self.entry2.pack(side=LEFT,**PAD_ENTRY)
        sepH7.pack(side=LEFT)
        # transfert
        self.label5.pack(side=LEFT,**PAD_LABEL)
        self.entry5.pack(side=LEFT,**PAD_ENTRY)
        self.button5.pack(side=LEFT, **PAD_SMALL_BUTTON)
        # service 
        self.entry3.pack(side=RIGHT,**PAD_ENTRY)
        self.label3.pack(side=RIGHT,**PAD_LABEL)
        
        # etat
        self.label4.pack(side=LEFT,**PAD_LABEL)
        self.entry4.pack(side=LEFT,**PAD_ENTRY)
       
        
        self.entryCode.pack(side=LEFT,**PAD_ENTRY)
        sepH1.pack(side=LEFT)
        self.entryDescription.pack(side=LEFT,**PAD_ENTRY)
        sepH2.pack(side=LEFT)
        self.entryPU.pack(side=LEFT,**PAD_ENTRY)
        sepH3.pack(side=LEFT)
        self.entryQTE.pack(side=LEFT,**PAD_ENTRY)
        sepH4.pack(side=LEFT)
        self.entryRemise.pack(side=LEFT,**PAD_ENTRY)
        sepH5.pack(side=LEFT)
        self.entryTotal.pack(side=LEFT,**PAD_ENTRY)
        
        self.listBox2.pack(side = LEFT, **PAD_LISTBOX)
        self.buttonValider.pack(pady = ESPACE_VERTICAL_BUTTON_VALIDER)
        
        line1.pack(pady = 10, fill=X)
        line2.pack(pady = 20, fill=X)
        self.listBox1.pack()
        self.label6.pack(**PAD_LABEL)
        line3.pack()
        line4.pack(padx=10, pady=5, fill=X)
        
        # droite
        
        # integration des cadres gauche et droit
        self.frameLeft.pack(side=LEFT)
        canvas.pack(side=LEFT)
        self.frameRight.pack(side=LEFT)
        
        # liens
        self.listBox1.bind('<<ListboxSelect>>', self.commandListBox)
        self.listBox1.bind('<Return>', self.returnListBox)   
        
        # ajouts des widgets au thème
        self.root.th.add_widget("frame", self.frameLeft)
        self.root.th.add_widget("frame", self.frameRight)
        
        self.root.th.add_widget("frame", line1)
        self.root.th.add_widget("frame", line2)
        self.root.th.add_widget("frame", line3)
        self.root.th.add_widget("frame", line4)
        
        self.root.th.add_widget("listBox", self.listBox1)
        self.root.th.add_widget("listBox", self.listBox2)
        
        self.root.th.add_widget("button", self.button1)
        self.root.th.add_widget("button", self.button5)
        self.root.th.add_widget("button", self.buttonValider)
        
        self.root.th.add_widget("label", self.label1)
        self.root.th.add_widget("label", self.label2)
        self.root.th.add_widget("label", self.label3)
        self.root.th.add_widget("label", self.label4)
        self.root.th.add_widget("label", self.label5)
        self.root.th.add_widget("label", self.label6)
        
        self.root.th.add_widget("entry", self.entry1)
        self.root.th.add_widget("entry", self.entry2)
        self.root.th.add_widget("entry", self.entry3)
        self.root.th.add_widget("entry", self.entry4)
        self.root.th.add_widget("entry", self.entry5)
        self.root.th.add_widget("entry", self.entryCode)
        self.root.th.add_widget("entry", self.entryDescription)
        self.root.th.add_widget("entry", self.entryPU)
        self.root.th.add_widget("entry", self.entryQTE)
        self.root.th.add_widget("entry", self.entryTotal)
        self.root.th.add_widget("entry", self.entryRemise)
        
        self.root.th.add_widget("canvas", sepH1)
        self.root.th.add_widget("canvas", sepH2)
        self.root.th.add_widget("canvas", sepH3)
        self.root.th.add_widget("canvas", sepH4)
        self.root.th.add_widget("canvas", sepH5)
        self.root.th.add_widget("canvas", sepH6)
        self.root.th.add_widget("canvas", sepH7)
       
    
    