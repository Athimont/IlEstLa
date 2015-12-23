#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sqlite3


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
        #conn.close();
    

    elif ("tweet -p" in action) :
        actionOk = True;
        
        #On supprime l'action
        pseudo = action.replace("tweet -p", "");
        
        #On supprime d'éventuels espaces
        pseudo = pseudo.replace(" ", "");
        
        print("Vous etes connecte en tant que : "+pseudo+"\n");
        res = ("Vous etes bien connectes : "+pseudo+"\n");
        conn.sendall(res.encode())
        #conn.close();


    else :
        print("Erreur : Commande inconnue.");
        res = ("Erreur : Commande inconnue.\n");
        conn.sendall(res.encode())
        #conn.close();






def reinitialiseBase():

    conn = sqlite3.connect('base_tweet.db');
    
    #On supprime la table si elle existe
    cursor = conn.cursor();
    cursor.execute("""
        DROP TABLE IF EXISTS Utilisateur;
        """);
    conn.commit();

    # On crée la nouvelle
    cursor = conn.cursor();
    cursor.execute("""
        CREATE TABLE Utilisateur(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        pseudo varchar(255)
        )
    """)
    conn.commit();


    # On insert des utilisateurs
    cursor = conn.cursor();
    data = {"pseudo" : "moncul"}
    cursor.execute("""
        INSERT INTO Utilisateur(pseudo) VALUES(:pseudo)""", data)
    conn.commit();

    cursor = conn.cursor();
    data = {"pseudo" : "moncul2"}
    cursor.execute("""
        INSERT INTO Utilisateur(pseudo) VALUES(:pseudo)""", data)
    conn.commit();


    #Base utilisateur
    cursor.execute("""SELECT * FROM Utilisateur""")
    user1 = cursor.fetchone()
    print(user1)





action = input("Que voulez-vous faire ? ");

if(action == "servtw") :

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


elif(action == "base") :
    reinitialiseBase();



        


