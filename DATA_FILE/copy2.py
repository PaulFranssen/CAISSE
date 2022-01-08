import sqlite3

 

      
connexion = sqlite3.connect("data6Tcopy.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
connexion.execute("PRAGMA foreign_keys = 1")



curseur = connexion.cursor()

curseur.execute("""CREATE TABLE IF NOT EXISTS article (
                                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                code TEXT,
                                descript TEXT, 
                                prix INTEGER)""")



# récupérer les articles dans la base initiale

res = curseur.execute("SELECT * FROM workers")
res = curseur.execute("""SELECT code, des, pv FROM article WHERE envente=?""",(1,)).fetchall()

connexion.close()

if res:
    # insertion dans la base de destination
    connexion2 = sqlite3.connect("bdd.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    connexion2.execute("PRAGMA foreign_keys = 1")
    curseur2 = connexion2.cursor()
    
    # self.curseur2.execute("""CREATE TABLE IF NOT EXISTS articles (
    #                             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    #                             code TEXT,
    #                             descript TEXT, 
    #                             prix INTEGER)""")
        
    for tup in res:
        curseur2.execute("""INSERT INTO articles (code, descript, prix) VALUES(?,?,?)""", tup)
        connexion2.commit()


connexion2.close()

    