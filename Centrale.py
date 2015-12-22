# ----- Centrale -----










actionOk = False;


while(actionOk == False):

    print("Que voulez-vous faire ?");

    action = input("1- Nouvelle inscription : comptetw –p <pseudo> \n2- Vous connecter : tweet -p <pseudo> \n");

    print (action);
    if ("comptetw -p" in action) :
        actionOk = True;
        
        #On supprime l'action
        pseudo = action.replace("comptetw -p", "");
    
        #On supprime d'éventuels espaces
        pseudo = pseudo.replace(" ", "");

        input("On crée un nouveau compte avec comme pseudo :"+pseudo+"\n");

    elif ("tweet -p" in action) :
        actionOk = True;
        
        #On supprime l'action
        pseudo = action.replace("tweet -p", "");
        
        #On supprime d'éventuels espaces
        pseudo = pseudo.replace(" ", "");
        
        input("Vous êtes connecté en tant que : "+pseudo+"\n");
        rechercheMail(mail, tableauColloque);

    else :
        input("Commande inconnue.");
    

