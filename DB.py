 
import sqlite3, datetime
from CONST import *
 
class Database:
     
    def __init__(self):
        self.connexion = None
        self.curseur = None
        self.dat = None  # date de la caisse en cours (none alors pas de caisse sélectionnée)
        self.ouvrir()
              
    def ouvrir(self):
        try:
            self.connexion = sqlite3.connect(join(DATA_FILE, DATABASE_FILE), detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            self.connexion.execute("PRAGMA foreign_keys = 1")
            self.curseur = self.connexion.cursor()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            
        except OSError as error:
            print('autre erreur dans ouvrir', error)
        
        else:
            
            self.curseur.execute("""CREATE TABLE IF NOT EXISTS caisse (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    dat TIMESTAMP,
                                    fermeture TIMESTAMP,
                                    statut INTEGER DEFAULT 1)""")
            
            self.curseur.execute("""CREATE TABLE IF NOT EXISTS workers (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    nom TEXT)""")
            
            self.curseur.execute("""CREATE TABLE IF NOT EXISTS tables (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    largeur FLOAT,
                                    hauteur FLOAT,
                                    couleur TEXT,
                                    tableName TEXT,
                                    x1 INTEGER,
                                    y1 INTEGER,
                                    x2 INTEGER,
                                    y2 INTEGER)""")
            
            self.curseur.execute("""CREATE TABLE IF NOT EXISTS facture (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    dat TIMESTAMP,
                                    nbr INTEGER, 
                                    serve TEXT,
                                    couleur TEXT,
                                    x1 INTEGER,
                                    y1 INTEGER,
                                    tablename TEXT,
                                    total INTEGER DEFAULT 0,
                                    recu INTEGER DEFAULT 0,
                                    solde INTEGER DEFAULT 0)""")
            
            self.curseur.execute("""CREATE TABLE IF NOT EXISTS articles (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    code TEXT,
                                    descript TEXT, 
                                    prix INTEGER)""")
            
            self.curseur.execute("""CREATE TABLE IF NOT EXISTS serve (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    caisse_id INT,
                                    tab_id INT,
                                    work_id INT,
                                    FOREIGN KEY(caisse_id) REFERENCES caisse(id),
                                    FOREIGN KEY(tab_id) REFERENCES tables(id),
                                    FOREIGN KEY(work_id) REFERENCES workers(id))""")
            
            self.curseur.execute("""CREATE TABLE IF NOT EXISTS recordF (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    fact_id INTEGER,
                                    code_id INTEGER, 
                                    pu INTEGER,
                                    qte INTEGER,
                                    remise INTEGER,
                                    prix INTEGER,
                                    transfert INTEGER DEFAULT 0)""")
            
            
            self.curseur.execute("""CREATE TABLE IF NOT EXISTS modification (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    fact_id INTEGER,
                                    total1 INTEGER, 
                                    total2 INTEGER,
                                    fin INTEGER DEFAULT 0)""")

            self.curseur.execute("""CREATE TABLE IF NOT EXISTS mem (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    ouvre TIMESTAMP,
                                    ferme TIMESTAMP,
                                    ttc INTEGER, 
                                    impaye TEXT,
                                    modif TEXT)""")
            
            self.connexion.commit()
            
    def getCaisse(self, mem):
        
        res = self.curseur.execute("""SELECT id, dat, fermeture FROM caisse where statut=? AND dat>?""", (0, datetime.datetime.now()-datetime.timedelta(days=mem))).fetchall()
        return [] if not res else list(res)
        
    
    def base0(self):
        """détermine la date de la caisse ouverte ou None"""
        res = self.curseur.execute("""SELECT dat FROM caisse WHERE statut=?""",(1,)).fetchone()
        return None if not res else res[0]

    def base1(self):

        """établit une nouvelle caisse 
        """ 
        self.dat = datetime.datetime.now()
        self.curseur.execute("""INSERT INTO caisse(dat, statut) VALUES(?,?)""", (self.dat, 1))
        self.connexion.commit()
            

        return self.dat
    
    def deleteCaisse(self):
        """supprime l'ancienne caisse
        """
        # effacement des records, modifications, serve, factures, caisse
        self.curseur.execute("""DELETE FROM recordF""")
        self.curseur.execute("""DELETE FROM modification""")
        self.curseur.execute("""DELETE FROM serve""")
        self.curseur.execute("""DELETE FROM facture""")
        self.curseur.execute("""DELETE FROM caisse WHERE statut=0""")
        self.connexion.commit()

        
        
        
            
    def base2(self, *tup):
        """insere une nouvelle table
        """
        self.curseur.execute("""INSERT INTO tables(largeur, hauteur, couleur, tableName, x1, y1, x2, y2) 
                             VALUES(?,?,?,?,?,?,?,?)""", tup)
        self.connexion.commit()
        
    def base3(self, tableName, box):
        """update de la bbox de la table tableName

        Args:
            tableName (int): id de la table dans le bac
            box (tup): bbox de la table
        """
        self.curseur.execute("""UPDATE tables SET x1=?, y1=?, x2=?, y2=? WHERE tableName=?""", (*box, tableName))
        self.connexion.commit()
        
        
    # def base4(self, newId, tableName):
    #     """update de table_id à partie du nom de la table

    #     Args:
    #         newId (int): ancien table_id
    #         tableName (str): nom de la table
    #     """
    #     self.curseur.execute("""UPDATE tables SET table_id=? WHERE tableName=?""", (newId, tableName))
    #     self.connexion.commit()
        
    def base5(self):
        """retourne les caractéristiques (lst) de toutes les tables de la salle
        """
        res = self.curseur.execute("""SELECT largeur, hauteur, couleur, tableName, x1, y1, x2, y2 FROM tables""").fetchall()
        
        return res
    
    def base6(self, nbr, box):
        """crée une nouvelle facture inhérente à une caisse
        """
        
        # valeurs initiales 
        dat = self.dat
        serve = ""
        tablename=""
        couleur = VERT
        self.curseur.execute("""INSERT INTO facture(dat, nbr, serve, couleur, x1, y1, tablename) 
                             VALUES(?,?,?,?,?,?,?)""", (dat, nbr, serve, couleur, *box, tablename))
        self.connexion.commit()
        
        
        
    def base7(self):
        """récupères la liste des factures d'une caisse ouverte
        """
        res = None
        if self.dat is not None:
            res = self.curseur.execute("""SELECT id, nbr, serve, couleur, x1,y1, tablename FROM facture WHERE dat=?""",(self.dat,)).fetchall()
        return res
    
    def base7bis(self):
        """récupère la liste des factures non rouge d'une caisse ouverte"
        """
        res = None
        if self.dat is not None:
            res = self.curseur.execute("""SELECT id, nbr, serve, couleur,x1,y1, tablename 
                                       FROM facture 
                                       WHERE dat=? 
                                       AND couleur<>?
                                       """,(self.dat,ROUGE)).fetchall()
        return res
    
    def base7ter(self, nbr):
        """récupère la facture EN COURS(VERT) ou MODIFIE(VERT2) d'une caisse ouverte de numéro NBR"
        """
        res = None
        if self.dat is not None:
            res = self.curseur.execute("""SELECT id, total 
                                       FROM facture 
                                       WHERE dat=? 
                                       AND nbr=?
                                       AND (couleur=? OR couleur=?)
                                       """,(self.dat, nbr, VERT, VERT2)).fetchone()
        return res
    
    def updateTotal(self, fact_id, total):
        self.curseur.execute("""UPDATE facture SET total=? WHERE id=?""", (total, fact_id))
        self.connexion.commit()
        
    def deleteFacture(self, fact_id):
        self.curseur.execute("""DELETE FROM facture WHERE id=?""",(fact_id,))
        self.connexion.commit()
        
    def base8(self, nbr, box):
        """update d'une facture suite à un déplacement
        """
        self.curseur.execute("""UPDATE facture SET x1=?, y1=? WHERE dat=? AND nbr=?""",(*box, self.dat, nbr))
        self.connexion.commit()
        
    def base9(self, nbr):
        """recupère éléments d'une facture sur base de son nombre et de sa date
    
        Args:
            nbr (int): nombre de la facture
        """

        
        # res = self.curseur.execute("""SELECT id, nbr, serve, couleur, x1, y1, tablename, recu, solde FROM facture WHERE dat=? AND nbr=?""",(self.dat, nbr)).fetchone()
        
        # ne tient pas compte de la date
        res = self.curseur.execute("""SELECT id, nbr, serve, couleur, x1, y1, tablename, recu, solde 
                                       FROM facture 
                                       WHERE nbr=?
                                       """,(nbr, )).fetchone()
        
        return res
    

    
    def base10(self, tablename):
        """récupère le service correspondant à tablename
        """
        if tablename:
         
            res = self.curseur.execute("""SELECT workers.nom FROM workers, serve, tables, caisse 
                                        WHERE workers.id = serve.work_id
                                        AND caisse.dat=? 
                                        AND caisse.id = serve.caisse_id
                                        AND tables.tableName=?
                                        AND tables.id = serve.tab_id
                                        """,(self.dat, tablename)).fetchone()
        else:
            res=None
        
        
        return '' if not res else res[0]
    
    def base11(self, begin):
        """recupère la liste des workers commençants par begin
        """
        res = self.curseur.execute("""SELECT nom FROM workers""").fetchall()
        
        if res:
            length = len(begin)
            liste = [nom[0] for nom in res if len(nom[0])>=length and begin==nom[0][:length]]
            liste.sort()
            
        else:
            liste = []
        return liste
    
    def base12(self, begin):
        """recupère la liste des code commençants par begin
        """
        res = self.curseur.execute("""SELECT code FROM articles""").fetchall()
        # print(res, 'res', begin)
        if res:
            length = len(begin)
            liste = [nom[0] for nom in res if len(nom[0])>=length and begin==nom[0][:length]]
            liste.sort()
            # print(liste)
        else:
            liste = []
        return liste
    def deleteTable(self, tableName):
        self.curseur.execute("""DELETE FROM tables WHERE tableName=?""",(tableName,))
        self.connexion.commit()
        
    def setRecu(self, fact_id, recu):
        self.curseur.execute("""UPDATE facture SET recu=? WHERE id=?""",(recu, fact_id))
        self.connexion.commit()
        
    def recordTable(self, fact_id, tablename):
        self.curseur.execute("""UPDATE facture SET tablename=? WHERE id=?""",(tablename, fact_id))
        self.connexion.commit()
        
    def recordService(self, fact_id, service):
        self.curseur.execute("""UPDATE facture SET serve=? WHERE id=?""",(service, fact_id))
        self.connexion.commit()
        
    def deleteServe(self):
        self.curseur.execute("""DELETE FROM serve""")
        self.connexion.commit()
        
        
    # def deleteSolde(self, fact_id):
    #     self.curseur.execute("""UPDATE facture SET solde=? WHERE id=?""",(0, fact_id))
    #     self.connexion.commit()
        
    def recordLigne(self, **kw):
        """enregistre une ligne de zone d'encodage dans la db (table recordF), ajuste le total
        """

        ## identifiant de la facture
        fact_id = self.base9(kw['nbr'])[0]
        total = self.curseur.execute("""SELECT total FROM facture WHERE id=?""",(fact_id,)).fetchone()[0]
        transfert = kw['transfert']
        if kw['index_selected'] is None: # cas de l'absence de ligne sélectionnée
     
            if not transfert:
                res = self.curseur.execute("""SELECT id, qte, remise, prix FROM recordF 
                                        WHERE fact_id=?
                                        AND code_id=? 
                                        AND pu=?
                                        AND transfert=?
                                        """, (fact_id, kw['code_id'], kw['pu'], 0)).fetchone()
                if res:
                    # cas du update
                    id = res[0]
                    qte = res[1] + kw['qte']          
                    remise = res[2] + kw['remise']
                    prix = res[3] + kw['prix']
                    
                    self.curseur.execute("""UPDATE recordF 
                                            SET qte=?, remise=?, prix=?
                                            WHERE id=?""", (qte, remise, prix, id))
                    
                    total += prix
                    self.curseur.execute("""UPDATE facture SET total=? WHERE id=?""",(total, fact_id))
                    self.connexion.commit()
                
                else:
                    # cas du insert
                    self.curseur.execute("""INSERT INTO recordF (fact_id, code_id, pu, qte, remise, prix) 
                                        VALUES(?,?,?,?,?,?)""", (fact_id, kw['code_id'], kw['pu'], kw['qte'], kw['remise'], kw['prix']))
                    total += kw['prix']
                    self.curseur.execute("""UPDATE facture SET total=? WHERE id=?""",(total, fact_id))
                    self.connexion.commit()
            else:
                # insertion (transfert)
                self.curseur.execute("""INSERT INTO recordF (fact_id, code_id, pu, qte, remise, prix, transfert) 
                                        VALUES(?,?,?,?,?,?,?)""", (fact_id, kw['code_id'], kw['pu'], kw['qte'], kw['remise'], kw['prix'], 1))
                total += kw['prix']
                self.curseur.execute("""UPDATE facture SET total=? WHERE id=?""",(total, fact_id))
                self.connexion.commit()
                
        else: # cas du remplacement de l'enregistrement
            id = self.getList_RecordF(fact_id)[kw['index_selected']][0] # récupération de id du record
            old_prix = self.getList_RecordF(fact_id)[kw['index_selected']][5]
            # update
            self.curseur.execute("""UPDATE recordF 
                                    SET code_id=?, pu=?, qte=?, remise=?, prix=?
                                    WHERE id=?""", (kw['code_id'], kw['pu'], kw['qte'], kw['remise'], kw['prix'], id))
            total += kw['prix'] - old_prix
            self.curseur.execute("""UPDATE facture SET total=? WHERE id=?""",(total, fact_id))
            self.connexion.commit()
            
    def getList_RecordF(self, fact_id):
        """get la liste des enregistrements correspondant à un id de facture
        """
        # récupérer le numéro de facture
        
        res = self.curseur.execute("""SELECT id, code_id, pu, qte, remise, prix, transfert FROM recordF 
                                    WHERE fact_id=?
                                    """, (fact_id,)).fetchall()
        return [] if not res else list(res)
    
    def insertRecordF(self, fact_id, code_id, pu, qte, remise, prix, transfert):
        self.curseur.execute("""INSERT INTO recordF (fact_id, code_id, pu, qte, remise, prix, transfert) 
                                VALUES(?,?,?,?,?,?,?)""", (fact_id, code_id, pu, qte, remise, prix, transfert))
        self.connexion.commit()
        
    def code_id(self, code):
        res = self.curseur.execute("""SELECT id FROM articles WHERE code=?""",(code,)).fetchone()
        return False if not res else res[0]   
    
    def getT(self, fact_id):
        res = self.curseur.execute("""SELECT total from facture WHERE id=?""", (fact_id,)).fetchone()
        return 0 if not res else res[0]
    
    def getTotal(self, fact_id):
        """calcule et renvoie le total d'une facture
        """
        # récupération des prix des recordF associés à cette facture
        res = self.curseur.execute("""SELECT prix from recordF WHERE fact_id=?""",(fact_id,)).fetchall()
        total = 0 if not res else sum([tup[0] for tup in res])
        
        # enregistrer le total dans le record
        self.curseur.execute("""UPDATE facture SET total=? WHERE id=?""",(total, fact_id))
        self.connexion.commit()
        return total
    
    def getArticle(self, code_id):
        res = self.curseur.execute("""SELECT code, descript FROM articles WHERE id=?""",(code_id,)).fetchone()
        return res 
    
    def getArticle2(self, code_id):
        res = self.curseur.execute("""SELECT code, descript, prix FROM articles WHERE id=?""",(code_id,)).fetchone()
        return res

    
    def updateArticle(self, code, descript, prix, code_id):
        self.curseur.execute("""UPDATE articles
                                    SET code=?, descript=?, prix=?
                                    WHERE id=?""", (code, descript, int(prix.replace('.','')), code_id))
        self.connexion.commit()
    
    def deleteServe2(self, work_id):
        self.curseur.execute("""DELETE FROM serve WHERE work_id=?""",(work_id,))
        self.connexion.commit()
        
    def deleteWorker(self, work_id):
        self.curseur.execute("""DELETE FROM workers WHERE id=?""",(work_id,))
        self.connexion.commit()
    
    def getStatut(self):
        res = self.curseur.execute("""SELECT statut FROM caisse WHERE dat=?""", (self.dat,)).fetchone()
        return None if not res else res[0]
    
    def getStatut2(self):
        res = self.curseur.execute("""SELECT statut FROM caisse""").fetchone()
        return None if not res else res[0]
    
    
    def getWorker_id(self, nom):
        res = self.curseur.execute("""SELECT id FROM workers WHERE nom=?""", (nom,)).fetchone()
        return None if not res else res[0]

    def getWorkerFromFacture(self, id):
        res = self.curseur.execute("""SELECT serve FROM facture WHERE id=?""", (id,)).fetchone()
        return None if not res else res[0]

    def clotureCaisse(self, fermeture):
        self.curseur.execute("""UPDATE caisse SET fermeture=?, statut=? WHERE dat=?""",(fermeture, 0, self.dat))
        self.connexion.commit()
        self.dat = None
        
    def getDat(self):
        return self.dat

    def getDatesCloture(self):
        res = self.curseur.execute("""SELECT dat, fermeture FROM caisse""").fetchone()
        if res:
           
            ouverture = JOUR_SEM[res[0].weekday()] + " "+res[0].strftime("%d/%m/%y %H:%M")
            fermeture = JOUR_SEM[res[1].weekday()] + " "+res[1].strftime("%d/%m/%y %H:%M")
            return (ouverture, fermeture)


    def setDat(self, dat):
        self.dat = dat
        
    def recordInServe(self, tablename, service):
        """enregistre un lien table-service
        """
        tab_id = self.curseur.execute("""SELECT id FROM tables WHERE tablename=?""",(tablename,)).fetchone()
        work_id = self.curseur.execute("""SELECT id FROM workers WHERE nom=?""",(service,)).fetchone()
        caisse_id = self.curseur.execute("""SELECT id FROM caisse WHERE dat=?""",(self.dat,)).fetchone()
        
        if tab_id and work_id and caisse_id: # cas du record possible
            
            id = self.curseur.execute("""SELECT id FROM serve 
                                       WHERE caisse_id=? 
                                       AND tab_id=?""",(caisse_id[0], tab_id[0])).fetchone()
            if id: # il y a déjà une table enregistrée > update le service
                self.curseur.execute("""UPDATE serve
                                        SET work_id=?
                                        WHERE id=?""", (work_id[0], id[0]))
                self.connexion.commit()
            else: # pas encore d'enregistrement pour cette table et cette caisse
                self.curseur.execute("""INSERT INTO serve (caisse_id, tab_id, work_id)
                             VALUES(?,?,?)""", (caisse_id[0], tab_id[0], work_id[0]))
                self.connexion.commit()
                
    def deleteRecordF(self, recordF_id):
        self.curseur.execute("""DELETE FROM recordF WHERE id=?""", (recordF_id,))
        self.connexion.commit()
            
    def isCaisseOpen(self):
        return self.curseur.execute("""SELECT id FROM caisse WHERE statut=1""").fetchone()
        
    def isWorker(self, nom):
        """détermine si un nom se trouve dans la base

        Args:
            nom (str): nom d'un employé
        """
        res = self.curseur.execute("""SELECT nom FROM workers WHERE nom=?""",(nom,)).fetchone()
        return True if res else False
    
    def isTable(self, nom):
        res = self.curseur.execute("""SELECT id FROM tables WHERE tableName=?""",(nom,)).fetchone()
        return False if not res else res[0]
    
    def deleteRecordServe(self, tab_id):
        self.curseur.execute("""DELETE FROM serve WHERE tab_id=?""",(tab_id,))
        self.connexion.commit()
    
    def recordStatut(self, fact_id, statut):
        self.curseur.execute("""UPDATE facture SET couleur=? WHERE id=?""", (statut, fact_id))
        self.connexion.commit()
        
    def recordSolde(self, fact_id, solde):
        self.curseur.execute("""UPDATE facture SET solde=? WHERE id=?""", (solde, fact_id))
        self.connexion.commit()
        
    def recordRecu(self, fact_id, recu):
        self.curseur.execute("""UPDATE facture SET recu=? WHERE id=?""", (recu, fact_id))
        self.connexion.commit()
        
    
             
    def recordModification(self, fact_id, step, total):
        """enregistre une modification à l'étape 0  ou à l'étape 1 (refacturation après modification)
        retourne le total avant modification si étape 1

        """
        res = 0
        if step == 0:
            # on enregistre une nouvelle modification et on la fin=0
            self.curseur.execute("""INSERT INTO modification (fact_id, total1) VALUES (?,?)""", (fact_id, total))  
            
        else: # step=1
            # récupérer l'ancien total qui apparaitra sur la facture
            res = self.curseur.execute("""SELECT total1 FROM modification WHERE fact_id=? AND fin=?""", (fact_id, 0)).fetchone()
            # enregistrement final
            self.curseur.execute("""UPDATE modification SET total2=?, fin=? WHERE fact_id=? AND fin=?""", (total, 1, fact_id, 0))

        self.connexion.commit() 
        return 0 if not res else res[0]

    
    def insertWorker(self, nom):
        """insère un worker

        Args:
            nom (str): nom d'un worker
        """ 
        self.curseur.execute("""INSERT INTO workers (nom) 
                             VALUES(?)""", (nom,))
        self.connexion.commit()
        
    def isCode(self, code):
        """détermine si le code se trouve dans la base
        """
        res = self.curseur.execute("""SELECT id FROM articles WHERE code=?""",(code,)).fetchone()
        return True if res else False
    
    def getCode_id(self,code):
        res = self.curseur.execute("""SELECT id FROM articles WHERE code=?""",(code,)).fetchone()
        if res:
            return res[0]
    def isRecorded(self, code_id):
        """détermine si un code apparait dans une facture
        """
        res = self.curseur.execute("""SELECT id FROM recordF WHERE code_id=?""",(code_id,)).fetchone()
        return False if not res else res
    
    def deleteArticle(self, code_id):
        self.curseur.execute("""DELETE FROM articles WHERE id=?""",(code_id,))
        self.connexion.commit()
     
    def isDescription(self, code, description):
        """Vérifie si le code correspond à la description
        """
        res = self.curseur.execute("""SELECT id FROM articles WHERE code=? AND descript=?""",(code, description)).fetchone()
        return True if res else False
    
    def getDescription(self, code):
        """Retourne la description à partir du code
        """
        res = self.curseur.execute("""SELECT descript FROM articles WHERE code=?""",(code,)).fetchone()
        return '' if not res else res[0]
    
    def getPU(self, code):
        """Retourne le pu partir du code
        """
        res = self.curseur.execute("""SELECT prix FROM articles WHERE code=?""",(code,)).fetchone()
        return '' if not res else str(res[0])
    
    def insertArticle(self, code, descript, prix):
        """insère un article
        """ 
        self.curseur.execute("""INSERT INTO articles (code, descript, prix) 
                             VALUES(?,?,?)""", (code, descript, prix))
        self.connexion.commit()
            
    def getOuverture(self):
        return self.dat
    
    def getOuverture2(self):
        return self.curseur.execute("""SELECT dat, fermeture FROM caisse""").fetchone()
    
    def getEnCours(self):
        res = self.curseur.execute("""SELECT total FROM facture WHERE dat=? AND (couleur=? OR couleur=?)""",(self.dat, VERT, VERT2)).fetchall()     
        return 0 if res is None else sum([tup[0] for tup in res])
    
    def getEnFacture(self):
        res = self.curseur.execute("""SELECT total FROM facture WHERE dat=? AND couleur=?""",(self.dat, ORANGE)).fetchall()     
        return 0 if res is None else sum([tup[0] for tup in res])
        
    def getEnCloture(self):
        res = self.curseur.execute("""SELECT total FROM facture WHERE dat=? AND couleur=?""",(self.dat, ROUGE)).fetchall()     
        return 0 if res is None else sum([tup[0] for tup in res])
    
    def getEnCloture2(self):
        res = self.curseur.execute("""SELECT total FROM facture WHERE couleur=?""",(ROUGE,)).fetchall()     
        return 0 if res is None else sum([tup[0] for tup in res])
    
    def getImpaye(self):
        res = self.curseur.execute("""SELECT solde FROM facture WHERE dat=? AND couleur=? AND solde>?""",(self.dat, ROUGE,0)).fetchall()     
        return (0, 0) if res is None else (sum([tup[0] for tup in res]), len(res))
    
    def getImpaye2(self):
        res = self.curseur.execute("""SELECT solde FROM facture WHERE couleur=? AND solde>?""",(ROUGE,0)).fetchall()     
        return (0, 0) if res is None else (sum([tup[0] for tup in res]), len(res))
      
    def getModification(self):
        res = self.curseur.execute("""SELECT total1, total2 FROM modification, facture WHERE facture.id=modification.fact_id AND facture.dat=? AND modification.fin=?""", (self.dat, 1)).fetchall()
      
        return (0, 0) if res is None else (sum([tup[1]-tup[0] for tup in res]), len(res))
    
    def getModification2(self):
        res = self.curseur.execute("""SELECT total1, total2 FROM modification, facture WHERE facture.id=modification.fact_id AND modification.fin=?""", (1,)).fetchall()
        
    
        return (0, 0) if res is None else (sum([tup[1] - tup[0] for tup in res]), len(res))
    
    def getFermeture(self):
        res = self.curseur.execute("""SELECT fermeture FROM caisse WHERE dat=? AND statut=?""",(self.dat,0)).fetchone()
        return res if res is None else res[0]

    def getOuvre(self):
        res = self.curseur.execute("""SELECT dat FROM caisse""").fetchone()
        return res if res is None else res[0]


    def getInfoTicket(self, fact_id):
        """informations sur la facture pour l'impression du ticket
        """
        infoTik = dict()
        # récupération dans la table facture
        res = self.curseur.execute("""SELECT nbr, serve, tableName, total, recu, solde FROM facture WHERE id=?""",(fact_id,)).fetchone()
        if res:
            infoTik['nbr'], infoTik['serve'], infoTik['tableName'], infoTik['total'], infoTik['recu'], infoTik['solde']  = res[0], res[1], res[2], res[3], res[4], res[5]
        else:
            print('erreur : pas de facture de cet id pour infoTicket!')

        # récupération dans recordF
        infoTik['recordF'] = []
        res = self.curseur.execute("""SELECT descript, pu, qte, remise, recordF.prix FROM articles, recordF WHERE code_id=articles.id AND fact_id=?""",(fact_id,)).fetchall()
        if res:
            for rec in res:
                infoTik['recordF'].append(dict(des=rec[0], pu=rec[1], qte=rec[2], remise=rec[3], prix=rec[4]))

        # récupération de la modification (à faire)
        
        return infoTik

    def getFinalTicket(self):
        """ renvoi une liste triée des ventes, la clé étant un tuple (code, pu) 
        """
        res = self.curseur.execute("""SELECT code, qte, recordF.prix FROM articles, recordF WHERE articles.id=recordF.code_id""").fetchall()
        dico = dict()
        if res:
            for code, qte, prix in res:
                pu=round(prix/qte)
                if (code, pu) not in dico:
                    dico[(code, pu)]= qte, prix
                else:
                    dico[(code, pu)] = dico[(code, pu)][0] + qte, dico[(code, pu)][1] + prix
        return sorted(dico.items(), key=lambda t:t[0])

    def getBackUp(self):
        """renvoi des éléments des caisses précédentes sous forme d'une liste triée selon le id en décroissant
        """
        dico = dict()
        res = self.curseur.execute("""SELECT id, ouvre, ferme, ttc, impaye, modif FROM mem""").fetchall()
        if res:
            for id, ouvre, ferme, ttc, impaye, modif in res:
                dico[-id] = (ouvre, ferme, ttc, impaye, modif)
        return [t[1] for t in sorted(dico.items())]

    def getArticles(self):
        """renvoi des éléments des articles sous forme d'une liste triée selon le id en décroissant
        """
        dico = dict()
        res = self.curseur.execute("""SELECT code, descript, prix FROM articles""").fetchall()
        if res:
            for code, descript, price in res:
                dico[code] = (code, descript, price)
        return [t[1] for t in sorted(dico.items())]

    def recordBackUp(self, impaye, modif, ttc, fermeture):
        """Enregistre la caisse qui se cloture et limite le backUp aux x derniers jours
        """
        res = self.curseur.execute("""SELECT dat FROM caisse WHERE statut=?""", (1,)).fetchone()
        if res:
            self.curseur.execute("""INSERT INTO mem(ouvre, ferme, ttc, impaye, modif) VALUES (?,?,?,?,?)""", (res[0], fermeture, ttc, impaye, modif)) 
            self.connexion.commit()
            # suppression des caisses trop vieilles
            self.curseur.execute("""DELETE FROM mem WHERE ferme<?""",(datetime.datetime.now()-datetime.timedelta(days=MEMORY),))
            self.connexion.commit()



 