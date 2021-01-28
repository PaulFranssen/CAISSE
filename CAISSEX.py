
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# importation des modules
import CTRL  # les vues sont contrôlées par la base se trouvant dans control
import VIEW
if __name__ == '__main__':
   
    # création de la DATABASE
    base = CTRL.Base()

    # création du cadre principal et du lien : cadre > database
    pf = VIEW.PF(base)

    # fixation du lien : base > cadre_principal
    # base.fix_cp(pf)

    # affichage écran d'accueil 
    pf.display("cadreGestion")

    # création éventuelle du système de fichiers, établissement de la base de départ et de l'exercice actuel
    # base.create_f()

    # boucle principale (attente des événements)
    
    pf.mainloop()
    
    
    