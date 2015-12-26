#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sqlite3
from User import User

# ----- Centrale ----



def trieData (conn, data) :

    # On récupère l'action
    actionBrut = data.decode();
    
    print(actionBrut);
    
    # On sépare l'action du pseudo de l'utilisateur
    pseudoUtilisateur = actionBrut.split(":")[0];
    pseudoUtilisateur = pseudoUtilisateur.replace(" ", "");
    
    #On récupère l'action
    action = actionBrut.split(":")[1];
    
    print(action);

    if ("comptetw -p" in action) :
        actionOk = True;
        
        #On supprime l'action
        pseudo = action.replace("comptetw -p", "");
        
        #On supprime d'éventuels espaces
        pseudo = pseudo.replace(" ", "");
        
        #On vérifie que le pseudo est libre
        utilise = utilisateurExiste(pseudo);
        if(utilise) :
        
            reponse = ("Erreur : ce pseudo est deja pris\n");

        else :
        
            print("On cree un nouveau compte avec comme pseudo :"+pseudo+"\n");

            #On cree le compte
            res = creerCompte(pseudo);
        
            if(res):
                reponse = ("Votre compte a bien ete cree : "+pseudo+"\n");
        
            else :
                reponse = ("Erreur : Une erreur s'est produite lors de votre inscription, veuillez reessayer\n");

        conn.sendall(reponse.encode());
        conn.close();

        afficheUtilisateurs();
    



    elif ("tweet -p" in action) :

        actionOk = True;
        
        #On supprime l'action
        pseudo = action.replace("tweet -p", "");
        
        #On supprime d'éventuels espaces
        pseudo = pseudo.replace(" ", "");
        
        #On test que l'utilisateur existe bien
        connecte = utilisateurExiste(pseudo);
        
        
        if (connecte):
            print("Vous etes connecte en tant que : "+pseudo+"\n");
            res = ("Vous etes bien connectes : "+pseudo+"\n");

        else :
            print("Erreur : Cet utilisateur n'existe pas : "+pseudo+"\n");
            res = ("Erreur : Cet utilisateur n'existe pas : "+pseudo+"\n");
        conn.sendall(res.encode())
        conn.close();




    elif ( "disconnect -p" in action) :
        
        # On vérifie que l'utilisateur est bien connecte
        if ( pseudoUtilisateur == ""):
            
            print("Erreur : Vous devez etre connecté pour effectuer cette action\n");
            res = ("Erreur : Vous devez etre connecté pour effectuer cette action\n");
            conn.sendall(res.encode())
            conn.close();
            return False;
        
        User.deconnecteUtilisateur();
    
        print("Vous avez ete deconnecte\n");
        res = ("0 : Vous avez ete deconnecte\n");
        conn.sendall(res.encode())
        conn.close();






    elif ("abonnement -p" in action) :
        
        # On vérifie que l'utilisateur est bien connecte
        if ( pseudoUtilisateur == ""):
            
            print("Erreur : Vous devez etre connecté pour effectuer cette action\n");
            res = ("Erreur : Vous devez etre connecté pour effectuer cette action\n");
            conn.sendall(res.encode())
            conn.close();
            return False;



        #On supprime l'action
        utilisateurSuivi = action.replace("abonnement -p", "");
        
        #On supprime d'éventuels espaces
        utilisateurSuivi = utilisateurSuivi.replace(" ", "");

        # On s'assure que l'utilisateur à suivre existe bien
        suiviExiste = utilisateurExiste(utilisateurSuivi);

        if (not suiviExiste):
            print("Erreur : L'utilisateur n'existe pas.");
            res = ("Erreur : L'utilisateur n'existe pas.\n");

        else:
            
            #On abonne l'utilisateur
            abonne(pseudoUtilisateur, utilisateurSuivi);
            
            
            print("Vous vous etes abonne a l'utilisateur : "+utilisateurSuivi+"\n");
            res = ("Vous vous etes abonne a l'utilisateur "+utilisateurSuivi+"\n");

        conn.sendall(res.encode())
        conn.close();




    else :
        print("Erreur : Commande inconnue.");
        res = ("Erreur : Commande inconnue.\n");
        conn.sendall(res.encode())
        conn.close();





def creerCompte(pseudo):

    conn = sqlite3.connect('base_tweet.db');
    # On insert l'utilisateurs
    cursor = conn.cursor();
    data = {"pseudo" : pseudo}
    cursor.execute("""
        INSERT INTO Utilisateur(pseudo) VALUES(:pseudo)""", data)
    conn.commit();

    return utilisateurExiste(pseudo);


