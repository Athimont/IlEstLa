#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

# ----- Centrale -----


def trieData (conn, data) :
    action = data.decode();
    print(action);

    if ("comptetw -p" in action) :
        actionOk = True;
        
        #On supprime l'action
        pseudo = action.replace("comptetw -p", "");
        
        #On supprime d'éventuels espaces
        pseudo = pseudo.replace(" ", "");
        
        print("On cree un nouveau compte avec comme pseudo :"+pseudo+"\n");
        res = ("Votre compte a bien ete cree : "+pseudo+"\n");
        conn.sendall(res.encode());
        conn.close();
    
    elif ("tweet -p" in action) :
        actionOk = True;
        
        #On supprime l'action
        pseudo = action.replace("tweet -p", "");
        
        #On supprime d'éventuels espaces
        pseudo = pseudo.replace(" ", "");
        
        print("Vous etes connecte en tant que : "+pseudo+"\n");
        res = ("Vous etes bien connectes : "+pseudo+"\n");
        conn.sendall(res.encode())
        conn.close();


    else :
        print("Erreur : Commande inconnue.");
        res = ("Erreur : Commande inconnue.\n");
        conn.sendall(res.encode())
        conn.close();







        
#On démarre le serveur
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

#On écoute le port 50007
s.bind(("localhost", 50007));

#On attend et on n'accepte qu'une seule connexion en même temps
s.listen(1);


        
while True:
    
    conn, addr = s.accept();
    
    #On recupere les données
    print("Donnees recues par : "+str(addr));
    data = conn.recv(1024);
    #On trie ce qu'on a recu
    trieData(conn, data);




        


