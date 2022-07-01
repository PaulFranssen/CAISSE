
#!/usr/bin/env python
# -*- coding: utf-8 -*-


import CONST

# contrôle du login
with open(CONST.LOG_FILE, "r", encoding=CONST.ENCODEINFO) as file:
    log1 = file.readline() #sans histo login=0
    log2 = file.readline() #avec histo login=1
    log3 = file.readline() #sans histo ni synthese ni de ticket login=2
while True:
    login=input("LOGIN ")
    log1, log2, log3 = log1.strip(), log2.strip(), log3.strip()
    if login in {log1, log2, log3}:
        break

# contrôle de l'affichage
import tkinter    
import sys
fenetre = tkinter.Tk()
w, h = fenetre.winfo_screenwidth(), fenetre.winfo_screenheight()

# test à réaliser pour la conformité de l'affichage
if (w, h) != (1920, 1080):
    print(f"paramètres d'affichage {w}x{h} non pris en compte (1920x1080 requis)")
    fenetre.iconify()
    sortie=input()
    sys.exit()

login = [log2, log1, log3].index(login)
#import CTRL  # les vues sont contrôlées par la base se trouvant dans control
import VIEW

if __name__ == '__main__':
       
    # création du cadre principal et du lien : cadre > database et clic
    pf = VIEW.PF(login=login)
    
    # affichage  du cadre de gestion (En tête, corps, comment)
    pf.display("cadreGestion")
    
    # établissement de la caisse ouverte si il y en a
    pf.clic.setCaisse()

    # boucle principale (attente des événements)
    pf.mainloop()
    
            
