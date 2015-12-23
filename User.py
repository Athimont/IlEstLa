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





print("Que voulez-vous faire ?");
    
action = input("1- Nouvelle inscription : comptetw –p <pseudo> \n2- Vous connecter : tweet -p <pseudo> \n");

#On connecte
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.connect(("localhost", 50007));
    
#On envoie l'action
s.sendall(action.encode());
    
reponse = s.recv(1024);
s.close();

print(reponse.decode());
    

    
    
