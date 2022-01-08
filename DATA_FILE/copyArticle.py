import sqlite3

 
class Database:
     
              
    def __init__(self):
      
        self.connexion = sqlite3.connect("data6T.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.connexion.execute("PRAGMA foreign_keys = 1")
    

        self.curseur = self.connexion.cursor()
       

        print(self.curseur)

    def copier(self):
        # récupérer les articles dans la base initiale
        res = self.curseur.execute("""SELECT code, des, pv FROM article WHERE envente=?""",(1,)).fetchall()
        
        self.connexion.close()
        
        if res:
            # insertion dans la base de destination
            self.connexion2 = sqlite3.connect("bdd.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            self.connexion2.execute("PRAGMA foreign_keys = 1")
            self.curseur2 = self.connexion2.cursor()
            
            # self.curseur2.execute("""CREATE TABLE IF NOT EXISTS articles (
            #                             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            #                             code TEXT,
            #                             descript TEXT, 
            #                             prix INTEGER)""")
                
            for tup in res:
                self.curseur2.execute("""INSERT INTO articles (code, descript, prix) VALUES(?,?,?)""", tup)
                self.connexion2.commit()
    
    def fermer(self):
        
        self.connexion2.close()
        
if __name__ == "__main__":
    
    db = Database()
   
    db.copier()
    db.fermer()
    