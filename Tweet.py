#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Tweet:
    
    
    """ Classe définisant un utilisateur caractérisé par:
        - son Identifiant
        - son Mot de passe
        - son Nom
        - son prénom"""
    
    def __init__(self,text,date,id_utilisateur):
        self.text = text
        self.date = date
        self.id_utilisateur = id_utilisateur
