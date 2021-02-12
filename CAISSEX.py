
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# importation des modules
# import CTRL  # les vues sont contrôlées par la base se trouvant dans control
import VIEW

if __name__ == '__main__':
   
    
    # création du cadre principal et du lien : cadre > database
    pf = VIEW.PF()
    

    # affichage  
    pf.display("cadreGestion")


    # boucle principale (attente des événements)
    pf.mainloop()
    
    
    
    
    
    