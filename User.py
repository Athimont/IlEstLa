#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tweet
import socket


class User:
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









def proposeActions():

    print("Que voulez-vous faire ?");

    action = input("1- twitter : tweet –p <message> \n2- Vous abonnez : abonnement -p <abonnement> \n");



def actionsDebut():

    print("Que voulez-vous faire ?");
    
    action = input("1- Nouvelle inscription : comptetw –p <pseudo> \n2- Vous connecter : tweet -p <pseudo> \n");

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

    #Si l'utilisateur est connecté, alors on affiche les autres actions
    if("bien connectes" in reponse.decode()) :
        proposeActions();

    else :
        actionsDebut();


actionsDebut();
    
    
