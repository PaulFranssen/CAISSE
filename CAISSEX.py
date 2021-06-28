
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# importation des modules
# import CTRL  # les vues sont contrôlées par la base se trouvant dans control
import VIEW

if __name__ == '__main__':
     
    # création du cadre principal et du lien : cadre > database et clic
    pf = VIEW.PF()
    

    # affichage  du cadre de gestion (En tête, corps, comment)
    pf.display("cadreGestion")
    
    # établissement de la caisse ouverte si il y en a
    pf.clic.setCaisse(newCaisse=False)

    # boucle principale (attente des événements)
    pf.mainloop()
    
   
    
     
     
    
    
    