import sqlite3

 
class Database:
     
    def __init__(self):
        self.connexion = None
        self.curseur = None
        self.connexion2 = None
        self.curseur2 = None
              
    def ouvrir(self):
        try:
            self.connexion = sqlite3.connect("data6T.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            self.connexion.execute("PRAGMA foreign_keys = 1")
            self.curseur = self.connexion.cursor()
            
           

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            
        except OSError as error:
            print('autre erreur dans ouvrir', error)
            
    def copier(self):
        # récupérer les articles dans la base initiale
        res1 = self.curseur.execute("""SELECT name FROM categorie""").fetchall()
        res = self.curseur.execute("""SELECT code, des, pv FROM article WHERE envente=?""",(1,)).fetchall()
        self.connexion.close()
        if res:
            # insertion dans la base de destination
            self.connexion2 = sqlite3.connect("bdd.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            self.connexion2.execute("PRAGMA foreign_keys = 1")
            self.curseur2 = self.connexion2.cursor()
            
            for tup in res:
                self.curseur2.connexion2("""INSERT INTO articles (code, descript, prix) VALUES(?,?,?)""",tup)
            self.connexion2.commit()
    
    def fermer(self):
        
        self.connexion2.close()
        
if __name__ == "__main__":
    
    db = Database()
    db.ouvrir()
    db.copier()
    db.fermer()
    