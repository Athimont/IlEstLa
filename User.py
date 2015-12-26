#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tweet
import socket




class User:

    currentUser = "";

    """ Classe définisant un utilisateur caractérisé par:
        - son Identifiant
	- son Mot de passe
	- son Nom
	- son prénom"""
    
    def __init__(self,identifiant,password,nom,prenom):
        self.id = identifiant
        self.password = password
        self.nom = nom
        self.prenom = prenom

	#def publie (text):
		
	#def abonne (user):

	#def desabonne (user):	

	#def affichecompte ():

	#def afficheabonnement ():

	#def connecte ():

	#def deconnecte ():


    @staticmethod
    def metUtilisateurCourant(pseudo):
        User.currentUser = pseudo;


    @staticmethod
    def utilisateurEstConnecte():
        return (not (User.currentUser==""));



    @staticmethod
    def connecteUtilisateur(pseudo):
        User.currentUser = pseudo;


    @staticmethod
    def deconnecteUtilisateur():
        User.currentUser = "";



def envoi(action):
    #On connecte
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.connect(("localhost", 50007));
    
    #On envoie l'action
    s.sendall(action.encode());
    
    #On récupère la réponse de centrale
    reponse = s.recv(1024);
    
    #on ferme la connection
    #s.close();

    # On affiche la réponse
    print(reponse.decode());
    
    #On detecte si l'utilisateur vient de se connecter
    if("Vous etes bien connectes" in reponse.decode()) :
    
        #On récupère le pseudo de l'utilisateur
        pseudo = reponse.decode().split(":")[1];
        pseudo = pseudo.replace("\n", "");
        User.metUtilisateurCourant(pseudo);
    

    #Si l'utilisateur est connecté, alors on affiche les autres actions
    if(User.utilisateurEstConnecte()) :
        proposeActions();

    else :
        actionsDebut();



def proposeActions():

    print("Que voulez-vous faire ?");

    action = input("1- twitter : tweet –m <message> \n2- Vous abonnez : abonnement -p <abonnement> \n3- Vous déconnectez: disconnect -p <>\n");

    envoi(User.currentUser+" : "+action);



def actionsDebut():

    print("Que voulez-vous faire ?");
    
    action = input("1- Nouvelle inscription : comptetw –p <pseudo> \n2- Vous connecter : tweet -p <pseudo> \n");

    envoi(User.currentUser+" : "+action);


def main():
    pass

if __name__ == "__main__":

    actionsDebut();

    main()


    
