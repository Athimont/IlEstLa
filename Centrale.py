#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import select
import time

import sqlite3
import datetime
import json

from User import User
from Tweet import Tweet

# ----- Centrale ----

dictionnaireAddrAbo = {};

dictionnaireAddrConn = {};

"""
Cette methode premet au programme de determiner quelle est 
l'action choisie par l'utilisateur et de lancer les methode 
necessaire au bon fonctionnement de l'action
addr : l'adresse de l'utilisateur
conn : le client d'un utilisateur
data : action brut d'un utilisateur encodee
"""
def trieData (addr, conn, data) :
    
    
    # On récupère l'action
    actionBrut = data.decode();
    print(actionBrut);
    
    # On sépare l'action du pseudo de l'utilisateur
    pseudoUtilisateur = actionBrut.split(":")[0];
    pseudoUtilisateur = pseudoUtilisateur.replace(" ", "");
    
    #On récupère l'action
    action = actionBrut.split(":")[1];
    
    print(action);
    # creation d'un nouveau compte
    if ("comptetw -p" in action) :
        
        # On vérifie que l'utilisateur est bien connecte
        if ( pseudoUtilisateur != ""):
            
            print("Erreur : Vous devez etre deconnecte pour effectuer cette action\n");
            res = ("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            conn.sendall(res.encode())
            #conn.close();
            return False;
    
    
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
        #conn.close();
    
        afficheUtilisateurs();
    # connexion d'un utilisateur
    elif ("tweet -p" in action) :
        
        # On vérifie que l'utilisateur est bien connecte
        if ( pseudoUtilisateur != ""):
            
            print("Erreur : Vous devez etre deconnecte pour effectuer cette action\n");
            res = ("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            conn.sendall(res.encode())
            #conn.close();
            return False;
    
    
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
            
            # On met a jour la liste des abonnement pour l'utilisateur
            metAJourAbonnementPourPseudoEtAdresse(pseudo, addr);
            
            
            print(str(dictionnaireAddrAbo));
        
        
        else:
            print("Erreur : Cet utilisateur n'existe pas : "+pseudo+"\n");
            res = ("Erreur : Cet utilisateur n'existe pas : "+pseudo+"\n");

        conn.sendall(res.encode())
    # deconnexion d'un utilisateur
    elif ( "disconnect -p" in action) :
    
        # On vérifie que l'utilisateur est bien connecte
        if ( pseudoUtilisateur == ""):
        
            print("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            res = ("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            conn.sendall(res.encode())
            #conn.close();
            return False;
        
        
        print("Vous avez ete deconnecte\n");
        res = ("Vous avez ete deconnecte\n");
        conn.sendall(res.encode())
    # desobonnement a un utilisateur
    elif ("desabonnement -p" in action) :
        
        # On vérifie que l'utilisateur est bien connecte
        if ( pseudoUtilisateur == ""):
            
            print("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            res = ("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            conn.sendall(res.encode())
            #conn.close();
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
                
                print("Vous devez etre abonne a l'utilisateur pour vous desabonner\n");
                res = ("Vous devez etre abonne a l'utilisateur pour vous desabonner\n");

            else :
                
                #On desabonne l'utilisateur
                bienDesabonne = desabonne(pseudoUtilisateur, utilisateurSuivi);
                
                # On met a jour la liste des abonnement pour l'utilisateur
                metAJourAbonnementPourPseudoEtAdresse(pseudoUtilisateur, addr);
                
                
                if (bienDesabonne) :
                    
                    print("Vous n'etes plus abonne a l'utilisateur : "+utilisateurSuivi+"\n");
                    res = ("Vous n'etes plus abonne a l'utilisateur : "+utilisateurSuivi+"\n");
                
                else :
                    
                    print("Erreur : une erreur s'est produite lors de votre desabonnement\n");
                    res = ("Erreur : une erreur s'est produite lors de votre desabonnement\n");


        conn.sendall(res.encode())
    
        afficheAbonnements();
    # abonnement a un utilisateur
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
                
                # On met a jour la liste des abonnement pour l'utilisateur
                metAJourAbonnementPourPseudoEtAdresse(pseudoUtilisateur, addr);
                
                
                if (bienAbonne) :
                    
                    print("Vous vous etes abonne a l'utilisateur : "+utilisateurSuivi+"\n");
                    res = ("Vous vous etes abonne a l'utilisateur "+utilisateurSuivi+"\n");
            
                else :
                    
                    print("Erreur : une erreur s'est produite lors de votre abonnement\n");
                    res = ("Erreur : une erreur s'est produite lors de votre abonnement\n");


        conn.sendall(res.encode())
    
        afficheAbonnements();
    # publication d'un tweet
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
        tweetEnregistre = envoieTweet(pseudoUtilisateur, message);
        
        
        if (tweetEnregistre):
            print("Votre tweet a bien ete enregistre\n");
            res = ("Votre tweet a bien ete enregistre\n");
        
        else :
            print("Erreur : Une erreur s'est produite lors de votre tweet\n");
            res = ("Erreur : Une erreur s'est produite lors de votre tweet\n");
    
        conn.sendall(res.encode())
        #conn.close();
        
        afficheTweets();
        
        time.sleep(0.5);
        
        print("On lance les avertissements");
        # On lance l'avertissement aux abonnés
        lanceAvertissement(pseudoUtilisateur, conn);
    # affichage de la file d'actualite
    elif("actu" in action) :
    
    
        # On vérifie que l'utilisateur est bien connecte
        if ( pseudoUtilisateur == ""):
        
            print("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            res = ("Erreur : Vous devez etre connecte pour effectuer cette action\n");
            conn.sendall(res.encode())
            conn.close();
            return False;
    
    
        actionOk = True;
        tweets = afficheActu(pseudoUtilisateur);
        
        # On trie les tweets par leur date
        tweets = sorted(tweets, key=getTweetKey, reverse=True);
        
        strTweets = "Mes tweets : \n"
        
        for tweet in tweets:
            strTweets = strTweets+tweet.date+" : "+getPseudoPourId(tweet.id_utilisateur)+" : "+tweet.text+"\n";


        conn.sendall(strTweets.encode());
        #conn.close();
    # commande non suporte par le programme
    else :
        print("Erreur : Commande inconnue.");
        res = ("Erreur : Commande inconnue.\n");
        conn.sendall(res.encode())
        conn.close();

"""
Cette methode permet la creation d'un compte en base de donnees
on passe le pseudo de l'utilisateur en parametre afin qu'il soit
enregistre en base de donnees
"""
def creerCompte(pseudo):
    
    conn = sqlite3.connect('base_tweet.db');
    # On insert l'utilisateurs
    cursor = conn.cursor();
    data = {"pseudo" : pseudo}
    cursor.execute("""
        INSERT INTO Utilisateur(pseudo) VALUES(:pseudo)""", data)
    conn.commit();
    
    return utilisateurExiste(pseudo);

"""
Cette methode permet d'ajouter un abonnement a un utilisateur
abonne : l'utilisateur qui s'abonne
utilisateurSuivi : l'utilisateur auquel on s'abonne.
"""
def abonne (abonne, utilisateurSuivi):
    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    
    id_abonne = getIdDeUtilisateur(abonne);
    id_UtilisateurSuivi = getIdDeUtilisateur(utilisateurSuivi);
    
    data = {"id_abonne" : id_abonne, "id_user" : id_UtilisateurSuivi}
    cursor.execute("""
        INSERT INTO Abonnement(id_Abonne, id_Utilisateur) VALUES(:id_abonne, :id_user)""", data)
    conn.commit();
    
    return abonnementExiste(abonne, utilisateurSuivi);

"""
Cette methode permet de supprimer un abonnement a un utilisateur
abonne : l'utilisateur qui se desabonne
utilisateurSuivi : l'utilisateur auquel on se desabonne.
"""
def desabonne (abonne, utilisateurSuivi):
    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    
    id_abonne = getIdDeUtilisateur(abonne);
    id_UtilisateurSuivi = getIdDeUtilisateur(utilisateurSuivi);
    
    data = {"id_abonne" : id_abonne, "id_user" : id_UtilisateurSuivi}
    cursor.execute("""
        DELETE FROM Abonnement where id_Abonne = :id_abonne and id_Utilisateur = :id_user""", data)
    conn.commit();
    
    return not abonnementExiste(abonne, utilisateurSuivi);

"""
Cette methode permet de savoir si un abonnement existe bien entre
deux utilisateurs.
abonne : l'utilisateur qui est abonne
utilisateurSuivi : l'utilisateur auquel on est abonne.
"""
def abonnementExiste(abonne, utilisateurSuivi):
    
    conn = sqlite3.connect('base_tweet.db');
    
    id_abonne = getIdDeUtilisateur(abonne);
    id_UtilisateurSuivi = getIdDeUtilisateur(utilisateurSuivi);
    
    cursor = conn.cursor();
    data = {"id_Abonne" : id_abonne , "id_Utilisateur" : id_UtilisateurSuivi}
    cursor.execute("""SELECT * FROM Abonnement where id_Abonne = :id_Abonne and id_Utilisateur=:id_Utilisateur""", data)
    abonnement = cursor.fetchall();
    
    if (len(abonnement) > 0) :
        return True;
    else :
        return False;

"""
Cette methode verifie l'existance d'un utilisateur
on passe ne parametre le pseudo de l'utilisateur a verifier
"""
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

"""
Cette methode permet le publication d'un tweet
pseudo : le pseudo de l'utilisateur qui publie le tweet
message : le message contenu dans le tweet
"""
def envoieTweet(pseudo, message):
    
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S");
    conn = sqlite3.connect('base_tweet.db');
    
    id_Utilisateur = getIdDeUtilisateur(pseudo);
    
    cursor = conn.cursor();
    data = {"id_Utilisateur" : id_Utilisateur , "message" : message, "date" : date}
    cursor.execute("""
        INSERT INTO Tweet(id_Utilisateur, text, date_Publication) VALUES(:id_Utilisateur, :message, :date)""", data)
    
    conn.commit();
    
    return tweetExiste(pseudo, message);

"""
Cette methode permet de verifier qu'un tweet existe
pseudo : le pseudo de l'utilisateur qui a publie le tweet
message : le message contenu dans le tweet
"""
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

"""
Cette methode permet de recuperer l'id d'un utilisateur
grace a son pseudo
on passe donc le pseudo de l'utilisateur rechercher en parametre.
"""
def getIdDeUtilisateur(pseudo) :
    
    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    data = {"pseudo" : pseudo}
    
    cursor.execute("""SELECT id FROM Utilisateur where pseudo= :pseudo""", data)
    users = cursor.fetchall();
    abonne = users[0];
    return abonne[0];

"""
Cette methode permet de recuperer tous les abonnement d'un utilisateur
on passe l'id d'un utilisateur en parametre
"""
def getAbonnementsPourUtilisateur(id):
    
    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    data = {"id" : id}
    
    cursor.execute("""SELECT id_Utilisateur FROM Abonnement where id_Abonne= :id""", data)
    abonnements = cursor.fetchall();
    
    listeAbonnements = [];
    
    for abonnement in abonnements :
        listeAbonnements.append(abonnement[0]);
    
    return listeAbonnements;

"""
Cette methode permet de recuperer le pseudo d'un 
utilisateur a partir de son idon passe donc l'id de
l'utilisateur en parametre
"""
def getPseudoPourId(id):
    
    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    data = {"id" : id}
    
    cursor.execute("""SELECT pseudo FROM Utilisateur where id= :id""", data)
    users = cursor.fetchall();
    pseudo = users[0];
    return pseudo[0];

"""
Cette methode permet au programme de tenir informer les abonnes d'un
utilisateur qu'il vient de publier un tweet
pseudo : pseudo de l'utilisateur qui publie le tweet
conn : le client d'un utilisateur
"""
def lanceAvertissement(pseudo, conn):
    
    
    id_U = getIdDeUtilisateur(pseudo);
    
    for addr, listeAbo in dictionnaireAddrAbo.items() :
        
        if id_U in listeAbo :
            conn = dictionnaireAddrConn[addr];
            message = "De nouveaux tweets sont disponibles pour vous\n";
            conn.sendall(message.encode());

"""
Cette methode permet de mettre a jour la liste des abonnes d'un
utilisateur en fonction de son pseudo et de son adresse.
"""
def metAJourAbonnementPourPseudoEtAdresse(pseudoUtilisateur, addr):
    #On va chercher les abo de l'utilisateur
    listeAbonnements = getAbonnementsPourUtilisateur(getIdDeUtilisateur(pseudoUtilisateur));
    
    #On stocke la liste dans le dictionnaire
    dictionnaireAddrAbo[addr] = listeAbonnements;

"""
Cette methode permet de reinitialiser la base de donnees
"""
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
        id_Utilisateur INTEGER,
        date_Publication datetime
        )
        """)
    conn.commit();
    
    
    # On insert des utilisateurs
    maintenant = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor = conn.cursor();
    data = {"text" : "Premier tweet de l'utilisteur 1", "id_Utilisateur" : "1" , "date_Publication" : maintenant}
    cursor.execute("""
        INSERT INTO Tweet(text, id_Utilisateur, date_Publication) VALUES(:text, :id_Utilisateur, :date_Publication)""", data)
    conn.commit();
    
    cursor = conn.cursor();
    data = {"text" : "deuxieme tweet de l'utilisteur 1", "id_Utilisateur" : "1", "date_Publication" : maintenant}
    cursor.execute("""
        INSERT INTO Tweet(text, id_Utilisateur, date_Publication) VALUES(:text, :id_Utilisateur, :date_Publication)""", data)
    conn.commit();
    
    cursor = conn.cursor();
    data = {"text" : "Premier tweet de l'utilisteur 2", "id_Utilisateur" : "2", "date_Publication" : maintenant}
    cursor.execute("""
        INSERT INTO Tweet(text, id_Utilisateur, date_Publication) VALUES(:text, :id_Utilisateur, :date_Publication)""", data)
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

"""
Cette methode permet d'afficher tous les utilisateurs
"""
def afficheUtilisateurs():
    
    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    cursor.execute("""SELECT * FROM Utilisateur""")
    users = cursor.fetchall();
    print(users)

"""
Cette methode permet d'afficher tous les tweets
"""
def afficheTweets():
    
    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    cursor.execute("""SELECT * FROM Tweet""")
    tweets = cursor.fetchall();
    print(tweets)

"""
Cette methode permet d'afficher tous les abonnements
"""
def afficheAbonnements():
    
    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    cursor.execute("""SELECT * FROM Abonnement""")
    abonnements = cursor.fetchall();
    print(abonnements)

"""
Cette methode permet a un utilisateur d'afficher
sa file d'actualite
On passe donc en parametre le pseudo de l'utilisateur 
qui veux afficher sa file d'actualite
"""
def afficheActu(pseudo):
    
    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    # changer utilisateur2 par l'id de l'utilisateur courrant
    data = {"id_currentUser" : getIdDeUtilisateur(pseudo)}
    cursor.execute("""SELECT id_Utilisateur FROM Abonnement WHERE id_Abonne = :id_currentUser""",data);
    abonnes = cursor.fetchall();
    print(abonnes);
    listeTweet =[];
    for abo in abonnes:
        tweets = chercheTweet(abo[0]);
        
        for tweet in tweets:
            listeTweet.append(Tweet(tweet[1],tweet[3],tweet[2]));

    return listeTweet;

"""
Cette methode permet de rechercher les tweets 
d'un utilisateur
on passe donc l'id de l'utilisateur en parametre
"""
def chercheTweet(id_Utilisateur):
    
    conn = sqlite3.connect('base_tweet.db');
    cursor = conn.cursor();
    data = {"id_Utilisateur" : id_Utilisateur};
    cursor.execute("""SELECT * FROM Tweet WHERE id_Utilisateur = :id_Utilisateur""",data);
    tweets = cursor.fetchall();
    
    return tweets;

"""
Cette methode permet de retourner la date d'un tweet
on passe donc un tweet en parametre
"""
def getTweetKey(tweet):
    return tweet.date;


#def lePlusRecent(liste_Tweets):
#    tweet = None;
#    dateCurrent =None;
#    #datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#    for t in liste_Tweets:
#        dateT = traitementDate(t[3]);
#        if tweet == None or dateT < dateCurrent:
#            tweet = t[1];
#            dateCurrent = dateT;
#    if tweet == None:
#        tweet = "Les utilisateurs pour lesquels vous etes abonne n'ont rien tweeter";
#    return tweet;

"""
Cette methode permet de passer une date string
en une date datetime
on passe donc une date string en parametre
"""
def traitementDate(date):
    dateHeure = date.split(" ");
    dateSplit = dateHeure[0].split("-");
    heureSplit = dateHeure[1].split(":");
    date = datetime.datetime(int(dateSplit[2]),int(dateSplit[1]),int(dateSplit[0]),int(heureSplit[0]),int(heureSplit[1]),int(heureSplit[2]));
    return date

"""
Voici ce qui est le main de ce programme il vas 
soit ecouter les utilisateurs 
soit mettre a jour la base de donnees
"""
action = input("Que voulez-vous faire ? ");

if(action == "servtw") :
    
    #On démarre le serveur
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    
    #On écoute le port 50007
    s.bind(("localhost", 50007));
    
    #On attend et on n'accepte qu'une seule connexion en même temps
    s.listen(5);
    
    
    
    while True:
        
        
        # On actualise la liste des clients qui veulent se connecter
        # On attend maximum 50ms
        connexions_demandees, wlist, xlist = select.select([s], [], [], 0.05);
        
        # On boucle sur les connexions qui ont été demandées
        for connexion in connexions_demandees:
            connexion_avec_client, addr = connexion.accept();
            # On ajoute le socket connecté à la liste des clients
            dictionnaireAddrConn[addr] = connexion_avec_client;
        
        
        
        
        
        
        # Une fois qu'on a actualisé la liste des clients connectés,
        # On detecte ceux qui envoient
        # On attend encore 50ms maximum
        
        # On utilise un bloc try car si la liste est vide = exception
        
        clients_a_lire = [];
        try:
            clients_a_lire, wlist, xlist = select.select(dictionnaireAddrConn.values(), [], [], 0.05);
    
        except select.error:
            pass
        else:
            
            # On parcourt la liste des clients à lire
            for client in clients_a_lire:
                
                data = client.recv(1024)
                
                addr = "";
                
                for addresse, co in dictionnaireAddrConn.items():
                    if co == client:
                        addr = addresse;
                
                print(addr);
                
                # Peut planter si le message contient des caractères spéciaux
                trieData(addr, client, data);






elif(action == "base") :
    reinitialiseBase();



else :
    
    print("Commande inconnue");