def abonne (abonne, utilisateurSuivi):
    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    data1 = {"pseudo" : abonne}


    cursor.execute("""SELECT id FROM Utilisateur where pseudo= :pseudo""", data1)
    users = cursor.fetchall();
    abonne = users[0];
    abonne = abonne[0];

    data2 = {"id_abonne" : abonne, "id_user" : utilisateurSuivi}
    cursor.execute("""
        INSERT INTO adonne(id_Abonne, id_Utilisateur) VALUES(:id_abonne, :id_user)""", data2)
    conn.commit();
    


#def trouveAbonne(pseudo):
#    
#    conn = sqlite3.connect('base_tweet.db');
#
#    cursor = conn.cursor();
#    data = {"pseudo" : pseudo}
#    cursor.execute("""SELECT id FROM Utilisateur where pseudo= :pseudo""", data)
#    users = cursor.fetchall();
#    if (len(users) > 0) :
#        abonne (users[0]);
#        return users[0];
#    else:
#        return False;
#        



def utilisateurExiste(pseudo):

    conn = sqlite3.connect('base_tweet.db');

    cursor = conn.cursor();
    data = {"pseudo" : pseudo}
    cursor.execute("""SELECT * FROM Utilisateur where pseudo= :pseudo""", data)
    users = cursor.fetchall();
    if (len(users) > 0) :
        return True
    else :
        return False






def reinitialiseBase():

    conn = sqlite3.connect('base_tweet.db');
    
    #----- PARTIE UTILISATEUR -----

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
    data = {"pseudo" : "utilisateur1"}
    cursor.execute("""
        INSERT INTO Utilisateur(pseudo) VALUES(:pseudo)""", data)
    conn.commit();

    cursor = conn.cursor();
    data = {"pseudo" : "utilisateur2"}
    cursor.execute("""
        INSERT INTO Utilisateur(pseudo) VALUES(:pseudo)""", data)
    conn.commit();


    #On affiche les utilisateurs
    afficheUtilisateurs();




    #----- PARTIE TWEET -----
    
    #On supprime la table si elle existe
    cursor = conn.cursor();
    cursor.execute("""
        DROP TABLE IF EXISTS Tweet;
        """);
    conn.commit();
    
    # On crée la nouvelle
    cursor = conn.cursor();
    cursor.execute("""
        CREATE TABLE Tweet(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        text varchar(120),
        id_Utilisateur INTEGER
        )
        """)
    conn.commit();
    
    
    # On insert des utilisateurs
    cursor = conn.cursor();
    data = {"text" : "Premier tweet de l'utilisteur 1", "id_Utilisateur" : "1"}
    cursor.execute("""
        INSERT INTO Tweet(text, id_Utilisateur) VALUES(:text, :id_Utilisateur)""", data)
    conn.commit();
    
    cursor = conn.cursor();
    data = {"text" : "deuxieme tweet de l'utilisteur 1", "id_Utilisateur" : "1"}
    cursor.execute("""
        INSERT INTO Tweet(text, id_Utilisateur) VALUES(:text, :id_Utilisateur)""", data)
    conn.commit();
    
    cursor = conn.cursor();
    data = {"text" : "Premier tweet de l'utilisteur 2", "id_Utilisateur" : "2"}
    cursor.execute("""
        INSERT INTO Tweet(text, id_Utilisateur) VALUES(:text, :id_Utilisateur)""", data)
    conn.commit();
    
    
    #On affiche les utilisateurs
    afficheTweets();




    #----- PARTIE ABONNEMENT -----

    #On supprime la table si elle existe
    cursor = conn.cursor();
    cursor.execute("""
        DROP TABLE IF EXISTS Abonnement;
        """);
    conn.commit();
    
    # On crée la nouvelle
    cursor = conn.cursor();
    cursor.execute("""
        CREATE TABLE Abonnement(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        id_Abonne INTEGER,
        id_Utilisateur INTEGER
        )
        """)
    conn.commit();
    
    






def afficheUtilisateurs():

    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    cursor.execute("""SELECT * FROM Utilisateur""")
    users = cursor.fetchall();
    print(users)




def afficheTweets():
    
    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    cursor.execute("""SELECT * FROM Tweet""")
    tweets = cursor.fetchall();
    print(tweets)


def afficheAbonnements():
    
    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    cursor.execute("""SELECT * FROM Abonnement""")
    abonnements = cursor.fetchall();
    print(abonnements)






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



        


