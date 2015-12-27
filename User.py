#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import select
import threading

import json




class User:
    
    thread = "";
    
    response = None;
    
    s = "";
    
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
    
    #On envoie l'action
    User.s.sendall(action.encode());





def traiteReponse(reponse):
    
    
    reponse = reponse.decode();
    
    # On affiche la réponse
    print(reponse.decode());
    
    #On detecte si l'utilisateur vient de se connecter
    if("Vous etes bien connectes" in reponse.decode()) :
        
        #On récupère le pseudo de l'utilisateur
        pseudo = reponse.decode().split(":")[1];
        pseudo = pseudo.replace("\n", "");
        User.metUtilisateurCourant(pseudo);

    elif("Vous avez ete deconnecte" in reponse.decode()) :
        
        User.deconnecteUtilisateur();



    #Si l'utilisateur est connecté, alors on affiche les autres actions
    if(User.utilisateurEstConnecte()) :
    
        proposeActions();
    
    else :
        actionsDebut();





def proposeActions():
    
    
    User.response = None;
    
    
    User.thread = threading.Thread(target=user_input_actions)
    #user.daemon = True
    User.thread.start()




def user_input_actions():
    
    print("Que voulez-vous faire ?");
    print("1- twitter : tweet –m <message> \n2- Vous abonnez : abonnement -p <utilisateur>\n3- Vous desabonnez : desabonnement -p <utilisateur> \n4- Vous déconnectez: disconnect -p <>\n5- Actualiser la file d'actualite: actu\n");
    User.response = input()



def actionsDebut():
    
    User.response = None;
    
    
    User.thread = threading.Thread(target=user_input_debut)
    #user.daemon = True
    User.thread.start()



def user_input_debut():
    
    print("Que voulez-vous faire ?");
    print("1- Nouvelle inscription : comptetw –p <pseudo> \n2- Vous connecter : tweet -p <pseudo> \n");
    User.response = input();



def main():
    pass

if __name__ == "__main__":
    
    
    #On connecte
    User.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    User.s.connect(("localhost", 50007));
    
    actionsDebut();
    main()
    
    
    
    
    
    
    while True :
        
        if(User.response is not None ):
            envoi(User.currentUser+" : "+User.response);
        
        
        
        try:
            clients_a_lire, wlist, xlist = select.select([User.s], [], [], 0.1);
    
        except select.error:
            
            pass
        else:
            
            # On parcourt la liste des clients à lire
            for client in clients_a_lire:
                
                data = client.recv(1024)
                
                User.thread.join(0.05);
                traiteReponse(data);





