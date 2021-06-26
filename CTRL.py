#!/usr/bin/env python

# -*- coding: utf-8 -*-

# importation des modules
from MODEL import Theme
import DB
from CONST import *
import datetime
import time
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
        self.com.set(f"Erreur {self.s} : {self.msg}")
        

class Clic:
    def __init__(self, boss=None):
        self.com = None
        self.boss = boss
        self.db = DB.Database()
        self.bac = None
        self.th = Theme()
        self.list_recordF=[] # liste parallèle à la listBox de la facture
        # self.dat = None # date de la caisse en cours
        self.index_selected = None # index de la ligne sélectionnée dans la box
        
    def setCom(self, com):
        self.com=com
        
    def clearCom(self):
        self.com.set('')
       
    def setBac(self, bac):
        self.bac = bac
        self.bac.setDb(self.db)
        
    def setFac(self, fac):
        self.fac = fac
        self.fac.setDb(self.db)
        
    def isNumber(self, chain):
        """détermine si chain a le format d'un nombre positif, le vide étant considéré comme 0
        """
        res=True
        ch = chain.strip()
        if ch == '':
            # cas du vide (c'est un nombre)
            res = True
        else:
            try:
                # vérifier si sans les points on a un nombre
                ch1 = int(ch.replace('.', ''))
                
                if ch1<0 or ch1>99999999: # le nombre est négatif ou excessif
                    res=False
                else:
                    liste = [(len(ch)-pos)%4 for pos, char in enumerate(ch) if char == '.']
                   
                    if sum(liste): # les positions des '.' n'est pas adéquate
                        res=False 
                    elif ch[0]=='.': # le premier caractère est un point
                        res=False
                    elif len(ch)>7 and len(liste)==1: # manque un point
                        res=False
            except:
                res=False
        return res
    
    def formatNumber(self, chain):
        """renvoie une chaine formatée à partir d'une chaine contenant un nombre
        """
        if type(chain) == int :
            chain=str(chain)
        ch = chain.replace('.','').strip()
        if len(ch) > 6:
            ch = ch[:-6] + '.' + ch[-6:-3] + '.' + ch[-3:]
        elif len(ch) > 3:
            ch = ch[:-3] + '.' + ch[-3:]
        return ch
    
    
    def setCaisse(self, newCaisse):  
        """établit la caisse et affiche les éventuelles factures dans la salle

        Args:
            newCaisse (bool): True s'il sagit d'un démarrage 
        """
        
        # fixe éventuellement la nouvelle caisse
        dat = self.db.base1(newCaisse)
        
        if dat is not None and not newCaisse: # cas d'une caisse relancée (non cloturée)
            
            # récupérer les factures non rouge d'une caisse ouverte
            factures = self.db.base7bis()
        
            # affiche les factures dans la salle s'il y en a
            if factures is not None:
                self.displayFactures(factures)
                
                
    def commandValider(self, **kw):
        # récupérer les variables
        service = kw['service'].get().strip()
        code = kw['code'].get().strip()
        description = kw['description'].get()
        pu=kw['pu'].get().strip()
        qte=kw['qte'].get().strip()
        remise=kw['remise'].get().strip()
        prix=kw['prix'].get().strip()
        statut = kw['statut'].get()
        nbr = kw['nbr'].get().strip()
        recu = kw['recu'].get().strip()
        
        try:
            # vérification du statut
            if statut not in {DIC_STATUT[VERT], DIC_STATUT[VERT2]}:
                raise E(self.com, 'STATUT ' + statut , 'modification non autorisée')
            
            # vérification du N°FACTURE
            test = "nbr"
            nbr1 = int(nbr)
            if self.fac.getN() != nbr1: # le numéro de facture a été changé sans GO
                #vérifier encore le  getNbr() vide (à faire) cas particulier de départ
                raise E(self.com, 'N°FACTURE', 'ne correspond pas à la facture')
            
            test ="service"
            # vérification du service
            if not self.db.isWorker(service):
                raise E(self.com, 'SERVICE', 'inexistant')
            
            test = "reçu"
            if not self.isNumber(recu):
                raise E(self.com, 'RECU', 'non-conforme')
            
            encodageVide = self.fac.isEncodageVide()
            if not encodageVide:
                # vérification du code
                code_id = self.db.code_id(code)
                if not code_id:
                    raise E(self.com, 'CODE', 'inexistant')
                
                # vérification de la description (doit correspondre au code)
                if not self.db.isDescription(code, description):
                    raise E(self.com, 'CODE', 'ne correspond pas à DESCRIPTION')
                
                # vérification du PU (int >=0)
                if not self.isNumber(pu) or not pu:
                    raise E(self.com, 'P.U.', 'non-conforme')
                pu1 = int(pu.replace('.', ''))
                
                # vérification de la quantité
                if not self.isNumber(qte) or not qte or qte == "0" or len(qte)>LENGTH_QTE:
                        raise E(self.com, 'QTE', 'non-conforme')
                qte1 = int(qte.replace('.', ''))
                
                # vérification de la remise
                if not self.isNumber(remise):
                    raise E(self.com, 'REMISE', 'non-conforme')
                remise1 = 0 if remise =='' else int(remise.replace('.',''))
                
                # vérification du prix (doit correspondre pu.qte - remise)
                if not prix or not self.isNumber(prix):
                    raise E(self.com, 'PRIX', 'non-conforme')
                
                # calcul du prix (doit correspondre au prix indiqué)       
                prix1 = pu1*qte1-remise1
                if prix1 != int(prix.replace('.', '')):
                    raise E(self.com, 'PRIX', 'non-conforme')
               
        except E as e:
            e.affiche()
            self.boss.master.after(attenteLongue, self.clearCom)
            
        except:
            if test == "nbr":
                E(self.com, "N°FACTURE", "non-conforme").affiche()
                self.boss.master.after(attenteLongue, self.clearCom)
                
            else:
                E(self.com, "", "?").affiche()
        
        else: # ENREGISTREMENT DES ENTRY VALIDES
            
            # association entre une table et le service
            ## récupérer la table
            tablename = kw['table'].get().strip()
            ## enregistrer le lien table-service (update ou insert) dans la db serve
            self.db.recordInServe(tablename, service)
            
            # récupérer le id de la facture
            #fact_id = self.db.base9(nbr1)[0] # récupère le id de facture
            fact_id = self.fac.getId()
            
            # mise en forme du reçu et enregistrement dans la base
            recu = 0 if recu == '' else int(recu)          
            self.db.setRecu(fact_id, recu)
            kw['recu'].set(self.formatNumber(recu))
            
            # ajout de la ligne dans la table recordF
            if not encodageVide:
                self.db.recordLigne(code_id=code_id,
                                    nbr = nbr1, 
                                    pu=pu1,
                                    qte=qte1,
                                    remise=remise1,
                                    prix=prix1,
                                    transfert=0,
                                    index_selected = self.index_selected)
                # actualisation de la listBox
                self.actualiserListBox(fact_id)
            
            # commentaire OK
            self.com.set('OK')
            self.boss.master.after(attenteLongue, self.clearCom)
    
    def commandFacturer(self):
        # si déjà statut "facturé", alors  juste réimprimer le ticket
        # sinon :
        
        # validation de la facture
        
        # changement de statut > désactivation (inside changement)
        
        # impression du ticket 
        
        # rem : activation désactivation dans le statut (setStatut)
        pass
    
    def commandTerminer(self):    
        # nécessite 2 clics
        # 1er clic : validation du reçu, affichage du solde : si c'est bon passé au second clic
        # 2ème clic : validation du reçu, affichae du reçu : si identique : impression du ticket et passage au ROUGE
        # si code négatif, 2 tickets : 1 ticket client et 1 ticket à garder
        # si ROUGE : uniquement impression du ticket (bouton devient "TICKET")
        
        # rem : si nouvel affichage de facture, alors réinitialiser le 1er clic à zéro
        pass
    def commandDelete(self):
       
        if self.index_selected is None:  # effacer la zone d'encodage
            self.fac.eraseEncodage()
        
        else : # cas d'une sélection en cours
            self.db.deleteRecordF(self.list_recordF[self.index_selected][0]) # suppression dans la base de donnée
            self.actualiserListBox(self.fac.getId())
       
            
    def commandLB(self, **kw):
        """récupère la ligne sélectionnée dans la listBox et l'affiche dans la zone d'encodage
        """       
        tup_selection = kw['listBox'].curselection()
        if tup_selection: # tuple vide si pas de sélection...
            
            i_selection = tup_selection[0]
            # suppression de la couleur de l'ancien item sélectionné
            if self.index_selected is not None:
                kw['listBox'].itemconfig(self.index_selected, foreground = self.th.getColorNormal())
            
            self.index_selected = i_selection
            
            
            # mise en rouge de l'item sélectionné (conservation si autre sélection)
            kw['listBox'].itemconfig(i_selection, foreground = self.th.getColorWarning())
            recordF = self.list_recordF[i_selection] # élement de self.list_recordF : (id, code_id, pu, qte, remise, prix, transfert)
            
            # mise des entry en warning
            #list_wgt = [kw['code'], kw['description'], kw['pu'], kw['qte'], kw['remise'], kw['prix']]
            #self.th.change_theme(list_wgt, "entryWarning")
            
            # copiage des valeurs dans la zone d'encodage
            kw['code_var'].set(self.db.getArticle(recordF[1])[0])
            kw['description_var'].set(self.db.getArticle(recordF[1])[1])
            kw['pu_var'].set(self.formatNumber(recordF[2]))
            kw['qte_var'].set(str(recordF[3]))
            kw['remise_var'].set(self.formatNumber(recordF[4]))
            kw['prix_var'].set(self.formatNumber(recordF[5]))
            
    def commandService(self, **kw):
        
        # établis les éléments de la listbox de service
        begin = kw['entry3_var'].get().strip() # début du nom
        # récupérer les workers dont le nom commencent par begin
        liste = self.db.base11(begin)
        
        if len(liste) == 0:
            # effacer la sélection de la box
            kw['listBox3_var'].set([])
       
        elif len(liste) == 1:
            # un seul nom donc l'afficher
            kw['entry3_var'].set(liste[0])
            kw['entry3'].icursor(END)
            # supprimer les éventuels mots dans la box
            kw['listBox3_var'].set([])
            
        else:
            # plus d'un nom dans la liste, donc les placer dans la listbox3
            kw['listBox3_var'].set(liste)
            kw['listBox3'].selection_clear(0, END)
            kw['listBox3'].selection_set(0)
            kw['listBox3'].focus_set()
            
    def commandCode(self, **kw):
        
        # établis les éléments de la listbox des codes débutant par begin
        begin = kw['code_var'].get().strip() # début du nom
        # récupérer les codes dont le nom commencent par begin
        liste = self.db.base12(begin)
        
        if len(liste) == 0:
            # effacer la sélection de la box
            kw['listBox2_var'].set([])
       
        elif len(liste) == 1:
            # un seul nom donc l'afficher
            kw['code_var'].set(liste[0])
            #kw['entryCode'].icursor(END)
            # supprimer les éventuels mots dans la box
            kw['listBox2_var'].set([])
            # afficher la description et le PU
            kw['description_var'].set(self.db.getDescription(kw['code_var'].get()))
            pu = self.formatNumber(str(self.db.getPU(kw['code_var'].get())))
            kw['pu_var'].set(pu)
            
            # effacer le prix et la remise+++++
            kw['remise_var'].set('')
            kw['prix_var'].set('')
            
             # aller à la quantité
            kw['qte_var'].set('')
            kw['qte'].focus_set()
            
        else:
            # plus d'un nom dans la liste, donc les placer dans la listbox2
            kw['listBox2_var'].set(liste)
            kw['listBox2'].selection_clear(0, END)
            kw['listBox2'].selection_set(0)
            kw['listBox2'].focus_set()
            
    
    def commandLB3(self, **kw):
        listBox3 = kw['listBox3']
        
        # récupérer la sélection (tuple)
        res = listBox3.curselection()
  
        if res:
            # afficher le service par récupération de la sélection
            kw['service'].set(listBox3.get(res[0]))
            
        # effacer la liste de la box
        kw['listBox3_var'].set([]) 
            
            
    def commandLB2(self, **kw):
        listBox2 = kw['listBox2']
        
        # récupérer la sélection (tuple)
        res = listBox2.curselection()
  
        if res:
            # afficher le code 
            kw['code_var'].set(listBox2.get(res[0]))
            
            # afficher la description et le PU
            kw['description_var'].set(self.db.getDescription(kw['code_var'].get()))
            pu = self.formatNumber(str(self.db.getPU(kw['code_var'].get())))
            kw['pu_var'].set(pu)
            
            # effacer le prix
            kw['remise_var'].set('')
            kw['prix_var'].set('')
            
            # aller à la quantité
            kw['qte_var'].set('')
            kw['qte'].focus_set()
            
        # effacer la liste de la box
        kw['listBox2_var'].set([])
        
    def commandPrix(self, **kw):
        """calcul éventuel du prix 
        """
        qte = kw['qte'].get().strip()
        pu = kw['pu'].get().strip()
        remise = kw['remise'].get().strip()
        
        if not remise:
            remise='0'
        
        res = True
        
      
        if not pu or not qte:
            res=False
        elif not self.isNumber(pu) or not self.isNumber(qte) or not self.isNumber(remise): 
            res=False
        elif len(qte)>LENGTH_QTE:
            res=False
        
        if res:
            # calcul d'un prix
            prix = int(qte.replace('.','')) * int(pu.replace('.','')) - int(remise.replace('.',''))
            if prix >=0 and prix <= 99999999:
                # fixer le prix
                kw['prix'].set(self.formatNumber(str(prix)))
                # focus sur le prix
                kw['entryPrix'].focus_set()
            else:
                res=False
        
        if not res:
            # prix annulé
            kw['prix'].set('')
            
                 
    def displayFactures(self, factures):
        # afficher toutes les factures se trouvant dans la database   
        for fact_id, nbr, serve, couleur,x1, y1, tablename in factures:
            # uniquement les vertes et les oranges (à faire)
            self.bac.id_lastFacture = self.bac.create_text(x1, y1,
                                                    fill=couleur, 
                                                    font = self.bac.font_facture, 
                                                    text=str(nbr), 
                                                    tags=("facture", couleur, str(nbr)))   
            self.bac.id_lastObject = self.bac.id_lastFacture
            self.bac.number = max(self.bac.number, nbr)
            
            
            # liens des factures avec le button-2 > gofacture
            # self.bac.tag_bind(self.bac.id_lastFacture, '<Button-2>', lambda _ : self.gofacture((fact_id, nbr, serve, couleur)))
        
    def gofacture(self, tup, tablename):
        """affiche la facturation avec les éléments de la facture

        Args:
            tup (tuple): (fact_id, nbr, serve, couleur, tablename))
        """
       
        # établissement des 2 premières lignes de la facture, du reçu et du solde
        self.fac.setId(tup, tablename)
        
        # actualisation de la listBox
        
        fact_id = tup[0] # récupère le id de facture
        
        self.actualiserListBox(fact_id)
        
        self.boss.cadreGestion.corps.display("facturation")
        
    def actualiserListBox(self, fact_id):
        """actualise la listBox pour une facture fact_id après validation, effacement ou lors de l'affichage de la facture, yc solde et reçu
        """
        if self.index_selected is not None:  # supprime l'éventuelle ligne sélectionnée dans la box
            print('suppression de la ligne rouge', self.index_selected, self.th.getColorNormal())
            self.fac.listBox.itemconfig(self.index_selected, foreground = self.th.getColorNormal())
        
        tup = self.fac.listBox.curselection()
        if tup:
            self.fac.listBox.selection_clear(tup[0])   # effacement de l'éventuelle sélection
                
            
        self.index_selected = None  # initialisation de la ligne sélectionnée précédemment
        
        self.list_recordF = self.db.getList_RecordF(fact_id) # construction de la liste parallèle à listBox_var
        # élement de self.list_recordF : (id, code_id, pu, qte, remise, prix, transfert)
        
        self.fac.setListBox_var(self.list_recordF) # fabrication de la listBox_var
        
        self.fac.eraseEncodage() # effacement de la zone d'encodage
        
        # re-calcul du total
        self.fac.setTotal(self.formatNumber(self.db.getTotal(fact_id)))
            
        
        
    def getFacture(self, nbr):
        """recupère la facture éventuelle de numéro nbr

        Args:
            nbr (str): numéro de la facture
        """
        # vérifier si nbr est un entier
        try:
            nbr = int(nbr)
            facture = self.db.base9(nbr)
            if not facture:
                raise E(self.com, "N°FACTURE", "inexistant")
            
            fact_id, nbr, serve, couleur, x1, y1, tablename, recu, solde = facture
            
        except E as e: 
            e.affiche()
            self.boss.master.after(attenteLongue, self.clearCom)  
        except :
            E(self.com, "N°FACTURE", 'non-conforme').affiche()
            self.boss.master.after(attenteLongue, self.clearCom)  
        else:  
            # récupérer la table si la facture n'est pas rouge
            if couleur != "ROUGE":  # cas d'une facture rouge 
                tablename = self.bac.getTableName(x1, y1)
                #self.fac.setId(facture, tablename) 
 
            self.gofacture(facture, tablename)
        
    def displayContenu(self, **KW):
        if KW['item'] == "ajouter une table":
            self.clearCom()
            KW['entry2_var'].set('')
            KW['entry2'].focus_set()
            

        elif KW['item'] == "afficher la salle":
            
            KW['bac'].focus_set()
            
        elif KW['item'] == "facturation":
            # actualiser la table et le service correspondant
            pass
            
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
            self.clearCom()
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
            self.clearCom()
            KW['entry2_var'].set('')
            KW['entry3_var'].set('')
            KW['entry4_var'].set('')
            KW['entry2'].focus_set()  
            
    def commandBouton(self, contenu, numeroBouton):
        if contenu.item == "nouvelle caisse":
            # désactiver la touche dans le menu
            self.boss.cadreGestion.entete.desactive_item('nouvelle caisse')
            
            # ajouter un id dans la base de données, avec le statut 1 (ouvert)
            self.db.base1(newCaisse = True)
            
            # récupérer le id de la caisse en cours
            
            
            # afficher la salle
            self.boss.cadreGestion.corps.display("afficher la salle")
            
        # if contenu.item == "facturation":
           
           
        #     pass
        #     # afficher la salle
        #     # self.boss.cadreGestion.corps.display("afficher la salle")
            
        if contenu.item == "ajouter un employé":
            nom = contenu.entry2_var.get().strip()
            
            test =''
            try:
                # le nom de l'employé doit être unique
                if self.db.isWorker(nom):
                    raise E(self.com, 'NOM', 'nom déjà utilisé')  
                
                if not nom :
                    raise E(self.com, 'NOM', 'pas de nom')
                
                if len(nom) > LENGTH_WORKER:
                    raise E(self.com, 'NOM', f"nom trop long (max {LENGTH_WORKER} caractères)")
            
            except E as e:
                e.affiche()
                self.boss.master.after(attenteLongue, self.clearCom)
                
            except :
                E(self.com, test, 'non-conforme').affiche()
                self.boss.master.after(attenteLongue, self.clearCom)
                
            else:
                self.db.insertWorker(nom)
                self.com.set('OK')
                self.boss.master.after(attenteCourte, self.clearCom)
              
                
                
            
        if contenu.item == "ajouter une table":
            nom, largeur, hauteur, couleur = contenu.entry2_var.get().strip(), contenu.entry3_var.get().strip(), contenu.entry4_var.get().strip(), contenu.spinBox_var.get()
            table_names = self.bac.find_withtag(nom)
            
            test =''
            try:
                 # le nom de la table doit être unique (utiliser la base de données ou le canvas)               
                if table_names:
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
                self.boss.master.after(attenteLongue, self.clearCom)
                
            except :
                E(self.com, test, 'non-conforme').affiche()
                self.boss.master.after(attenteLongue, self.clearCom)
            
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
                
        if contenu.item == "ajouter un article":
            code, description, prix = contenu.entry2_var.get().strip(), contenu.entry3_var.get().strip(), contenu.entry4_var.get().strip()
            
            test =''
            try:
                 # le code de l'article doit être unique (utiliser la base de données)               
                if self.db.isCode(code):
                    raise E(self.com, 'CODE', 'code déjà utilisé')  
                if not code :
                    raise E(self.com, 'CODE', 'pas de code')
                if len(code) > LENGTH_CODE:
                    raise E(self.com, 'CODE', f"code trop long (max {LENGTH_CODE} caractères)")
                
                if not description :
                    raise E(self.com, 'DESCRIPTION', 'pas de description')
                if len(description) > LENGTH_DESCRIPTION:
                    raise E(self.com, 'DESCRIPTION', f"trop long (max {LENGTH_DESCRIPTION} caractères)")
                
                if not prix :
                        raise E(self.com, 'PRIX', 'pas de prix')
                if len(prix) > LENGTH_PRIX:
                    raise E(self.com, 'PRIX', f"trop long (max {LENGTH_PRIX} caractères)")
                
                prix = float(prix)
                if prix < 0:
                    raise E(self.com, 'PRIX', f"prix négatif")
                
            except E as e:
                e.affiche()
                self.boss.master.after(attenteLongue, self.clearCom)
                
            except:
                E(self.com, test, 'non-conforme').affiche()
                self.boss.master.after(attenteLongue, self.clearCom)
            else:    
                
                # ajouter l'aricle
                self.db.insertArticle(code, description, prix)
                
                self.com.set('OK')
                self.boss.master.after(attenteCourte, self.clearCom)
                
        
                # basculer l'affichage dans la table
                # self.boss.cadreGestion.corps.display("afficher la salle")
            
    def commandListBox(self, **KW):    
        
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
             
   
       