#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sqlite3
import datetime
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
            
            print("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            res = ("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            conn.sendall(res.encode())
            conn.close();
            return False;
        
    
        print("Vous avez ete deconnecte\n");
        res = ("Vous avez ete deconnecte\n");
        conn.sendall(res.encode())
        conn.close();



    elif ("desabonnement -p" in action) :
    
        # On vérifie que l'utilisateur est bien connecte
        if ( pseudoUtilisateur == ""):
        
            print("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            res = ("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            conn.sendall(res.encode())
            conn.close();
            return False;
        
        
        
        #On supprime l'action
        utilisateurSuivi = action.replace("desabonnement -p", "");
        print("e : "+utilisateurSuivi);
        #On supprime d'éventuels espaces
        utilisateurSuivi = utilisateurSuivi.replace(" ", "");
        
        # On s'assure que l'utilisateur à suivre existe bien
        suiviExiste = utilisateurExiste(utilisateurSuivi);
        
        if (not suiviExiste):
            print("Erreur : L'utilisateur n'existe pas.");
            res = ("Erreur : L'utilisateur n'existe pas.\n");
    
        else:
            
            #On regarde si l'utilisateur est déjà abonné
            dejaAbonne = abonnementExiste(pseudoUtilisateur, utilisateurSuivi);
            
            if (not dejaAbonne) :
                
                print("Vous devez être abonne a l'utilisateur pour vous desabonner\n");
                res = ("Vous devez être abonne a l'utilisateur pour vous desabonner\n");
        
            else :
                
                #On desabonne l'utilisateur
                bienDesabonne = desabonne(pseudoUtilisateur, utilisateurSuivi);
                
                if (bienDesabonne) :
                    
                    print("Vous n'etes plus abonne a l'utilisateur : "+utilisateurSuivi+"\n");
                    res = ("Vous n'etes plus abonne a l'utilisateur : "+utilisateurSuivi+"\n");
                
                else :
                    
                    print("Erreur : une erreur s'est produite lors de votre desabonnement\n");
                    res = ("Erreur : une erreur s'est produite lors de votre desabonnement\n");


        conn.sendall(res.encode())
        conn.close();
        
        afficheAbonnements();
    
    





    elif ("abonnement -p" in action) :
        
        # On vérifie que l'utilisateur est bien connecte
        if ( pseudoUtilisateur == ""):
            
            print("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            res = ("Erreur : Vous devez etre connecte pour effectuer cette action\n");
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
            
            #On regarde si l'utilisateur est déjà abonné
            dejaAbonne = abonnementExiste(pseudoUtilisateur, utilisateurSuivi);
            
            if (dejaAbonne) :

                print("Vous vous etes deja abonne a l'utilisateur : "+utilisateurSuivi+"\n");
                res = ("Vous vous etes deja abonne a l'utilisateur "+utilisateurSuivi+"\n");
            
            else :

                #On abonne l'utilisateur
                bienAbonne = abonne(pseudoUtilisateur, utilisateurSuivi);
            
                if (bienAbonne) :
            
                    print("Vous vous etes abonne a l'utilisateur : "+utilisateurSuivi+"\n");
                    res = ("Vous vous etes abonne a l'utilisateur "+utilisateurSuivi+"\n");

                else :
                
                    print("Erreur : une erreur s'est produite lors de votre abonnement\n");
                    res = ("Erreur : une erreur s'est produite lors de votre abonnement\n");
                        

        conn.sendall(res.encode())
        conn.close();

        afficheAbonnements();





    elif ("tweet -m" in action) :
        
        
        # On verifie que l'utilisateur est bien connecte
        if ( pseudoUtilisateur == ""):
            
            print("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            res = ("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            conn.sendall(res.encode())
            conn.close();
            return False;

    
        actionOk = True;
        
        #On supprime l'action
        message = action.replace("tweet -m", "");
        
        #On supprime d'éventuels espaces
        message = message.replace(" ", "");
        
        #On test que l'utilisateur existe bien
        tweetEnregistre = tweet(pseudoUtilisateur, message);
        
        
        if (tweetEnregistre):
            print("Votre tweet a bien été enregistre\n");
            res = ("Votre tweet a bien été enregistre\n");

        else :
            print("Erreur : Une erreur s'est produite lors de votre tweet\n");
            res = ("Erreur : Une erreur s'est produite lors de votre tweet\n");

        conn.sendall(res.encode())
        conn.close();

        afficheTweets();

    elif("actu" in action) :

        
        # On vérifie que l'utilisateur est bien connecte
        if ( pseudoUtilisateur == ""):
            
            print("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            res = ("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            conn.sendall(res.encode())
            conn.close();
            return False;

    
        actionOk = True;
        res = afficheActu(pseudoUtilisateur);
        
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

    id_abonne = getIdDeUtilisateur(abonne);
    utilisateurSuivi = getIdDeUtilisateur(utilisateurSuivi);

    data = {"id_abonne" : id_abonne, "id_user" : utilisateurSuivi}
    cursor.execute("""
        INSERT INTO Abonnement(id_Abonne, id_Utilisateur) VALUES(:id_abonne, :id_user)""", data)
    conn.commit();

    return abonnementExiste(abonne, utilisateurSuivi);



def desabonne (abonne, utilisateurSuivi):
    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    
    id_abonne = getIdDeUtilisateur(abonne);
    
    data = {"id_abonne" : id_abonne, "id_user" : utilisateurSuivi}
    cursor.execute("""
        DELETE FROM Abonnement where id_Abonne = :id_abonne and id_Utilisateur = :id_user""", data)
    conn.commit();
    
    return not abonnementExiste(abonne, utilisateurSuivi);




def abonnementExiste(abonne, utilisateurSuivi):
    
    conn = sqlite3.connect('base_tweet.db');

    id_abonne = getIdDeUtilisateur(abonne);

    cursor = conn.cursor();
    data = {"id_Abonne" : id_abonne , "id_Utilisateur" : utilisateurSuivi}
    cursor.execute("""SELECT * FROM Abonnement where id_Abonne = :id_Abonne and id_Utilisateur=:id_Utilisateur""", data)
    abonnement = cursor.fetchall();
    
    if (len(abonnement) > 0) :
        return True;
    else :
        return False;
        



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



def tweet(pseudo, message):
    
    conn = sqlite3.connect('base_tweet.db');
    
    id_Utilisateur = getIdDeUtilisateur(pseudo);
    
    cursor = conn.cursor();
    data = {"id_Utilisateur" : id_Utilisateur , "message" : message}
    cursor.execute("""
        INSERT INTO Tweet(id_Utilisateur, text) VALUES(:id_Utilisateur, :message)""", data)

    conn.commit();
    
    return tweetExiste(pseudo, message);




def tweetExiste(pseudo, message):
    
    conn = sqlite3.connect('base_tweet.db');
    
    id_Utilisateur = getIdDeUtilisateur(pseudo);
    
    cursor = conn.cursor();
    data = {"id_Utilisateur" : id_Utilisateur , "message" : message}
    cursor.execute("""SELECT * FROM Tweet where id_Utilisateur= :id_Utilisateur and text= :message""", data)
    
    tweet = cursor.fetchall();

    if (len(tweet) > 0) :
        return True
    else :
        return False




def getIdDeUtilisateur(pseudo) :

    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    data = {"pseudo" : pseudo}
    
    cursor.execute("""SELECT id FROM Utilisateur where pseudo= :pseudo""", data)
    users = cursor.fetchall();
    abonne = users[0];
    return abonne[0];





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


def afficheActu(pseudo):

    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    # changer utilisateur2 par l'id de l'utilisateur courrant
    data = {"id_currentUser" : getIdDeUtilisateur(pseudo)}
    cursor.execute("""SELECT id_Utilisateur FROM Abonnement WHERE id_Abonne = :id_currentUser""",data);
    abonnes = cursor.fetchall();
    listeTweet =[];
    for abo in abonnes:
        listeTweet.append(chercheTweet(abo[0]));
    strliste = "\n";
    for tweet in listeTweet :
        strliste = strliste + tweet + "\n";
    return strliste;


def chercheTweet(id_Abonne):
    
    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    data = {"id_Abonne" : id_Abonne};
    cursor.execute("""SELECT * FROM Tweet WHERE id_Utilisateur = :id_Abonne""",data);
    tweets = cursor.fetchall();
    return lePlusRecent(tweets);


def lePlusRecent(liste_Tweets):
    tweet = None;
    dateCurrent =None;
    #datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for t in liste_Tweets:
        dateT = traitementDate(t[3]);
        if tweet == None or dateT < dateCurrent:
            tweet = t[1];
            dateCurrent = dateT;
    if tweet == None:
        tweet = "Les utilisateurs pour lesquels vous etes abonne n'ont rien tweeter";
    return tweet;


def traitementDate(date):
    dateHeure = date.split(" ");
    dateSplit = dateHeure[0].split("-");
    heureSplit = dateHeure[1].split(":");
    date = datetime.datetime(int(dateSplit[2]),int(dateSplit[1]),int(dateSplit[0]),int(heureSplit[0]),int(heureSplit[1]),int(heureSplit[2]));
    return date


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





        


