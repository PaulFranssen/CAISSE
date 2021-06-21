
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
        self.id = None #numéro de la facture à afficher
        
        self.height = None
        self.number = 0  # numéro de la facture actuelle (0 donc pas de facture)
        self.color = CONST.VERT
        self.id_lastFacture = None
        
        # construis une chaine à partir d'un tuple x (éléments de la box)
        self.f=lambda x : f"{x[0]:^15}   {x[1]:^30}   {x[2]:^8}   {x[3]:^5}   {x[4]:^8}   {x[5]:^10}" 
        
        # variables des widgets
        self.entry1_var = StringVar()
        self.entry2_var = StringVar()
        self.entry3_var = StringVar()
        self.entry4_var = StringVar()
        self.entry5_var = StringVar()
        self.entryC_var = StringVar()
        self.entryD_var = StringVar()
        self.entryE_var = StringVar()
        self.listBox_var = StringVar()
        self.entryPU_var = StringVar()
        self.entryQTE_var = StringVar()
        self.entryCode_var = StringVar()
        self.entryRemise_var = StringVar()
        self.entryTotal_var = StringVar()
        self.entryDescription_var = StringVar()
        self.listBox2_var = StringVar()
        self.listBox3_var = StringVar()
        
        self.compoUI() # définition des widgets
    
    def setDb(self, db):
        self.db = db
        
    def setId(self, tup, tablename):
        """fixe le numéro de la facture, le nom de la table, le statut et le service

        Args:
            tup (tuple): (fact_id, nbr, serve, couleur,x1, y1, tablename)
            tablename (str) : nom de la table ou ''
        """
        self.fact = tup
        self.entry1_var.set(str(tup[1])) # indique le numéro de facture 
        self.entry2_var.set(tablename) # indique la table
        self.entry4_var.set(DIC_STATUT[tup[3]]) # fixe le statut d'après la couleur
        
    def commandListBox():
            pass
        
    def returnListBox():
        pass
        
        
        
    def compoUI(self):
        """Ajout des widgets au contenu
        """
        
        # widgets   
        ## cadre gauche et droite avec séparateur
        self.frameLeft = Frame(self) 
        canvas = Canvas(self, width=ECART_DOUBLE_CADRE_VERTICAL, **KW_CANVAS) #séparateur
        self.frameRight = Frame(self)
        
        ## gauche
        
        ##structure en line
        line1 = Frame(self.frameLeft)
        line2 = Frame(self.frameLeft)
        sepV = Canvas(self.frameLeft, height=0, **KW_CANVAS) #séparateur vertical avant listbox
        text = self.f(("CODE", "DESCRIPTION", "P.U.", "QTE", "REMISE", "TOTAL"))
        self.listBox1 = Listbox(self.frameLeft, listvariable=self.listBox_var, width=len(text), height=HEIGHT_LISTBOX, **KW_LISTBOX)
        self.label6 = Label(self.frameLeft, text = text, **KW_LABEL)
        line3 = Frame(self.frameLeft)
        self.listBox2 = Listbox(self.frameLeft, listvariable=self.listBox2_var, width=LENGTH_CODE, height=HEIGHT_LISTBOX2, **KW_LISTBOX)
        sepV2 = Canvas(self.frameLeft, height=0, **KW_CANVAS) #séparateur vertical avant les buttons valider er effacer
        line4 = Frame(self.frameLeft) # contient les buttons effacer et valider
          
        ##composants du line 1
        self.label1 = Label(line1, text = "N°FACTURE", **KW_LABEL)
        self.entry1 = Entry(line1, textvariable=self.entry1_var, width = LENGTH_NUMERO, **KW_ENTRY)
        self.button1 = Button(line1, text="GO", **KW_SMALL_BUTTON)
        
        self.label2 = Label(line1, text = "TABLE", **KW_LABEL)
        self.entry2 = Entry(line1, textvariable=self.entry2_var, width = LENGTH_TABLE,**KW_ENTRY)
        
        self.label3 = Label(line1, text = " SERVICE", **KW_LABEL)
        self.entry3 = Entry(line1, textvariable=self.entry3_var, width = LENGTH_WORKER,**KW_ENTRY)
        
        self.label5 = Label(line1, text = "TRANSFERT>", **KW_LABEL)
        self.entry5 = Entry(line1, textvariable=self.entry5_var, width = LENGTH_NUMERO, **KW_ENTRY)
        self.button5 = Button(line1, text = "GO", **KW_SMALL_BUTTON)
        
        eH1 = 55 # séparateur dans line1
        sepH6 = Canvas(line1, width=eH1, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        sepH7 = Canvas(line1, width=eH1, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        
        # composants line2
        self.label4 = Label(line2, text = "STATUT", **KW_LABEL)
        self.entry4 = Entry(line2, textvariable=self.entry4_var, width = LENGTH_ETAT_FACTURE, **KW_ENTRY)
        
        self.listBox3 = Listbox(line2, listvariable=self.listBox3_var, width=LENGTH_WORKER, height=HEIGHT_LISTBOX3, **KW_LISTBOX)
        
        # composants sous listbox 
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
        
        self.buttonEffacer = Button(line4, text = "EFFACER", width= 14, **KW_BUTTON)
        self.buttonValider = Button(line4, text = "VALIDER", width= 14, **KW_BUTTON)
       
        # intégration des widgets
        
        # gauche
        # N FACTURE
        eX =1 # écart H du label
        self.label1.pack(side=LEFT, padx=eX, pady=5)
        self.entry1.pack(side=LEFT, **PAD_ENTRY)
        self.button1.pack(side=LEFT, **PAD_SMALL_BUTTON)
        sepH6.pack(side=LEFT)
        # table
        self.label2.pack(side=LEFT, padx=eX, pady=5)
        self.entry2.pack(side=LEFT,**PAD_ENTRY)
        sepH7.pack(side=LEFT)
        # transfert
        self.label5.pack(side=LEFT, padx=0, pady=5)
        self.entry5.pack(side=LEFT, padx=0)
        self.button5.pack(side=LEFT, padx=5, **PAD_SMALL_BUTTON)
        # service 
        self.entry3.pack(side=RIGHT,padx=7)
        self.label3.pack(side=RIGHT,padx=0)
        
        # etat
        self.label4.pack(side=LEFT,padx=eX, pady=5)
        self.entry4.pack(side=LEFT,**PAD_ENTRY)
        # listbox worker
        self.listBox3.pack(side=RIGHT, padx=7)
        
        # sous listbox
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
        
        self.buttonEffacer.pack(padx=20, side=LEFT)
        self.buttonValider.pack(padx=20, side=LEFT)
        
        # intégration de la structure en line
        
        line1.pack(pady = 0, fill=X)
        line2.pack(pady = 0, fill=X)
        sepV.pack(pady=5)
        self.listBox1.pack()
        self.label6.pack(**PAD_LABEL)
        line3.pack()
        self.listBox2.pack(side=LEFT, padx=10, pady=5)
        sepV2.pack(pady=30, fill=X)
        line4.pack()
        
        
       
        # droite
        # structure en line
        lineA = Frame(self.frameRight)
        lineB = Frame(self.frameRight)
        lineC = Frame(self.frameRight)
        lineD = Frame(self.frameRight)
        lineE = Frame(self.frameRight)
        lineF = Frame(self.frameRight)
        sepV3 = Canvas(self.frameRight, width=0, height=0, **KW_CANVAS)
        
        # composants des line
        self.buttonFacturer = Button(lineA, text = "FACTURER", width= 14, **KW_BUTTON)
        self.buttonModifier = Button(lineB, text = "MODIFIER", width= 14, **KW_BUTTON)
        self.labelC = Label(lineC,text = "TOTAL", **KW_LABEL)
        self.entryC = Entry(lineC, textvariable=self.entryC_var, width = LENGTH_PRIX, **KW_ENTRY)
        self.labelD = Label(lineD,text = "RECU", **KW_LABEL)
        self.entryD = Entry(lineD, textvariable=self.entryD_var, width = LENGTH_PRIX,**KW_ENTRY)
        self.labelE = Label(lineE,text = "SOLDE", **KW_LABEL)
        self.entryE = Entry(lineE, textvariable=self.entryE_var, width = LENGTH_PRIX, **KW_ENTRY)
        self.buttonTerminer = Button(lineF, text = "TERMINER", width= 14, **KW_BUTTON)
        
        # integration des widgets
        self.buttonFacturer.pack(side=RIGHT)
        self.buttonModifier.pack(side=RIGHT)
        self.entryC.pack(side=RIGHT)
        self.labelC.pack(side=RIGHT, padx=5)
        self.entryD.pack(side=RIGHT)
        self.labelD.pack(side=RIGHT, padx=5)
        self.entryE.pack(side=RIGHT)
        self.labelE.pack(side=RIGHT, padx=5)
        self.buttonTerminer.pack(side=RIGHT)
        
        #integration des line
        eH2 = 15
        lineA.pack(pady = eH2, fill=X)
        lineB.pack(pady = eH2, fill=X)
        lineC.pack(pady = eH2, fill=X)
        lineD.pack(pady = eH2, fill=X)
        lineE.pack(pady = eH2, fill=X)
        lineF.pack(pady = eH2, fill=X)
        sepV3.pack(pady=50)
        
        
        # integration des cadres principaux gauche et droit
        self.frameLeft.pack(side=LEFT)
        canvas.pack(side=LEFT)
        self.frameRight.pack(side=LEFT)
        
        # liens
        self.button1.bind('<1>', lambda _: self.clic.getFacture(self.entry1_var.get())) # clic sur go (facture)
        self.listBox1.bind('<<ListboxSelect>>', self.commandListBox)
        self.listBox1.bind('<Return>', self.returnListBox)   
        
        # ajouts des widgets au thème
        self.root.th.add_widget("frame", self.frameLeft)
        self.root.th.add_widget("frame", self.frameRight)
        
        self.root.th.add_widget("frame", line1)
        self.root.th.add_widget("frame", line2)
        self.root.th.add_widget("frame", line3)
        self.root.th.add_widget("frame", line4)
        self.root.th.add_widget("frame", lineA)
        self.root.th.add_widget("frame", lineB)
        self.root.th.add_widget("frame", lineC)
        self.root.th.add_widget("frame", lineD)
        self.root.th.add_widget("frame", lineE)
        self.root.th.add_widget("frame", lineF)
        
        self.root.th.add_widget("listBox", self.listBox1)
        self.root.th.add_widget("listBox", self.listBox2)
        self.root.th.add_widget("listBox", self.listBox3)
        
        self.root.th.add_widget("button", self.button1)
        self.root.th.add_widget("button", self.button5)
        self.root.th.add_widget("button", self.buttonValider)
        self.root.th.add_widget("button", self.buttonEffacer)
        self.root.th.add_widget("button", self.buttonFacturer)
        self.root.th.add_widget("button", self.buttonModifier)
        self.root.th.add_widget("button", self.buttonTerminer)
        
        self.root.th.add_widget("label", self.label1)
        self.root.th.add_widget("label", self.label2)
        self.root.th.add_widget("label", self.label3)
        self.root.th.add_widget("label", self.label4)
        self.root.th.add_widget("label", self.label5)
        self.root.th.add_widget("label", self.label6)
        self.root.th.add_widget("label", self.labelC)
        self.root.th.add_widget("label", self.labelD)
        self.root.th.add_widget("label", self.labelE)
        
        self.root.th.add_widget("entry", self.entry1)
        self.root.th.add_widget("entry", self.entry2)
        self.root.th.add_widget("entry", self.entry3)
        self.root.th.add_widget("entry", self.entry4)
        self.root.th.add_widget("entry", self.entry5)
        self.root.th.add_widget("entry", self.entryC)
        self.root.th.add_widget("entry", self.entryD)
        self.root.th.add_widget("entry", self.entryE)
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
        self.root.th.add_widget("canvas", sepV)
        self.root.th.add_widget("canvas", sepV2)
        self.root.th.add_widget("canvas", sepV3)
        self.root.th.add_widget("canvas", canvas)
        
       
    
    