from tkinter import *
from random import randrange
from CONST import *

class Bac(Canvas):
    def __init__(self, boss, width, height, bd=0, cursor=CURSOR):
        Canvas.__init__(self, boss, width = width, height = height, bd=bd, cursor=cursor, highlightthickness=0)
        
        # attributs
        self.boss = boss  # boss est contenu
        self.clic = boss.root.clic
        self.db = None
        self.width = None
        self.height = None
        self.table_pixels = None
        self.milieu = None
        self.font_tableName = (POLICE_TABLE, int(HAUTEUR_TEXTE_SALLE*COEF_DILATATION))
        self.font_facture = (POLICE_SALLE, int(HEIGHT_FACTURE*COEF_DILATATION))
        self.tup_selected = None  # tuple d'id sélectionnés
        self.number = 0  # numéro de la facture actuelle (0 donc pas de facture)
        self.id_lastFacture = None
        self.autorisation = True
        
        # liens avec événements
        self.bind('<Button-1>', self.selectByClic)
        self.bind('<Button1-Motion>', self.motion)
        self.bind('<Button1-ButtonRelease>', self.release)
        self.bind('<Control-Key-F>', self.create_facture)
        self.bind('<Control-Key-f>', self.create_facture)
        self.bind('<Button-2>', self.getFacture) # selection d'une facture par clic2
        
    def setDb(self, db):
        self.db = db
        
    def setNumber(self, number):
        """Détermine le Numéro de la dernière facture"""
        self.number = number
        
    def setColorFacture(self, nbr, statut):
        # récupérer le id correspondand à la facture nbr (str)
        tup = self.find_withtag("facture")
        for id in tup:
            if self.gettags(id)[2] == nbr:
                
                if statut == ROUGE:
                    self.delete(id)
                else:
                    self.itemconfigure(id, fill = statut)
                    # aussi à modifier tag[1]
                break
    
    def deleteFacture(self, nbr):
        tup = self.find_withtag("facture")
        for id in tup:
            if self.gettags(id)[2] == nbr:
                self.delete(id)
                break
    
    
    def setDimensions(self):
        # attributs
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self.table_pixels = int(self.height/DECOUPAGE_HEIGHT*COEF_DILATATION)
        self.milieu = (self.width/2, self.height/2)
        
    def displayTablesInit(self):
        for t in self.db.base5():
            args = list(t)[0:4] + [list(t)[4:]]
            self.create_table(*args)
            
    def getFacture(self, evt):
        "selectionne une facture par clic-2"
        # récupération de la position du clic et de l'id
        self.x1, self.y1 = evt.x, evt.y
        self.tup_selected = self.find_overlapping(self.x1, self.y1, self.x1, self.y1)
         
        if self.tup_selected:
            length = len(self.tup_selected)
            tag1 = self.gettags(self.tup_selected[0]) # tag du tuple sélectionné
            
            if length == 1:
                if tag1[0] == 'facture':
                    nbr = int(tag1[2])
                    self.clic.gofacture(self.db.base9(nbr), '')                    
            
            else: # la sélection contient une table et une facture en principe
                
                tag2 = self.gettags(self.tup_selected[1])
                if tag1[0] == 'facture':
                    nbr = int(tag1[2])
                    if tag2[0] == 'table':
                        self.clic.gofacture(self.db.base9(nbr), tag2[2])
                    else:
                        self.clic.gofacture(self.db.base9(nbr), '') 
                        
                elif tag2[0] == 'facture':
                    nbr = int(tag2[2])
                    if tag1[0] == 'table':
                        self.clic.gofacture(self.db.base9(nbr), tag1[2])
                    else:
                        self.clic.gofacture(self.db.base9(nbr), '')
            
        
    def getNbrMaxTable(self, dim):
        """retourne  le nombre max d'unités de tables en largeur ou en hauteur
        """
        dic = dict(width=int(self.width/self.table_pixels*COEF_REMPLISSAGE), 
                   height=int(self.height/self.table_pixels*COEF_REMPLISSAGE))
        
        return dic[dim]
    
    def create_facture(self, evt):
        ## vérifier si la caisse est ouverte
        if self.db.dat is not None:
           
        ## vérifier si la facture précédente a bougé
            if self.autorisation:
                
                self.id_lastFacture = self.create_text(self.milieu[0], self.milieu[1], 
                                                        fill=VERT, 
                                                        font = self.font_facture, 
                                                        text=str(self.number + 1), 
                                                        tags=("facture", VERT, str(self.number + 1)))   
                self.id_lastObject = self.id_lastFacture
                self.number +=1
                self.autorisation = False
                #self.tag_bind(id, '<Button-3>', lambda _ : self.gofacture(id)) #?
                
                # ajout de la facture à la base de données 
                box = self.coords(self.id_lastFacture)[0], self.coords(self.id_lastFacture)[1]
                self.db.base6(self.number, box)
                
   
    def create_table(self,largeur, hauteur, couleur, tableName, box=None):
        """crée une table et son nom en box ou au milieu

        Args:
            largeur (int): largeur de la table en unités
            hauteur (int): hauteur de la table en unités
            couleur (str): code couleur de la table
            tableName (str): nom de la table
        """
        nouvelle_table = True if box is None else False
        largeur_pixels = largeur*self.table_pixels
        hauteur_pixels = hauteur*self.table_pixels
        if box is None:
            x1 = int(self.milieu[0]-largeur_pixels/2)
            y1 = int(self.milieu[1]-hauteur_pixels/2)
            x2 = int(self.milieu[0]+largeur_pixels/2)
            y2 = int(self.milieu[1]+hauteur_pixels/2)
            box = x1, y1, x2, y2
        pos_texte = int((box[0] + box[2])/2), box[1] - HAUTEUR_TEXTE_SALLE * COEF_DILATATION
        
        id_tableName = self.create_text(*pos_texte, 
                                        font=self.font_tableName, 
                                        fill=couleur, 
                                        text=tableName, 
                                        tags=("tableName",))
        id_table = self.create_rectangle(*box, 
                                            fill=couleur, 
                                            width=0,
                                            tags=("table",))

        # créer le lien entre la table et son nom (la table comprendra aussi le nom de la table comme 3ème tag)
        self.addtag_withtag(str(id_tableName), id_table) # ajout de l'identifiant du nom comme tag de la table
        self.addtag_withtag(tableName, id_table)         # ajout du nom de la table comme tag de la table
        self.addtag_withtag(str(id_table), id_tableName) # ajout de l'identifiant de la table comme tag du nom de la table
        self.addtag_withtag(tableName, id_tableName)
                            
        self.lower(id_table)
        self.lower(id_tableName)
        
        # enregistrement de la table dans la db
        if nouvelle_table:
            self.db.base2(largeur, hauteur, couleur, tableName, *box)
 
    def deleteTable(self, tableName):
        # suppression de la table
        tup = self.find_withtag(tableName)
        for id in tup: # ne devrait contenir que 2 id
            self.delete(id)
           
    def selectByClic(self, evt):
        # récupération de la position du clic et de l'id le plus proche
        self.x1, self.y1 = evt.x, evt.y
        self.tup_selected = self.find_closest(self.x1, self.y1)
         
        if self.tup_selected:
            # tag du tuple sélectionné
            tag = self.gettags(self.tup_selected[0])
            #self.itemconfig(self.tup_selected[0], width = 20)
        
            if tag[0] == 'facture':
                self.lift(self.tup_selected)
                
            elif tag[0] == 'table' or tag[0] == 'tableName':
                if tag[0] == 'table':
                    id_table = self.tup_selected[0]
                    id_tableName = self.find_withtag(tag[1])[0]
                else:
                    id_tableName = self.tup_selected[0]
                    id_table = self.find_withtag(tag[1])[0]
                    
                self.tup_selected = (id_table, id_tableName)
                
                # détermination des factures dans la zone de la table
                box = self.bbox(id_table)
                if CAPTURE_DANS_TABLE == "find_overlapping":
                    insideBox_id = self.find_overlapping(*box)
                else:
                    insideBox_id = self.find_enclosed(*box)
                factures_id = self.find_withtag('facture')     
                for id in insideBox_id:
                    if id in factures_id:
                        self.tup_selected += (id,)
            else:
                self.tup_selected = None
                
    def getTableName(self, x1, y1):
        """détermine le nom de la table à la position x1,y1          

        Args:
            x1 (float): position x
            y1 (float): position y
        """
        insideBox_id = self.find_overlapping(x1, y1, x1,y1)
        tables_id = self.find_withtag("table")
        
        # récupérer un élément commun de ces deux ensembles
        tablename = ''
        if insideBox_id and tables_id:
            tables_id = set(insideBox_id) & set(tables_id)
            if tables_id:
                # récupérer le nom de la table
                tablename = self.gettags(tables_id.pop())[2]

        return tablename        
        
            
    def inFenetre(self, id, box):
        """détermine si id est dans une boite

        Args:
            id (int): id d'un objet
            box (tuple): boite englobante

        Returns:
            bool: True si id se trouve enfermé dans la box, False sinon
        """
        return id in self.find_enclosed(*box)
            
    def motion(self, evt):   
        if self.tup_selected:
            # position de la souris
            x2, y2 = evt.x, evt.y
            
            # valeur du déplacement potentiel
            dx, dy = x2-self.x1, y2-self.y1
            
            # deplacement sous condition : chaque objet dans la fenètre
            i = 0
            inside = True
            while i < len(self.tup_selected) and inside:
                inside = self.inFenetre(self.tup_selected[i], (0-dx , 0-dy, self.width-dx, self.height-dy))
                i +=1          
            if inside:    
                # chaque objet lié se déplace 
                for id in self.tup_selected:
                    self.move((id,), dx, dy)
                    
                # enregistrement de la nouvelle position 
                self.x1, self.y1 = x2, y2 
                
                # vérification du movement de la dernière facture
                if self.id_lastFacture in self.tup_selected:
                    self.autorisation = True 
                

    def release(self, evt):
        self.x1, self.y1 = evt.x, evt.y
        if self.tup_selected:
           
            # enregistrement des déplacements des objets sélectionnés
            for id in self.tup_selected:
                if self.gettags(id)[0] == 'table':
                    box = self.coords(id)
                    self.db.base3(self.gettags(id)[2], box)
                elif self.gettags(id)[0] == 'facture':
                    box = self.coords(id)[0], self.coords(id)[1]
                    self.db.base8(int(self.gettags(id)[2]), box)
                    
            # if self.gettags(self.tup_selected[0])[0] == 'facture':
            #     print(f'la facture {self.gettags(self.tup_selected[0])[2]} a été déplacée à la position ({self.x1}, {self.y1})')
            self.tup_selected = None
            