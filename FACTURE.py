
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
        self.width = None
        self.id = None #id de la facture à afficher
        self.nbr = None #numéro de la facture à afficher
        self.statut = None
        
        self.height = None
        self.number = 0  # numéro de la facture actuelle (0 donc pas de facture)
        self.color = CONST.VERT
        #self.id_lastFacture = None
        
        # construis une chaine à partir d'un tuple x (éléments de la box)
        # self.f=lambda x : f"{x[0]:^15}   {x[1]:^30}   {x[2]:^10}   {x[3]:^5}   {x[4]:^10}   {x[5]:^10}" 
        
        # variables des widgets
        self.entry1_var = StringVar()
        self.entry2_var = StringVar()
        self.entry3_var = StringVar()
        self.entry4_var = StringVar()
        self.entry5_var = StringVar()
        self.entryTotal_var = StringVar()
        self.entryRecu_var = StringVar()
        self.entrySolde_var = StringVar()
        self.listBox_var = StringVar()
        self.entryPU_var = StringVar()
        self.entryQTE_var = StringVar()
        self.entryCode_var = StringVar()
        self.entryRemise_var = StringVar()
        self.entryPrix_var = StringVar()
        self.entryDescription_var = StringVar()
        self.listBox_var = StringVar()
        self.listBox2_var = StringVar()
        self.listBox3_var = StringVar()
        
        self.compoUI() # définition des widgets
        self.liens() # ajout des widgets au thème
        
    def liens(self):
        # ajout des liens 
        # self.bind_all("<Control-q>", lambda e: self.boss.boss.display('afficher la salle'))
        
        self.buttonValider.bind('<FocusIn>', self.colorValider)
        self.buttonValider.bind('<FocusOut>', self.colorValider)
        
        self.button1.bind('<ButtonRelease-1>', lambda _: self.clic.getFacture(self.entry1_var.get().strip())) # clic sur go (facture)
        # self.listBox.bind('<<ListboxSelect>>', self.commandListBox)
        # self.listBox.bind('<Return>', self.returnListBox) 
        self.button5.bind('<ButtonRelease-1>', lambda _: self.clic.goTransfert(destination=self.entry5_var,
                                                                               bouton5 = self.button5,
                                                                               nbr = self.entry1_var,
                                                                               listBox_var=self.listBox_var)) # clic sur go (transfert)
        
        self.buttonFacturer.bind('<ButtonRelease-1>', lambda _:self.clic.commandFacturer(table=self.entry2_var, 
                                                                          service=self.entry3_var,
                                                                          nbr=self.entry1_var,
                                                                          recu = self.entryRecu_var,
                                                                          listBox_var=self.listBox_var,
                                                                          listBox2_var = self.listBox2_var,
                                                                          b=self.buttonFacturer))
        
        self.buttonTerminer.bind('<ButtonRelease-1>', lambda _:self.clic.commandTerminer(solde=self.entrySolde_var,
                                                                          nbr=self.entry1_var,
                                                                          recu = self.entryRecu_var,
                                                                          entrySolde=self.entrySolde,
                                                                          service = self.entry3_var,
                                                                          total = self.entryTotal_var,
                                                                          table = self.entry2_var,
                                                                          b=self.buttonTerminer))
        
        self.buttonModifier.bind('<ButtonRelease-1>', lambda _: self.clic.commandModifier(b=self.buttonModifier))
        
        self.buttonValider.bind('<ButtonRelease-1>', lambda _: self.clic.commandValider(table=self.entry2_var, 
                                                                          service=self.entry3_var,
                                                                          code=self.entryCode_var,
                                                                          description=self.entryDescription_var,
                                                                          statut=self.entry4_var,
                                                                          pu=self.entryPU_var,
                                                                          qte=self.entryQTE_var,
                                                                          remise=self.entryRemise_var,
                                                                          prix=self.entryPrix_var,
                                                                          nbr=self.entry1_var,
                                                                          recu = self.entryRecu_var,
                                                                          b=self.buttonValider)) 
        
        self.buttonValider.bind('<Return>', lambda _: self.clic.commandValider(table=self.entry2_var, 
                                                                          service=self.entry3_var,
                                                                          code=self.entryCode_var,
                                                                          description=self.entryDescription_var,
                                                                          statut=self.entry4_var,
                                                                          pu=self.entryPU_var,
                                                                          qte=self.entryQTE_var,
                                                                          remise=self.entryRemise_var,
                                                                          prix=self.entryPrix_var,
                                                                          nbr=self.entry1_var,
                                                                          recu = self.entryRecu_var,
                                                                          b=self.buttonValider))
        
        self.buttonEffacer.bind('<ButtonRelease-1>', lambda _: self.clic.commandDelete())
        
        self.entry3.bind('<Return>', lambda _ : self.clic.commandService(entry3_var=self.entry3_var,
                                                                         entry3=self.entry3,
                                                                         listBox3 = self.listBox3,
                                                                         listBox3_var = self.listBox3_var,
                                                                         entryCode=self.entryCode))
        
        
        self.listBox.bind('<<ListboxSelect>>', lambda _: self.clic.commandLB(listBox=self.listBox,
                                                                             listBox_var=self.listBox_var,
                                                                             code_var = self.entryCode_var,
                                                                             description_var = self.entryDescription_var,
                                                                             pu_var = self.entryPU_var,
                                                                             qte_var = self.entryQTE_var,
                                                                             remise_var = self.entryRemise_var,
                                                                             prix_var = self.entryPrix_var,
                                                                             code = self.entryCode,
                                                                             description = self.entryDescription,
                                                                             pu = self.entryPU,
                                                                             qte = self.entryQTE,
                                                                             remise = self.entryRemise,
                                                                             prix = self.entryPrix))
        
        self.listBox3.bind('<Return>', lambda _: self.clic.commandLB3(service=self.entry3_var,
                                                                                listBox3 = self.listBox3,
                                                                                listBox3_var = self.listBox3_var,
                                                                                entryCode=self.entryCode)) 
        self.listBox3.bind('<FocusOut>', self.deleteLB23)
        
        self.entryCode.bind('<Return>', lambda _: self.clic.commandCode(code_var=self.entryCode_var,
                                                                         code=self.entryCode,
                                                                         pu_var=self.entryPU_var,
                                                                         qte_var=self.entryQTE_var,
                                                                         qte=self.entryQTE,
                                                                         remise_var=self.entryRemise_var,
                                                                         listBox2=self.listBox2,
                                                                         listBox2_var=self.listBox2_var,
                                                                         description_var=self.entryDescription_var,
                                                                         prix_var=self.entryPrix_var))
        
        
        
       
        self.listBox2.bind('<Return>', lambda _: self.clic.commandLB2(code_var=self.entryCode_var,
                                                                         code=self.entryCode,
                                                                         pu_var=self.entryPU_var,
                                                                         qte_var=self.entryQTE_var,
                                                                         qte=self.entryQTE,
                                                                         remise_var=self.entryRemise_var,
                                                                         listBox2=self.listBox2,
                                                                         listBox2_var=self.listBox2_var,
                                                                         description_var=self.entryDescription_var,
                                                                         prix_var=self.entryPrix_var))
        
        self.listBox2.bind('<FocusOut>', self.deleteLB23)
        
        self.entryQTE.bind('<Return>', lambda _: self.clic.commandPrix(pu=self.entryPU_var,
                                                                         entryQTE=self.entryQTE,
                                                                         entryRemise=self.entryRemise,
                                                                         entryPU=self.entryPU,
                                                                         qte=self.entryQTE_var,
                                                                         remise=self.entryRemise_var,
                                                                         prix=self.entryPrix_var,
                                                                         entryPrix=self.entryPrix))
        
        self.entryQTE.bind('<Tab>', lambda _: self.clic.commandPrix(pu=self.entryPU_var,
                                                                         entryQTE=self.entryQTE,
                                                                         entryRemise=self.entryRemise,
                                                                         entryPU=self.entryPU,
                                                                         qte=self.entryQTE_var,
                                                                         remise=self.entryRemise_var,
                                                                         prix=self.entryPrix_var,
                                                                         entryPrix=self.entryPrix))
        
        self.entryRemise.bind('<Return>', lambda _: self.clic.commandPrix(pu=self.entryPU_var,
                                                                         entryQTE=self.entryQTE,
                                                                         entryRemise=self.entryRemise,
                                                                         entryPU=self.entryPU,
                                                                         qte=self.entryQTE_var,
                                                                         remise=self.entryRemise_var,
                                                                         prix=self.entryPrix_var,
                                                                         entryPrix=self.entryPrix))
        
        self.entryRemise.bind('<Tab>', lambda _: self.clic.commandPrix(pu=self.entryPU_var,
                                                                         entryQTE=self.entryQTE,
                                                                         entryRemise=self.entryRemise,
                                                                         entryPU=self.entryPU,
                                                                         qte=self.entryQTE_var,
                                                                         remise=self.entryRemise_var,
                                                                         prix=self.entryPrix_var,
                                                                         entryPrix=self.entryPrix))
        
        
        self.entryPU.bind('<Return>', lambda _: self.clic.commandPrix(pu=self.entryPU_var,
                                                                         entryQTE=self.entryQTE,
                                                                         entryRemise=self.entryRemise,
                                                                         entryPU=self.entryPU,
                                                                         qte=self.entryQTE_var,
                                                                         remise=self.entryRemise_var,
                                                                         prix=self.entryPrix_var,
                                                                         entryPrix=self.entryPrix))
        
        self.entryPU.bind('<Return>', lambda _: self.clic.commandPrix(pu=self.entryPU_var,
                                                                         entryQTE=self.entryQTE,
                                                                         entryRemise=self.entryRemise,
                                                                         entryPU=self.entryPU,
                                                                         qte=self.entryQTE_var,
                                                                         remise=self.entryRemise_var,
                                                                         prix=self.entryPrix_var,
                                                                         entryPrix=self.entryPrix))
        
        
        self.entryRecu.bind('<Return>', lambda _: self.clic.commandRecu(recu=self.entryRecu_var))
       
    def focusEntryCode(self):
        if self.entryCode['state'] == NORMAL:
            self.entryCode.focus_set() 
            self.entryCode.icursor(END)
            
    def focusEntryService(self):
        if self.entry3['state'] == NORMAL:
            self.entry3.focus_set() 
            self.entry3.icursor(END)
            
    def getEntryService(self):
        return self.entry3_var.get()
        
    def getId(self):
        """id de la facture en cours, None si aucune
        """
        return self.id 
    
    def getN(self):
        """retourne le numero de facture correspondant à l'id, ne pas confondre avec getNbr qui est pour le entry
        """
        return self.nbr
      
    
    def setDb(self, db):
        self.db = db
        
    def setId(self, tup, tablename):
        """fixe le numéro de la facture, le nom de la table, le statut et le service

        Args:
            tup (tuple): (fact_id, nbr, serve, couleur,x1, y1, tablename, recu, solde)
            tablename (str) : nom de la table ou ''
        """
        self.fact = tup
        self.id = self.fact[0]
        self.nbr = self.fact[1]
        self.setStatut(tup[3])
        if self.statut == VERT or self.statut == VERT2:
            # récupération dans le bac des informations de table et service
            
            self.entry1_var.set(str(tup[1])) # indique le numéro de facture 
            self.entry2_var.set(tablename) # indique la table
            # affiche le service correspondant à la table
            self.entry3_var.set(self.db.base10(tablename))
        
        else: # facture orange ou rouge: récupération dans la facture du service et de la table (enregistré lors de la facturation)
            serve, tableName = tup[2], tup[6] 
            self.entry1_var.set(str(tup[1])) # indique le numéro de facture 
            self.entry2_var.set(tableName)
            self.entry3_var.set(serve)
            
        # affiche le reçu et le solde
        recu, solde = tup[7], tup[8]
        self.entryRecu_var.set(self.clic.formatNumber(recu))
        if self.statut == ROUGE: # le solde est uniquement à afficher lorsque la facture est rouge 
            self.entrySolde_var.set(self.clic.formatNumber(solde))
            self.entrySolde.configure(disabledbackground=self.clic.th.getColorNormal(choix = "disabledbackground"))
        
        else: # suppression du solde si pas rouge et affichage normal du bg
            self.entrySolde_var.set('')
            self.entrySolde.configure(disabledbackground=self.clic.th.getColorNormal(choix = "disabledbackground"))
    
    def deleteSolde(self):
        self.entrySolde_var.set('')
        self.entrySolde.configure(disabledbackground=self.clic.th.getColorNormal(choix = "disabledbackground"))
        #self.clic.db.deleteSolde()
        
    def deleteTransfert(self):
        self.entry5_var.set('')
    
    def getStatut(self):
        return self.statut
    
    def setStatut(self, statut_new):
        if statut_new == ORANGE:
            self.entryCode.configure(state=DISABLED)
            self.entryPU.configure(state=DISABLED)
            self.entryQTE.configure(state=DISABLED)
            self.entryRemise.configure(state=DISABLED)
            self.buttonEffacer.configure(state=DISABLED)
            self.buttonValider.configure(state=DISABLED)
            self.entry3.configure(state=DISABLED)
            self.entry5.configure(state=DISABLED)
            self.entryRecu.configure(state=NORMAL)
            self.buttonModifier.configure(state=NORMAL)
            self.buttonFacturer.configure(state=NORMAL)
            self.buttonTerminer.configure(state=NORMAL, text = "TERMINER")
            self.button5.configure(state=DISABLED)
            self.listBox.configure(state=DISABLED)
            # modification dans la database
            self.clic.db.recordStatut(self.id, ORANGE)
                
        elif statut_new == VERT:
            self.entryCode.configure(state=NORMAL)
            self.entryPU.configure(state=NORMAL)
            self.entryQTE.configure(state=NORMAL)
            self.entryRemise.configure(state=NORMAL)
            self.buttonEffacer.configure(state=NORMAL)
            self.buttonValider.configure(state=NORMAL)
            self.entry3.configure(state=NORMAL)
            self.entry5.configure(state=NORMAL)
            self.entryRecu.configure(state=NORMAL)
            self.buttonModifier.configure(state=DISABLED)
            self.buttonFacturer.configure(state=NORMAL)
            self.buttonTerminer.configure(state=DISABLED, text = "TERMINER")
            self.button5.configure(state=NORMAL)
            self.listBox.configure(state=NORMAL)
            # modification dans la database
            self.clic.db.recordStatut(self.id, VERT)
            
        elif statut_new == VERT2:
            self.entryCode.configure(state=NORMAL)
            self.entryPU.configure(state=NORMAL)
            self.entryQTE.configure(state=NORMAL)
            self.entryRemise.configure(state=NORMAL)
            self.buttonEffacer.configure(state=NORMAL)
            self.buttonValider.configure(state=NORMAL)
            self.entry3.configure(state=NORMAL)
            self.entry5.configure(state=DISABLED)
            self.entryRecu.configure(state=NORMAL)
            self.buttonModifier.configure(state=DISABLED)
            self.buttonFacturer.configure(state=NORMAL)
            self.buttonTerminer.configure(state=DISABLED, text = "TERMINER")
            self.button5.configure(state=DISABLED)
            self.listBox.configure(state=NORMAL)
            # modification dans la database
            self.clic.db.recordStatut(self.id, VERT2)
            
        elif statut_new == ROUGE:
            self.entryCode.configure(state=DISABLED)
            self.entryPU.configure(state=DISABLED)
            self.entryQTE.configure(state=DISABLED)
            self.entryRemise.configure(state=DISABLED)
            self.buttonEffacer.configure(state=DISABLED)
            self.buttonValider.configure(state=DISABLED)
            self.entry3.configure(state=DISABLED)
            self.entry5.configure(state=DISABLED)
            self.entrySolde.configure(state=DISABLED)
            self.entryRecu.configure(state=DISABLED)
            self.buttonModifier.configure(state=DISABLED)
            self.buttonFacturer.configure(state=DISABLED)
            self.buttonTerminer.configure(state=NORMAL, text = "TICKET")
            self.button5.configure(state=DISABLED)
            self.listBox.configure(state=DISABLED)
            # modification dans la database
            self.clic.db.recordStatut(self.id, ROUGE)
         
        else: # absence de statut
            self.entryCode.configure(state=DISABLED)
            self.entryPU.configure(state=DISABLED)
            self.entryQTE.configure(state=DISABLED)
            self.entryRemise.configure(state=DISABLED)
            self.buttonEffacer.configure(state=DISABLED)
            self.buttonValider.configure(state=DISABLED)
            self.entry3.configure(state=DISABLED)
            self.entry5.configure(state=DISABLED)
            self.entrySolde.configure(state=DISABLED)
            self.entryRecu.configure(state=DISABLED)
            self.buttonModifier.configure(state=DISABLED)
            self.buttonFacturer.configure(state=DISABLED)
            self.buttonTerminer.configure(state=DISABLED, text = "TERMINER")
            self.button5.configure(state=DISABLED)
            self.listBox.configure(state=DISABLED)
            # modification dans la database
            self.clic.db.recordStatut(self.id, '')
                                                                                                                                                                                                                    
        self.statut = statut_new
        self.entry4_var.set(DIC_STATUT[self.statut])
        
    def displayVoid():
        
        pass
            
    def eraseEncodage(self):
        """efface la zone d'encodage
        """
        self.entryCode_var.set('')
        self.entryDescription_var.set('')
        self.entryPU_var.set('')
        self.entryQTE_var.set('')
        self.entryRemise_var.set('')
        self.entryPrix_var.set('')
        
    def setTotal(self, total):
        self.entryTotal_var.set(total)
        
    def isEncodageVide(self):
        b = self.entryCode_var.get().strip()
        b += self.entryDescription_var.get().strip()
        b += self.entryPU_var.get().strip()
        b += self.entryQTE_var.get().strip()
        b += self.entryRemise_var.get().strip()
        b += self.entryPrix_var.get().strip()
        return b == ''
    
    def focusValider(self):
        self.buttonValider.focus_set()
    
    def setListBox_var(self, list_recordF):
        """établit la liste dans la box, sur base de la self.list_recordF déjà construite
        """       
        liste=[] # liste qui contiendra les éléments de listBox_var
        
        list_transfert = [] # liste des indice des items transférés
        list_normal = []    # liste des indice des items non transférés
        
        for i, tup in enumerate(list_recordF):
            id, code_id, pu, qte, remise, prix, transfert = tup
            code, description = self.db.getArticle(code_id)
            chaine = code, description, self.clic.formatNumber(pu), str(qte), self.clic.formatNumber(remise), self.clic.formatNumber(prix)
            liste.append(F(chaine))
            if transfert:
                list_transfert.append(i)
            else:
                list_normal.append(i)
                
        self.listBox_var.set(liste)
           
        for i in list_transfert:
            self.listBox.itemconfig(i, foreground=self.clic.th.getForegroundListBox(transfert=1))
        
        for i in list_normal:
            self.listBox.itemconfig(i, foreground=self.clic.th.getForegroundListBox())
        
    def deleteLB23(self, evt=None):
        """efface la list des box 2 et 3
        """
        self.listBox2_var.set([])
        self.listBox3_var.set([])
        
    def getNbr(self):
        """capte le numéro indiqué dans la case facture

        Returns:
            str: numéro de la case N°FACTURE
        """
        return self.entry1_var.get()
       
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
        text1 = F(("CODE", "DESCRIPTION", "P.U.", "QTE", "REMISE", "PRIX"))
        text = F(("CODE + ENTER", "DESCRIPTION", "P.U.", "QTE", "REMISE", "PRIX"))
        self.label7 = Label(self.frameLeft, text = text1, **KW_LABEL)
        self.listBox = Listbox(self.frameLeft, listvariable=self.listBox_var, width=len(text), height=HEIGHT_LISTBOX, **KW_LISTBOX)
        self.label6 = Label(self.frameLeft, text = text, **KW_LABEL)
        line3 = Frame(self.frameLeft)
        self.listBox2 = Listbox(self.frameLeft, listvariable=self.listBox2_var, width=LENGTH_CODE, height=HEIGHT_LISTBOX2, **KW_LISTBOX2)
        sepV2 = Canvas(self.frameLeft, height=0, **KW_CANVAS) #séparateur vertical avant les buttons valider er effacer
        line4 = Frame(self.frameLeft) # contient les buttons effacer et valider
          
        ##composants du line 1
        self.label1 = Label(line1, text = "N°FACTURE", **KW_LABEL)
        self.entry1 = Entry(line1, textvariable=self.entry1_var, width = LENGTH_NUMERO, **KW_ENTRY)
        self.button1 = Button(line1, text="GO", **KW_SMALL_BUTTON)
        
        self.label2 = Label(line1, text = "TABLE", **KW_LABEL)
        self.entry2 = Entry(line1, textvariable=self.entry2_var, width = LENGTH_TABLE, state=DISABLED,**KW_ENTRY)
        
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
        self.entry4 = Entry(line2, textvariable=self.entry4_var, width = LENGTH_ETAT_FACTURE,  state=DISABLED,**KW_ENTRY)
        
        self.listBox3 = Listbox(line2, listvariable=self.listBox3_var, width=LENGTH_WORKER, height=HEIGHT_LISTBOX3, **KW_LISTBOX2)
        
        # composants sous listbox 
        eH = 26 # espacement horizontal entre les entry code, description, ...
        sepH1 = Canvas(line3, width=eH, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        sepH2 = Canvas(line3, width=eH, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        sepH3 = Canvas(line3, width=eH, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        sepH4 = Canvas(line3, width=eH, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        sepH5 = Canvas(line3, width=eH, height=TAILLE_CAR, **KW_CANVAS) #séparateur horizontal
        self.entryCode = Entry(line3, textvariable=self.entryCode_var, width = LENGTH_CODE, **KW_ENTRY)
        self.entryDescription = Entry(line3, textvariable=self.entryDescription_var, width = LENGTH_DESCRIPTION, state=DISABLED, **KW_ENTRY)
        self.entryPU = Entry(line3, textvariable=self.entryPU_var, width = LENGTH_PU, **KW_ENTRY)
        self.entryQTE = Entry(line3, textvariable=self.entryQTE_var, width = LENGTH_QTE, **KW_ENTRY)
        self.entryRemise = Entry(line3, textvariable=self.entryRemise_var, width = LENGTH_PU, takefocus=0, **KW_ENTRY)
        self.entryPrix = Entry(line3, textvariable=self.entryPrix_var, width = LENGTH_PRIX,  state=DISABLED,**KW_ENTRY)
        
        self.buttonEffacer = Button(line4, text = "SUPPRIMER", width= 14, takefocus=0, **KW_BUTTON)
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
        self.entryPrix.pack(side=LEFT,**PAD_ENTRY)
        
        self.buttonEffacer.pack(padx=20, side=LEFT)
        self.buttonValider.pack(padx=20, side=LEFT)
        
        # intégration de la structure en line
        
        line1.pack(pady = 0, fill=X)
        line2.pack(pady = 0, fill=X)
        sepV.pack(pady=5)
        self.label7.pack(padx=5) # titre des colonnes
        self.listBox.pack()
        self.label6.pack(padx=5)
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
        self.buttonModifier = Button(lineB, text = "MODIFIER", state = DISABLED, width= 14, **KW_BUTTON)
        self.labelC = Label(lineC,text = "TOTAL", **KW_LABEL)
        self.entryTotal = Entry(lineC, textvariable=self.entryTotal_var, width = LENGTH_PRIX,  state=DISABLED,**KW_ENTRY)
        self.labelD = Label(lineD,text = "reçu".upper(), **KW_LABEL)
        self.entryRecu = Entry(lineD, textvariable=self.entryRecu_var, width = LENGTH_PRIX,**KW_ENTRY)
        self.labelE = Label(lineE,text = "SOLDE", **KW_LABEL)
        self.entrySolde = Entry(lineE, textvariable=self.entrySolde_var, width = LENGTH_PRIX,  state=DISABLED,**KW_ENTRY)
        self.buttonTerminer = Button(lineF, text = "TERMINER", state = DISABLED, width= 14, **KW_BUTTON)
        
        # integration des widgets
        self.buttonFacturer.pack(side=RIGHT)
        self.buttonModifier.pack(side=RIGHT)
        self.entryTotal.pack(side=RIGHT)
        self.labelC.pack(side=RIGHT, padx=5)
        self.entryRecu.pack(side=RIGHT)
        self.labelD.pack(side=RIGHT, padx=5)
        self.entrySolde.pack(side=RIGHT)
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
        
        self.root.th.add_widget("listBox", self.listBox)
        self.root.th.add_widget("listBox2", self.listBox2)
        self.root.th.add_widget("listBox2", self.listBox3)
        
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
        
        self.root.th.add_widget("label2", self.label7)
        
        self.root.th.add_widget("entry", self.entry1)
        self.root.th.add_widget("entry", self.entry2)
        self.root.th.add_widget("entry", self.entry3)
        self.root.th.add_widget("entry", self.entry4)
        self.root.th.add_widget("entry", self.entry5)
        self.root.th.add_widget("entry", self.entryTotal)
        self.root.th.add_widget("entry", self.entryRecu)
        self.root.th.add_widget("entry", self.entrySolde)
        self.root.th.add_widget("entry", self.entryCode)
        self.root.th.add_widget("entry", self.entryDescription)
        self.root.th.add_widget("entry", self.entryPU)
        self.root.th.add_widget("entry", self.entryQTE)
        self.root.th.add_widget("entry", self.entryPrix)
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
        
    def colorValider(self, evt):
        if self.focus_get() == self.buttonValider:
            if not self.clic.db.isCode(self.entryCode_var.get()):
                self.entryCode.focus_set()
                self.entryCode.icursor(END)
            else:
                self.buttonValider.configure(background=self.clic.th.getValiderFocus(valider=1))
        else:
            self.buttonValider.configure(background=self.clic.th.getValiderFocus(valider=0))