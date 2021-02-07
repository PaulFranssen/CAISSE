from tkinter import *
from random import randrange
from CONST import *


# LARGEUR_FENETRE = 500
# HAUTEUR_FENETRE = 400

class Bac(Canvas):
    def __init__(self, boss, width, bd=0, cursor=CURSOR):
        Canvas.__init__(self, boss, width = width, bd=bd, cursor=cursor, highlightthickness=0)
        # self.cadre = self.create_rectangle(0,0, width, height)
        self.bind('<Button-1>', self.selectByClic)
        self.bind('<Button1-Motion>', self.motion)
        self.bind('<Button1-ButtonRelease>', self.release)
        self.tup_selected = None
        print('configuration de la salle')
        
    def create_facture(self, number, x, y):
        id = self.create_text(x, y, fill='green', font=('helvetica', 14, 'bold'), text=str(number), tags=("facture", "green", str(number)))
        
        print('facture', id)
        self.tag_bind(id, '<Button-3>', lambda _ : self.gofacture(id))
         
    def create_table(self,x1, y1, x2, y2, coul, tableName):
        
        id_tableName = self.create_text((x1+x2)/2, y1 - HAUTEUR_TEXTE_SALLE, font=('helvetica', 12, 'italic'), fill='black', text=tableName, tags=("tableName",))
        id_table = self.create_rectangle(x1, y1, x2, y2, fill=coul, width=0,tags=("table",))
        
        print('tableName', id_tableName, 'table', id_table)
        
        # créer le lien entre la table et son nom
        self.addtag_withtag(str(id_tableName), id_table)
        self.addtag_withtag(str(id_table), id_tableName)
                              
        self.lower(id_table)
        self.lower(id_tableName)
        
    def gofacture(self, id):  
        print('accéder à la facture', self.gettags(id))
        #self.delete(id)
        
    def selectByClic(self, evt):
        #self.tup_selected = None
        self.x1, self.y1 = evt.x, evt.y
        self.tup_selected = self.find_closest(self.x1, self.y1)
            
        tag = self.gettags(self.tup_selected[0])
        print('objet sélectionné', self.tup_selected, "tags", tag)
        #self.itemconfig(self.tup_selected, width = 20)
        if tag[0] == 'facture':
            #print(f'une facture a été clickée une fois')
            self.lift(self.tup_selected)
             
        elif tag[0] == 'table'or tag[0] == 'tableName':
            if tag[0] == 'table':
                id_table = self.tup_selected[0]
                id_tableName = self.find_withtag(tag[1])[0]
            else:
                id_tableName = self.tup_selected[0]
                id_table = self.find_withtag(tag[1])[0]
                
            self.tup_selected = (id_table, id_tableName)
            
            # détermination des factures dans la zone de la table
            box = self.bbox(id_table)
            print('box', box)
            insideBox_id = self.find_enclosed(*box)
            print('inside_box', insideBox_id)
            factures_id = self.find_withtag('facture')     
            print('factures id', factures_id)
            for id in insideBox_id:
                if id in factures_id:
                    self.tup_selected += (id,)
        else:
            self.tup_selected = None
            
    def inFenetre(self, id, box):
        
        # print('in fenetre', id, self.find_enclosed(*box))
        return id in self.find_enclosed(*box)
            
    def motion(self, evt):   
        if self.tup_selected:
            # position de la souris
            x2, y2 = evt.x, evt.y
            
            # valeur du déplacement potentiel
            dx, dy = x2-self.x1, y2-self.y1
            
            # deplacement sous condition : chaque objet dans le cadre
            i = 0
            inside = True
            while i < len(self.tup_selected) and inside:
                inside = self.inFenetre(self.tup_selected[i], (0-dx , 0-dy, LARGEUR_FENETRE-dx,HAUTEUR_FENETRE-dy))
                i +=1          
            if inside:    
                # chaque objet lié se déplace 
                for id in self.tup_selected:
                    self.move((id,), dx, dy)
                    
                # enregistrement de la nouvelle position 
                self.x1, self.y1 = x2, y2 



    def release(self, evt):
        self.x1, self.y1 = evt.x, evt.y
        if self.tup_selected:
            if self.gettags(self.tup_selected[0])[0] == 'facture':
                print(f'la facture {self.gettags(self.tup_selected[0])[2]} a été déplacée à la position ({self.x1}, {self.y1})')
            self.tup_selected = None
            
if __name__ == '__main__':
    
    couleurs = ('grey80', 'wheat1', 'wheat2', 'wheat3')
    fen = Tk()
    bac = Bac(fen, width=LARGEUR_FENETRE, height=HAUTEUR_FENETRE, bg='ivory')
    bac.pack(padx=5, pady=3)
    b_fin = Button(fen, text='terminer', bg='royal blue', fg='white', font=("Helvetica", 10,'bold'), command=fen.quit)
    b_fin.pack(pady=2)
    
    wgt = [None for _ in range(5)]
    nbr = [None for _ in range(5)]
    for i in range(1):
        
        coul = couleurs[randrange(len(couleurs))]
        x1, y1 = randrange(30), randrange(20)
        x2, y2 = x1 + randrange(20,50), y1 + randrange(30, 50)
        bac.create_table(x1, y1, x2, y2, coul, "salon blanc" if i==0 else "table2")
        bac.create_facture(20, 30, str(49+randrange(50)))

    fen.mainloop()