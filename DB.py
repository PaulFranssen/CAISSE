 
import sqlite3, datetime
from CONST import *
 
class Database:
     
    def __init__(self):
        self.connexion = None
        self.curseur = None
        self.dat = None  # date de la caisse en cours
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
                                    tablename TEXT)""")
            
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
                                   
                            
            self.connexion.commit()
            
            # ouverture automatique d'une caisse existante
            #
            #
    # def base1(self):
    #     """retourne l'id de la caisse ouverte (None si pas de caisse ouverte)
    #     """
    #     return self.curseur.execute("""SELECT id WHERE statut=1""").fetchone()
    
    

    def base1(self, newCaisse):

        """établit la nouvelle caisse si pas de caisse avec un statut = 1
        
            newCaisse (bool) True si on crée une nouvelle caisse
        """
        res = self.curseur.execute("""SELECT dat FROM caisse WHERE statut=1""").fetchone()
        if res:
            print('caisse active', res)
            self.dat = res[0]
            print(self.dat)
            
        elif newCaisse:
            self.dat = datetime.datetime.now()
            self.curseur.execute("""INSERT INTO caisse(dat) VALUES(?)""", (self.dat,))
            print("ajout d'une caisse")
            self.connexion.commit()
            
        return self.dat
            
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
            res = self.curseur.execute("""SELECT nbr, serve, couleur, x1,y1, tablename FROM facture WHERE dat=?""",(self.dat,)).fetchall()
        return res
    
    def base7bis(self):
        """récupère la liste des factures vertes et oranges d'une caisse ouverte"
        """
        res = None
        if self.dat is not None:
            res = self.curseur.execute("""SELECT id, nbr, serve, couleur,x1,y1, tablename 
                                       FROM facture 
                                       WHERE dat=? 
                                       AND couleur<>?
                                       """,(self.dat,"rouge")).fetchall()
        return res
    
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
        res = self.curseur.execute("""SELECT id, nbr, serve, couleur, x1, y1, tablename 
                                       FROM facture 
                                       WHERE dat=? 
                                       AND nbr=?
                                       """,(self.dat, nbr)).fetchone()
        
        return res
    
    
    
    def base10(self, tablename):
        """récupère le service correspondant à tablename
        """
        if tablename:
            print('nomTAble', tablename)
            res = self.curseur.execute("""SELECT workers.nom FROM workers, serve, tables, caisse 
                                        WHERE workers.id = serve.work_id
                                        AND caisse.dat=? 
                                        AND caisse.id = serve.caisse_id
                                        AND tables.tableName=?
                                        AND tables.id = serve.tab_id
                                        """,(self.dat, tablename)).fetchone()
        else:
            res=None
        print(res)
        
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
        print(res, 'res', begin)
        if res:
            length = len(begin)
            liste = [nom[0] for nom in res if len(nom[0])>=length and begin==nom[0][:length]]
            liste.sort()
            print(liste)
        else:
            liste = []
        return liste
    
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
                
            
        
       
        
    def isWorker(self, nom):
        """détermine si un nom se trouve dans la base

        Args:
            nom (str): nom d'un employé
        """
        res = self.curseur.execute("""SELECT nom FROM workers WHERE nom=?""",(nom,)).fetchone()
        print(res)
        return True if res else False
    
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
        res = self.curseur.execute("""SELECT code FROM articles WHERE code=?""",(code,)).fetchone()
        return True if res else False
    
    def insertArticle(self, code, descript, prix):
        """insère un article
        """ 
        self.curseur.execute("""INSERT INTO articles (code, descript, prix) 
                             VALUES(?,?,?)""", (code, descript, prix))
        self.connexion.commit()
            
            
        
        
        
 
 # def fermer(self):
    #     pass

    # def fix_cp(self, cp):
    #     self.cp = cp
    # # self.fix_exercice(date.today().year)

    # def fix_theme(self, theme):
    #     self.theme = theme
    #     # self.cp.fix_exercice(theme)

    # def fix_database(self, database):

    #     # fixer le nom de la database et le path
    #     self.database = database
    #     self.database_path = join('BASE', database + '.db')

    #     # afficher le nom à l'écran
    #     self.cp.fix_database(self.database)

    #     # création de la database ou ouverture simple
    #     self.ouvrir()

    #     # création éventuelle des tables
    #     self.create_cat()
    #     self.create_type()
    #     self.create_article()
    #     self.create_composition()
    #     self.create_tiers()
    #     self.create_workers()
    #     self.create_charge()
    #     self.create_factureA()
    #     self.create_recordA()
    #     self.create_vente()
    #     self.create_recordV()
    #     self.create_stocloture()
    #     self.create_correction()
    #     self.create_ponderation()
    #     self.create_fixecat()
    #     self.create_limitation()
    #     self.create_trace()

    #     # fermeture de la database
    #     self.fermer()

    #     # enregistrement dans le fichier f_base de la database de lancement
    #     with open(f_base, 'w', encoding='utf-8') as f:
    #         f.write(self.database)

    # def get_database(self):
    #     return self.database

    # def get_curseur(self):
    #     return self.curseur

    # def ouvrir(self):
    #     try:
    #         self.connexion = connect(self.database_path, detect_types=PARSE_DECLTYPES | PARSE_COLNAMES)
    #         self.connexion.execute("PRAGMA foreign_keys = 1")
    #         self.curseur = self.connexion.cursor()

    #     except Error as error:
    #         print("Error while connecting to sqlite", error)

    #     else:
    #         if self.connexion:
    #             # connexion à la base de données
    #             pass

    # def enregistrer(self):
    #     self.connexion.commit()

    # def fermer(self):
    #     self.connexion.close()

    # def create_f(self):

    #     # fixation de l'execice
    #     self.fix_exercice(date.today().year)

    #     # création des fichiers txt
    #     try:
    #         if not exists('BASE'):
    #             mkdir('BASE')
    #         elif not isdir('BASE'):
    #             mkdir('BASE')
    #         if not exists('MEM_file'):
    #             mkdir('MEM_file')
    #         elif not isdir('MEM_file'):
    #             mkdir('MEM_file')
    #         if not exists(f_partage):
    #             with open(f_partage, 'w', encoding='utf-8') as f:
    #                 f.write('')
    #         if not exists(f_sauvegarde):
    #             with open(f_sauvegarde, 'w', encoding='utf-8') as f:
    #                 f.write('')
    #         if not exists(f_dirImport):
    #             with open(f_dirImport, 'w', encoding='utf-8') as f:
    #                 f.write('')
    #         if not exists(f_dirImportVente):
    #             with open(f_dirImportVente, 'w', encoding='utf-8') as f:
    #                 f.write('')
    #         if not exists(f_nameImport):
    #             with open(f_nameImport, 'w', encoding='utf-8') as f:
    #                 f.write('')
    #         if not exists(f_ticket):
    #             with open(f_ticket, 'w', encoding='utf-8') as f:
    #                 f.write('')
    #         if not exists(f_base):
    #             with open(f_base, 'w', encoding='utf-8') as f:
    #                 f.write('baseX')
    #         with open(f_base, 'r', encoding='utf-8') as f:
    #             nom = f.readline()
    #         if not nom.strip():
    #             nom = "baseX"

    #     except OSError as error:
    #         print(error)
    #         # a revoir commentaire avant de débuter
    #         return False
    #     else:
    #         # database initiale
    #         self.fix_database(nom)

    # def create_article(self):
    #     chaine = """CREATE TABLE IF NOT EXISTS article (
    #                 art_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    #                 code TEXT,
    #                 des TEXT,
    #                 cat_id INTEGER,        
    #                 pv INTEGER,
    #                 stockmin INTEGER DEFAULT 0,
    #                 envente INTEGER DEFAULT 1,
    #                 ad INTEGER,
    #                 FOREIGN KEY(cat_id) REFERENCES categorie(cat_id))"""
    #     self.curseur.execute(chaine)
    #     self.enregistrer()