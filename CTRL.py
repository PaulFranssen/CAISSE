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
        self.clicTerminer = 0 # indique le nombre de clic effectué sur la touche terminer
        
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
        
        if ch and ch[0] == "-":
            # cas négatif
            print(ch)
            if len(ch) > 7:
                    ch = ch[:-6] + '.' + ch[-6:-3] + '.' + ch[-3:]
            elif len(ch) > 4:
                ch = ch[:-3] + '.' + ch[-3:]    
        else:
            if len(ch) > 6:
                ch = ch[:-6] + '.' + ch[-6:-3] + '.' + ch[-3:]
            elif len(ch) > 3:
                ch = ch[:-3] + '.' + ch[-3:]
        return ch
    
    
    def setCaisse(self):  
        """établit la caisse et affiche les éventuelles factures dans la salle

        """
        # déterminer si une caisse est ouverte
        dat = self.db.base0()
        
        if dat :
            self.db.setDat(dat)
            # récupérer les factures d'une caisse ouverte
            factures = self.db.base7()
        
            # affiche les factures dans la salle s'il y en a
            if factures :
                # affiche les factures non rouges existantes
                self.displayFactures(factures)
                
    def commandValider(self, **kw):
        # récupérer les variables
        if kw['b']['state'] == DISABLED:
            return
        # annulle les box 2 et 3 (service et article)
        #self.fac.deleteLB23()
        
        service = kw['service'].get().strip()
        code = kw['code'].get().strip()
        description = kw['description'].get()
        pu=kw['pu'].get().strip()
        qte=kw['qte'].get().strip()
        remise=kw['remise'].get().strip()
        prix=kw['prix'].get().strip()
        #statut = kw['statut'].get()
        nbr = kw['nbr'].get().strip()
        recu = kw['recu'].get().strip()
        
        try:
            # # vérification du statut
            # if statut not in {DIC_STATUT[VERT], DIC_STATUT[VERT2]}:
            #     raise E(self.com, 'STATUT ' + statut , 'modification non autorisée')
            
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
                self.boss.master.after(attenteLongue, self.clearCom)
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
            recu = 0 if recu == '' else int(recu.replace('.',''))          
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
            self.boss.master.after(attenteCourte, self.clearCom)
            self.fac.focusEntryCode()
    
    def commandFacturer(self, **kw):
       
        if kw['b']['state'] == DISABLED:
            return
        
        service = kw['service'].get().strip()
        recu = kw['recu'].get().strip()
        nbr = kw['nbr'].get().strip()
        statut = self.fac.getStatut()

        # self.fac.deleteLB23()
        kw['listBox2_var'].set([]) # effacer la listbox2 (proposition d'aricles)
        
        try:
            test = "nbr"
            nbr1 = int(nbr)
            if self.fac.getN() != nbr1: # le numéro de facture a été changé sans GO
                    #vérifier encore le  getNbr() vide (à faire) cas particulier de départ
                    raise E(self.com, 'N°FACTURE', 'ne correspond pas à la facture')

            if statut == ORANGE:
                pass
               
            elif statut == VERT or statut == VERT2:
                test = ""      
                # vérifier si la facture contient des éléments
                if not len(kw['listBox_var'].get()):
                    raise E(self.com, "FACTURER", "facture vide")
                
                # vérifier si la zone d'encodage est vide
                if not self.fac.isEncodageVide():
                    raise E(self.com, "ZONE D'ENCODAGE", "non-vide")
                
                test ="service"
                # vérification du service
                if not self.db.isWorker(service):
                    raise E(self.com, 'SERVICE', 'inexistant')
                
                test = "reçu"
                if not self.isNumber(recu):
                    raise E(self.com, 'RECU', 'non-conforme')
                
        except E as e:
            e.affiche()
            self.boss.master.after(attenteLongue, self.clearCom)
        
        except:
            if test == "nbr":
                E(self.com, "N°FACTURE", "non-conforme").affiche()
                self.boss.master.after(attenteLongue, self.clearCom)
        
            else:
                E(self.com, "", "?").affiche()
                self.boss.master.after(attenteLongue, self.clearCom)
        
        else: 
            
            if statut == ORANGE:
                self.imprimerFacture(fact_id = self.fac.getId())
            
            elif statut == VERT or statut == VERT2:
               
                ## association entre une table et le service
                ### récupérer la table
                tablename = kw['table'].get().strip()
                ### enregistrer le lien table-service (update ou insert) dans la db serve
                self.db.recordInServe(tablename, service)
                
                # récupérer le id facture
                fact_id = self.fac.getId()
                
                # enregistrement du service et de la tableName dans la facture
                self.db.recordService(fact_id, service)
                self.db.recordTable(fact_id, tablename)
                
                # mise en forme du reçu et enregistrement dans la base
                recu = 0 if recu == '' else int(recu.replace('.',''))          
                self.db.setRecu(fact_id, recu)
                kw['recu'].set(self.formatNumber(recu))
                
                
                # modification 
                if statut == VERT2:
                    modification=True # modification activée pour l'impression
                    total1 = self.db.recordModification(fact_id = fact_id, step=1, total = self.db.getTotal(fact_id))
                else:
                    modification = False
                    total1 = False
                    
                # établissement du nouveau statut
                self.fac.setStatut(ORANGE)
                self.bac.setColorFacture(nbr, ORANGE) 
                
                
                # impression facture
                self.imprimerFacture(fact_id = fact_id, modification=modification, total1=total1)
            
    def imprimerFacture(self, fact_id, modification=False, total1=0, finale=False):
        """lance l'impression d'une facture

        Args:
            fact_id (int): id de la facture
            modification (bool): _True si il s'agit d'imprimer une facture qui a été modifiée_. Defaults to False.
            total1 (int, optional): _valeur du total avant modification_. Defaults to 0.
            finale(bool): _True si le client a payé et que c'est sa facture finale_.Defaults to 0.
        """


        def contenu():
            """imprime le contenu d'une facture"""
          
            fichier.write('{:^31}'.format(ETOILE))
            fichier.write('\n{:^31}'.format(NOM_BAR))
            fichier.write('\n{:^31}'.format(ETOILE))
            fichier.write('\n'+'{:^31}'.format(NUM_TEL))          
            fichier.write('\n\n'+'{:^31}'.format('TICKET DE CAISSE'))
            fichier.write('\n'+BARRE)
            fichier.write('\n\n')
            fichier.write(f"{dico['tableName']:<13}{'FACTURE N°'+str(fact_id):>18}")
            fichier.write('\n'+TIRET)

            for ligne in dico['recordF']:
                fichier.write('\n'+ligne['des'][:31])            
                pu=fpx(ligne['pu'])
                qte=fpx(ligne['qte'])
                ttc=fpx(ligne['prix'])

                if ligne['remise']=="0" or not ligne['remise']:
                    "pas de remise"
                    lig='  {:>16}{:>13}'.format(qte+"x"+pu,ttc)
                    fichier.write('\n'+lig)
                else :
                    remise='-'+fpx(ligne['remise'])
                    lig='  {:>16}'.format(qte+"x"+pu)
                    fichier.write('\n'+lig)
                    lig='  {:>16}{:>13}'.format(remise,ttc)
                    fichier.write('\n'+lig)
                
            fichier.write('\n'+TIRET)
            fichier.write('\n'+'  {:>16}{:>13}'.format('TOTAL TTC ',fpx(dico['total'])))

            if finale: # afficher le montant reçu et le solde
                fichier.write('\n'+'  {:>16}{:>13}'.format('RECU ',fpx(dico['recu']))) 
                texte = "RESTE A PAYER " if dico['solde']>0 else "SOLDE "
                fichier.write('\n'+'  {:>16}{:>13}'.format(texte,fpx(dico['solde'])))
                 
            fichier.write('\n'+TIRET)    
            fichier.write('\n{:^31}'.format('A votre service : '+self.db.getWorkerFromFacture(fact_id).capitalize()[:13]))

            dat=str(datetime.datetime.today())
            fichier.write('\n'+'{:^31}'.format(dat[8:10]+'/'+dat[5:7]+'/'+dat[0:4]+'   '+dat[11:16]))
            
            if finale:
                fichier.write(f"\n{POLITESSE:^31}")
        
        print("IMPRESSION FACTURE, modification :", fact_id, modification)
        dico =self.db.getInfoTicket(fact_id)

        if modification==False:

            fichier = open(TICKET_FILE+".txt", "w")
            if finale and dico['solde']>0:
                fichier.write(f"{'FACTURE N°' + str(fact_id) +' CRÉDITÉE':^31}")
                fichier.write('\n')
                fichier.write(f"{'MONTANT CRÉDITÉ : '+ fpx(dico['solde']):^31}")
                fichier.write('\n\n')

            contenu()  
            fichier.close()
            startfile(TICKET_FILE+".txt", IMPR)
            if finale and dico['solde']>0 : 
                 startfile(TICKET_FILE+".txt", IMPR)

            
        else: # imprimer 2 tickets modifiés : 1 pour le client et 1 pour la caisse
            
            fichier = open(TICKET_FILE+".txt", "w")
            fichier.write(f"{'FACTURE N°' + str(fact_id) +' MODIFIÉE':^31}")
            fichier.write('\n')
            fichier.write(f"{'ANCIEN TOTAL : '+ fpx(total1):^31}")
            fichier.write('\n\n')
            #récupérer les infos de la modification
            contenu()

            fichier.close()

            startfile(TICKET_FILE+".txt", IMPR)
            startfile(TICKET_FILE+".txt", IMPR)
          

            
           
       

        # à poursuivre ici ligne 1728 dans excaisse

        
     





        
    def commandModifier(self, **kw):
        
        if kw['b']['state'] == DISABLED:
            return
        
        # annulle les box 2 et 3 (service et article)
        #self.fac.deleteLB23()
        
        # effacer l'éventuel solde
        self.fac.deleteSolde()
        
        # récupérer id de la facture
        fact_id = self.fac.getId()
        
        # enregistrer la modification (step=0 en début de modification et step=1 en fin de modification)
        self.db.recordModification(fact_id =fact_id, step=0, total = self.db.getTotal(fact_id))
        
        # ouvrir la facture et la faire passer en modification
        self.fac.setStatut(VERT2)
        self.bac.setColorFacture(str(self.fac.getN()), VERT2)
        
        
    def commandTerminer(self, **kw): 
        
        if kw['b']['state'] == DISABLED:
            return   
        
        # annulle les box 2 et 3 (service et article)
        #self.fac.deleteLB23()
        
        # terminer n'est activé que quand je suis en statut orange
        fact_id = self.fac.getId()
        recu = kw['recu'].get().strip()
        nbr = kw['nbr'].get().strip()
        total = kw['total'].get().strip()
        
        try:
            test = "nbr"
            # vérification du N° de facture
            nbr1 = int(nbr)
            if self.fac.getN() != nbr1: # le numéro de facture a été changé sans GO
                #vérifier encore le  getNbr() vide (à faire) cas particulier de départ
                raise E(self.com, 'N°FACTURE', 'ne correspond pas à la facture')
           
            if self.fac.getStatut() != ROUGE:    
                test = "reçu"
                if not self.isNumber(recu) or recu == '':
                    raise E(self.com, 'RECU', 'non-conforme')
                
        except E as e:
            e.affiche()
            self.boss.master.after(attenteLongue, self.clearCom)
        
        except:
            if test == "nbr":
                E(self.com, "N°FACTURE", "non-conforme").affiche()
                self.boss.master.after(attenteLongue, self.clearCom)
        
            else:
                E(self.com, "", "?").affiche()
                self.boss.master.after(attenteLongue, self.clearCom)
        
        else: # validation effectuée correctement
            
            if self.fac.getStatut() == ROUGE: # cas de l'impression ticket direct
                self.imprimerFacture(fact_id, finale=True)
                
            else: # orange et passage au rouge si second clic
                
                # récupération du reçu et du total
                recu = int(recu.replace('.',''))
                self.db.recordRecu(fact_id, recu) # enregistrement du recu
                total = int(total.replace('.', ''))
                
                # calcul du solde
                solde = total - recu
                
                # affichage du solde (avec recup de l'ancien)
                sld = kw['solde'].get().strip().replace('.','')
                solde_old = 0 if not sld else int(sld)
                kw['solde'].set(self.formatNumber(solde))
                
                # affichage du reçu 
                kw['recu'].set(self.formatNumber(recu))
                self.fac.focus_set()
                
                # adaptation du background du solde
                if solde > 0:
                    # modifier le background du entry
                        kw['entrySolde'].configure(disabledbackground = self.th.getColorWarning(choix = "disabledbackground"))
                else: 
                    kw['entrySolde'].configure(disabledbackground = self.th.getColorOK(choix = "disabledbackground"))
                
                
                if self.clicTerminer == 1: 
                    self.clicTerminer = 0 # réinitialisation du clicTerminer
                    
                    # impression facture si le solde n'a pas changé      
                    if solde == solde_old: # le solde est resté identique après le premier clic
                        self.db.recordSolde(fact_id, solde) # fixer le solde dans la facture définitive
                        # self.db.recordTable(fact_id, kw['table'].get().strip())
                        # self.db.recordService(fact_id, kw['service'].get().strip())
                        
                        self.fac.setStatut(ROUGE) # passage au rouge 
                        self.bac.setColorFacture(nbr, ROUGE) # passage de la facture nbr au rouge dans le bac
                        # suppression des associations table-serveur
                        kw['entrySolde'].configure(disabledbackground = self.th.getColorNormal(choix = "disabledbackground"))
                        self.imprimerFacture(fact_id, finale=True) # imprimée 2x si le solde est positif
                else:
                    self.clicTerminer = 1 # second passage à venir
    
    def commandRecu(self, **kw):
        recu = kw['recu'].get().strip()
        if self.isNumber(recu):
            kw['recu'].set(self.formatNumber(recu))
            self.fac.focus_set()
                    
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
            
            # supprimer les éventuels mots dans la box
            kw['listBox3_var'].set([])
            # focus sur entryCode
            kw['entryCode'].focus_set()
            kw['entryCode'].icursor(END)
            
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
        
        # focus sur le code
        kw['entryCode'].focus_set()
        kw['entryCode'].icursor(END)
            
            
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
            
        # mise en forme du pu et de la remise
        
        res = True
        
        boolPu, boolQte, boolRemise = self.isNumber(pu), self.isNumber(qte),self.isNumber(remise)
        if not pu or not qte:
            res=False
        elif not boolPu or not boolQte or not boolRemise: 
            res=False
        elif len(qte)>LENGTH_QTE:
            res=False
        
        if res:
            # calcul d'un prix
            prix = int(qte.replace('.','')) * int(pu.replace('.','')) - int(remise.replace('.',''))
            if prix >=0 and prix <= 99999999:
                # fixer le prix
                kw['prix'].set(self.formatNumber(str(prix)))
                # focus sur le buttonValider
                self.fac.focusValider()
                #kw['entryPrix'].focus_set()
            else:
                res=False
                         
        if not res:
            # prix annulé
            kw['prix'].set('')
            
            # focus sur le probleme
            if not boolPu or pu == '':
                kw['entryPU'].focus_set()
                kw['entryPU'].icursor(END)
            elif not boolQte or qte == '':
                kw['entryQTE'].focus_set()
                kw['entryQTE'].icursor(END)
            elif not boolRemise:
                kw['entryRemise'].focus_set()
                kw['entryRemise'].icursor(END)
            else:
                kw['entryPrix'].focus_set()
                
        # mise en forme du pu et de la remise
        if boolPu:
            kw['pu'].set(self.formatNumber(pu))
        if boolRemise:
            kw['remise'].set(self.formatNumber(remise))  
                 
    def displayFactures(self, factures):
        # afficher toutes les factures se trouvant dans la database   
        nbr_max = 0 # nombre max de factures
        for fact_id, nbr, serve, couleur,x1, y1, tablename in factures:
            # sauf les rouges
            if couleur != ROUGE:
                self.bac.id_lastFacture = self.bac.create_text(x1, y1,
                                                        fill=couleur, 
                                                        font = self.bac.font_facture, 
                                                        text=str(nbr), 
                                                        tags=("facture", couleur, str(nbr)))   
                self.bac.id_lastObject = self.bac.id_lastFacture
            nbr_max = max(nbr, nbr_max)
            
        self.bac.setNumber(nbr_max)
            
            
            # liens des factures avec le button-2 > gofacture
            # self.bac.tag_bind(self.bac.id_lastFacture, '<Button-2>', lambda _ : self.gofacture((fact_id, nbr, serve, couleur)))
        
    def gofacture(self, tup, tablename):
        """affiche la facturation avec les éléments de la facture

        Args:
            tup (tuple): (fact_id, nbr, serve, couleur, tablename, recu, solde))
        """
        self.clicTerminer = 0  # initialisation du clicTerminer
        
        # établissement des 2 premières lignes de la facture, du reçu et du solde
        self.fac.setId(tup, tablename)
        
        # actualisation de la listBox
        
        fact_id = tup[0] # récupère le id de facture
        
        self.actualiserListBox(fact_id)
        
        self.boss.cadreGestion.corps.display("facturation")
        
    def actualiserListBox(self, fact_id):
        """actualise la listBox pour une facture fact_id après validation, effacement ou lors de l'affichage de la facture, yc solde et reçu
        """
         # annulle les box 2 et 3 (service et article)
        self.fac.deleteLB23()
        
        # supprime le transfert
        self.fac.deleteTransfert()
        
        if self.index_selected is not None:  # supprime l'éventuelle ligne sélectionnée dans la box
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
        
        # focus
        if not self.fac.getEntryService():
            self.fac.focusEntryService()
        else:
            self.fac.focusEntryCode()
        
        
            
        
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
            tablename = ''
            # récupérer la table si la facture n'est pas rouge
            if couleur == VERT or couleur == VERT2:  
                tablename = self.bac.getTableName(x1, y1)
                #self.fac.setId(facture, tablename) 
            self.gofacture(facture, tablename)
    
    """
    def imprimerFactureFinale(self, fact_id):
        print('FACTURE FINALE', fact_id)
        # à imprimer 2x si le solde correspondant à cette facture est positif
    """         
    def displayContenu(self, **KW):
        
        # if KW['item'] == "sélectionner":
        #     # récupérer les valeurs dans les caisses
        #     liste_caisse = self.db.getCaisse(MEMORY)
        #     if liste_caisse:
        #         liste_var = [str(elem[1])[:19] for elem in liste_caisse] 
        #     else:
        #         liste_var = []
            
        #     # fixer la liste dans le spinBox
        #     KW['spinBox'].configure(values = liste_var)
            
        if KW['item'] == "synthèse":
            
            self.clearCom()
            
            h = self.db.getOuverture2()
            
            if h: # il existe une caisse
                ouverture, fermeture = h
                ouverture = str(ouverture)[:19]
                fermeture = "-" if not fermeture else str(fermeture)[:19] 
                KW['entry2_var'].set(ouverture)
                
                a = self.db.getEnCours()
                KW['entryA_var'].set(self.formatNumber(a))
                b = self.db.getEnFacture()
                KW['entryB_var'].set(self.formatNumber(b))
               
                c = self.db.getEnCloture2()
                KW['entryC_var'].set(self.formatNumber(c))
                KW['entryD_var'].set(self.formatNumber(a+b+c))
                
                d = self.db.getImpaye2()
                d = "-" if d==(0,0) else f"{self.formatNumber(d[0])} #{d[1]}"
                KW['entry3_var'].set(d)
                
                e = self.db.getModification2()
                e = "-" if e==(0,0) else f"{self.formatNumber(e[0])} #{e[1]}"
                KW['entry4_var'].set(e)
                # g = self.db.getFermeture()
                # g = "-" if not g else str(g)[:19]
                KW['entry5_var'].set(fermeture)
                
            else: # pas de caisse
                KW['entry2_var'].set("-")
                KW['entryA_var'].set("-")
                KW['entryB_var'].set("-")
                KW['entryC_var'].set("-")
                KW['entryD_var'].set("-")
                KW['entry3_var'].set("-")
                KW['entry4_var'].set("-")
                KW['entry5_var'].set("-")
            
        elif KW['item'] == "ajouter une table":
            self.clearCom()
            KW['entry2_var'].set('')
            KW['entry2'].focus_set()
        
        elif KW['item'] == "afficher la salle":
            
            KW['bac'].focus_set()
            
        elif KW['item'] == "facturation":
            
            if not self.db.isCaisseOpen(): # pas de caisse active
                # afficher un message 
                self.fac.pack_forget()
                KW['facVide'].pack()
                self.com.set("Pas de caisse ouverte")
                self.boss.master.after(attenteLongue, self.clearCom)
            else:
                self.fac.pack(side=LEFT)
            
            
            
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
            
        # elif KW['item'] == "éditer les employés":
        #     KW['entry2_var'].set('')
        #     KW['entry2']['state']=DISABLED
        #     employe_lst = [' Jacques', ' Norbert', ' Andrea']
        #     KW['listBox_lst'].clear()
        #     KW['listBox_lst'].extend(employe_lst)
        #     KW['listBox'].configure(height=min(len(employe_lst), HEIGHT_LISTBOX), width=LENGTH_CODE+2)
        #     KW['listBox_var'].set(employe_lst)
        #     KW['listBox'].selection_set(0)
        #     KW['listBox'].focus_set()
            
        elif KW['item'] == "modifier un article":
            self.clearCom()
            KW['entry2_var'].set('')
            KW['entryA_var'].set('')
            KW['entryB_var'].set('')
            KW['entryC_var'].set('')
            
            KW['entry2'].configure(state=NORMAL)
            KW['entryA'].configure(state=DISABLED)
            KW['entryB'].configure(state=DISABLED)
            KW['entryC'].configure(state=DISABLED)
            
            KW['entry2'].focus_set()
            
          
        elif KW['item'] == "ajouter un article":
            self.clearCom()
            KW['entry2_var'].set('')
            KW['entry3_var'].set('')
            KW['entry4_var'].set('')
            KW['entry2'].focus_set()  
    
    def displayButton(self, **kw):
        
        if kw['item'] == "cloture & ticket":
            self.clearCom()
           
            statut = self.db.getStatut2()
            
            if statut is None:
                # désactiver le bouton1
                kw['bouton1'].configure(state = DISABLED, text = "CLOTURER")
                self.com.set("Pas de caisse enregistrée")
                self.boss.master.after(attenteLongue, self.clearCom)
                
            elif statut == 0:
                # la caisse est cloturée
                kw['bouton1'].configure(state = NORMAL, text = "TICKET")
                
            elif not self.db.base7bis():
                # la caisse est active et toutes les factures sont cloturées
                kw['bouton1'].configure(state = NORMAL, text = "CLOTURER")
            
            else:
                # la caisse est active et toutes les factures sont cloturées
                kw['bouton1'].configure(state = DISABLED, text = "CLOTURER")
                self.com.set("Il reste des factures non cloturées")
                self.boss.master.after(attenteLongue, self.clearCom)
           
        
        elif kw['item'] == "nouvelle caisse":
            self.clearCom()
            
            if self.db.getDat() is None:
                    # désactiver le bouton1
                kw['bouton1'].configure(state = NORMAL)
                  
            else:
                kw['bouton1'].configure(state = DISABLED)
                self.com.set('Caisse en cours')
                self.boss.master.after(attenteLongue, self.clearCom)
                
        # elif kw['item'] == "sélectionner":
            
        #     if self.db.getDat() is None:
        #         kw['bouton1'].configure(state = NORMAL)        
        #     else: 
        #         kw['bouton1'].configure(state = DISABLED)
        #         self.com.set('Inaccessible car une caisse est ouverte')
        #         self.boss.master.after(attenteLongue*2, self.clearCom)
            

                   
    def commandBouton(self, **kw):
        numeroBouton = kw['numeroBouton']
        contenu = kw['contenu']
        bouton1 = kw['bouton1']
        
        # if contenu.item == "sélectionner":
        #     if kw['bouton1']['state'] == DISABLED:
        #         return
            
        # considérer la sélection et fixer la date
        # date = contenu.spinBox_var.get()
              
        
        if contenu.item == "supprimer une table":
            try:
                # vérifier si la table existe
                tableName = contenu.entry2_var.get().strip()
                table_id = self.db.isTable(tableName)
                if not table_id:
                    raise E(self.com, "NOM", "inexistant")   
                    
            except E as e:
                e.affiche() 
                self.boss.master.after(attenteLongue, self.clearCom)
            
            else:    
                # supprimer son enregistrement du serve db
                self.db.deleteRecordServe(table_id)
                # supprimer dans le bac (avec son assicié tablename)
                self.bac.deleteTable(tableName)
                # supprimer dans la database
                self.db.deleteTable(tableName)
                self.com.set('OK')
                self.boss.master.after(attenteCourte, self.clearCom)
                # effacer le entry
                contenu.entry2_var.set('')
                contenu.focus_set()
            
        if contenu.item == "supprimer un article":
            # vérifier si l'article existe
            try:
                code = contenu.entry2_var.get().strip()
                code_id = self.db.getCode_id(code)
                if not code_id:
                    raise E(self.com, "CODE", "inexistant")         
                # vérifier qu'il n'apparaisse pas dans un record de facture
                if self.db.isRecorded(code_id):
                    raise E(self.com, "CODE", "présent dans une facture")  
                
            except E as e:
                e.affiche() 
                self.boss.master.after(attenteLongue, self.clearCom)
            
            else:   
                # supprimer dans la db
                self.db.deleteArticle(code_id)
                
                self.com.set('OK')
                self.boss.master.after(attenteCourte, self.clearCom)
                # effacer le entry
                contenu.entry2_var.set('')
                contenu.focus_set()
                
        if contenu.item == "supprimer un employé":
            # vérifier si l'employé existe
            try:
                code = contenu.entry2_var.get().strip()
                work_id = self.db.getWorker_id(code)
                if not work_id:
                    raise E(self.com, "NOM", "inexistant")         
                 
                
            except E as e:
                e.affiche() 
                self.boss.master.after(attenteLongue, self.clearCom)
            
            else:   
                # supprimer dans serve
                self.db.deleteServe2(work_id)
                
                # supprimer dans la db
                self.db.deleteWorker(work_id)
                
                self.com.set('OK')
                self.boss.master.after(attenteCourte, self.clearCom)
                # effacer le entry
                contenu.entry2_var.set('')
                contenu.focus_set()
                
        if contenu.item == "modifier un article":
            
            code, description, prix = contenu.entryA_var.get().strip(), contenu.entryB_var.get().strip(), contenu.entryC_var.get().strip()
            codeM = contenu.entry2_var.get().strip()
            test = ''
            try:
                 # le code de l'article doit être unique (utiliser la base de données)               
                if self.db.isCode(code) and code != codeM:
                    raise E(self.com, 'CODE', 'déjà utilisé')  
                if not code :
                    raise E(self.com, 'CODE', 'saisie vide')
                if len(code) > LENGTH_CODE:
                    raise E(self.com, 'CODE', f"trop long (max {LENGTH_CODE} caractères)")
                
                if not description :
                    raise E(self.com, 'DESCRIPTION', 'saisie vide')
                if len(description) > LENGTH_DESCRIPTION:
                    raise E(self.com, 'DESCRIPTION', f"trop long (max {LENGTH_DESCRIPTION} caractères)")
                
                if not prix :
                        raise E(self.com, 'PRIX', 'saisie vide')
                if len(prix) > LENGTH_PRIX:
                    raise E(self.com, 'PRIX', f"trop long (max {LENGTH_PRIX} caractères)")
                
                if not self.isNumber(prix) or prix == '':
                    raise E(self.com, 'PRIX', f"prix non-conforme")
                
            except E as e:
                e.affiche()
                self.boss.master.after(attenteLongue, self.clearCom)
                
            except:
                E(self.com, "", '?').affiche()
                self.boss.master.after(attenteLongue, self.clearCom)
            else:    
                
                # modifier l'article
                code_id = self.db.getCode_id(codeM)
               
                self.db.updateArticle(code, description, prix.replace('.',''), code_id)
                
                self.com.set('OK')
                self.boss.master.after(attenteCourte, self.clearCom)
                contenu.entryA_var.set('')
                contenu.entryB_var.set('')
                contenu.entryC_var.set('')
                contenu.entry2_var.set('')
                contenu.entryA.configure(state=DISABLED)
                contenu.entryB.configure(state=DISABLED)
                contenu.entryC.configure(state=DISABLED)
                contenu.entry2.configure(state=NORMAL)
                
                contenu.entry2.focus_set()
                
        if contenu.item == "nouvelle caisse":
            # désactiver la touche dans le menu
            #self.boss.cadreGestion.entete.desactive_item('nouvelle caisse')
            # ajouter un id dans la base de données, avec le statut 1 (ouvert)
            # self.db.base1(newCaisse = True)
            
            # récupérer la dat de la caisse en cours ou none
            if bouton1["state"] == DISABLED:
                 return  
            
            else:
                self.db.base1() # ouverture de caisse

                self.bac.setNumber(0)  # mise à 0 du numéro de factures
                
                # factures = self.db.base7()
                # # affiche les factures dans la salle s'il y en a
                # if factures:
                #     # affiche les factures existantes
                #     self.displayFactures(factures)
                
                # suppression des données de l'ancienne caisse
                self.db.deleteCaisse()
                

                self.com.set('OK')
                bouton1.configure(state=DISABLED)
                self.boss.master.after(attenteCourte, self.clearCom) 
                 
                # afficher la salle
                # self.boss.cadreGestion.corps.display("afficher la salle")
                return
        
        if contenu.item == "cloture & ticket":
           
            if bouton1['state'] == DISABLED:
                return
            
            elif bouton1['text'] == "TICKET":
                print('IMPRIMER TICKET FINAL')
                self.com.set('OK')
                self.boss.master.after(attenteCourte, self.clearCom) 
                      
            else:
                # cloture effective de la caisse
                
                self.db.clotureCaisse()
                print('cloture effectuée')
                #self.db.deleteServe()  # suppression de l'association service-table
                bouton1.configure(text="TICKET")
                self.com.set('OK')
                self.boss.master.after(attenteCourte, self.clearCom)
                
        if contenu.item == "ajouter un employé":
            nom = contenu.entry2_var.get().strip()
            
            test =''
            try:
                # le nom de l'employé doit être unique
                if self.db.isWorker(nom):
                    raise E(self.com, 'NOM', 'déjà utilisé')  
                
                if not nom :
                    raise E(self.com, 'NOM', 'pas de nom')
                
                if len(nom) > LENGTH_WORKER:
                    raise E(self.com, 'NOM', f"trop long (max {LENGTH_WORKER} caractères)")
            
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
            nom, largeur, hauteur, couleur = contenu.entry2_var.get().strip(), contenu.entryA_var.get().strip(), contenu.entryB_var.get().strip(), contenu.spinBox_var.get()
            table_names = self.bac.find_withtag(nom)
            
            test =''
            try:
                 # le nom de la table doit être unique (utiliser la base de données ou le canvas)               
                if table_names:
                    raise E(self.com, 'NOM', 'déjà utilisé')  
                if not nom :
                    raise E(self.com, 'NOM', 'pas de nom saisi')
                if len(nom) > LENGTH_TABLE:
                    raise E(self.com, 'NOM', f"trop long (max {LENGTH_TABLE} caractères)")
                if nom.isnumeric():
                    raise E(self.com, 'NOM', f"format numérique non accepté")
                
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
                self.clearCom()
                
                # ajouter une table au milieu du canvas
                tup = self.bac.create_table(largeur=float(largeur),
                                                hauteur=float(hauteur), 
                                                couleur=couleur, 
                                                tableName=nom)
                
                # basculer l'affichage dans la table
                self.boss.cadreGestion.corps.display("afficher la salle")
                
        if contenu.item == "ajouter un article":
            code, description, prix = contenu.entryA_var.get().strip(), contenu.entryB_var.get().strip(), contenu.entryC_var.get().strip()
            
            test = ''
            try:
                 # le code de l'article doit être unique (utiliser la base de données)               
                if self.db.isCode(code):
                    raise E(self.com, 'CODE', 'déjà utilisé')  
                if not code :
                    raise E(self.com, 'CODE', 'saisie vide')
                if len(code) > LENGTH_CODE:
                    raise E(self.com, 'CODE', f"trop long (max {LENGTH_CODE} caractères)")
                
                if not description :
                    raise E(self.com, 'DESCRIPTION', 'saisie vide')
                if len(description) > LENGTH_DESCRIPTION:
                    raise E(self.com, 'DESCRIPTION', f"trop long (max {LENGTH_DESCRIPTION} caractères)")
                
                if not prix :
                        raise E(self.com, 'PRIX', 'saisie vide')
                if len(prix) > LENGTH_PRIX:
                    raise E(self.com, 'PRIX', f"trop long (max {LENGTH_PRIX} caractères)")
                
                if not self.isNumber(prix) or prix == '':
                    raise E(self.com, 'PRIX', f"prix non-conforme")
                
            except E as e:
                e.affiche()
                self.boss.master.after(attenteLongue, self.clearCom)
                
            except:
                E(self.com, test, 'non-conforme').affiche()
                self.boss.master.after(attenteLongue, self.clearCom)
            else:    
                
                # ajouter l'aricle
                self.db.insertArticle(code, description, prix.replace('.',''))
                
                self.com.set('OK')
                self.boss.master.after(attenteCourte, self.clearCom)
                contenu.entryA_var.set('')
                contenu.entryB_var.set('')
                contenu.entryC_var.set('')
                contenu.focus_set()
                
            
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
            
    def commandEntry2(self, **kw):
        if kw['item'] == "modifier un article":
            # vérifier qu'il y a un code valide dans entry2_var
            try:
                code = kw['entry2_var'].get().strip()
                code_id = self.db.getCode_id(code)
                if not code_id:
                    raise E(self.com, "CODE", 'inexistant')
                
            except E as e:
                e.affiche()
                self.boss.master.after(attenteCourte, self.clearCom)
                
            else:
                kw['entry2'].configure(state=DISABLED)
                kw['entryA'].configure(state=NORMAL)            
                kw['entryB'].configure(state=NORMAL)   
                kw['entryC'].configure(state=NORMAL) 
                
                cod, des, prx = self.db.getArticle2(code_id)
                
                kw['entryA_var'].set(cod)            
                kw['entryB_var'].set(des)  
                kw['entryC_var'].set(self.formatNumber(prx))
                 
                kw['entryA'].focus_set()
                kw['entryA'].icursor(END)
                 
    def commandSpinBox(self, **kw):
        
        if kw['item'] == "ajouter une table":
            # récupérer la sélection et modifier la couleur de bg
            colorKey = kw['spinBox_var'].get().strip()
            color = self.th.getColorT(colorKey)
            kw['spinBox'].configure(readonlybackground=color)
               
    # def returnListBox(self, **KW):
        
    #     if KW['item'] == "éditer les employés":
    #         index = int(KW['listBox'].curselection()[0])
    #         employe = KW['listBox'].get(index).strip()
    #         KW['entry2']['state'] = NORMAL
    #         KW['entry2_var'].set(employe)
    #         KW['entry2'].focus_set()
    
    def goTransfert(self, **kw):
        
        if kw['bouton5']['state'] == DISABLED:
            return
        
        destination = kw['destination'].get().strip()
        nbr = kw['nbr'].get().strip()
        listBox_var = kw['listBox_var']
        
        test =''
        # test de la validité du transfert demandé de nbr > destination
        try:
            test = 'nbr'
            nbr1 = int(nbr)
            
            factN = self.fac.getN()
            fact_id = self.fac.getId()
            
            if factN != nbr1:
                raise E(self.com, "N°FACTURE", "ne correspond pas à la facture")
            # facture verte2 (modifié) ne peut pas être transféré (état DISABLED)
            # la destination doit correspondre à entier
            test = 'transfert'
            nbr2 = int(destination)
            
            # la destination doit être différente de nbr
            if nbr2 == factN:
                 raise E(self.com, 'TRANSFERT', 'non-conforme')
                 
            # la destination doit être une facture au statut VERT ou VERT2 self.dat
            facture_destination = self.db.base7ter(nbr2)
           
            if not facture_destination:
                 raise E(self.com, 'TRANSFERT', 'non-conforme')
                
            # la listBox doit être non-vide
            if not listBox_var.get():
                 raise E(self.com, "FACTURE", "rien à transférer")
               
            # la zone d'encodage doit être vide
            if not self.fac.isEncodageVide():
                raise E(self.com, "ZONE D'ENCODAGE", "non-vide")
  
        except E as e:
            e.affiche()
            self.boss.master.after(attenteLongue, self.clearCom)
            
        except:
            if test == 'nbr':
                E(self.com, 'N°FACTURE', 'non-conforme').affiche()
            
            elif test == 'transfert':
                E(self.com, 'TRANSFERT', 'numéro non-conforme').affiche()
            
            else:
                E(self.com, '', '?').affiche()
            
            self.boss.master.after(attenteLongue, self.clearCom)
            
        else:
            # effacer la entry de transfert
            kw['destination'].set('')
            
            id_destination, total_destination = facture_destination
            
            # ajouter les éléments de la box à l'autre facture (recalculer son total)
            total_origine = self.db.getT(fact_id) # total de la facture de départ
            for recordF_id, code_id, pu, qte, remise, prix, transfert in self.db.getList_RecordF(fact_id):
                self.db.insertRecordF(id_destination, code_id, pu, qte, remise, prix, transfert = 1) # ajoute un record F dans la facture de destination
                self.db.deleteRecordF(recordF_id) # supprime l'enregistrement dans la facture d'origine
            
            self.bac.deleteFacture(nbr) # efface la facture origine dans la salle
            self.db.deleteFacture(fact_id) # supprimer la facture d'origine dans la base
            self.db.updateTotal(id_destination, total_origine + total_destination) # update le total de destination
            
            facture = self.db.base9(nbr2) # facture de destination
            fact_id, nbr, serve, couleur, x1, y1, tablename, recu, solde = facture
            if couleur != "ROUGE":  # cas d'une facture rouge (ici ne devrait pas arriver)
                tablename = self.bac.getTableName(x1, y1)
            self.gofacture(facture, tablename)
            self.fac.focusEntryCode()
            # self.com.set('Transfert effectué')
            # self.boss.master.after(attenteLongue, self.clearCom())
   
       