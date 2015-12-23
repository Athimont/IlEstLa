import socket

# ----- Centrale -----


def trieData (data) :
    action = data.decode();
    print(action);

    



        
#On demarre le serveur
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

#On ecoute le port 50007
s.bind(("localhost", 50007));

#On attend et on n'accepte qu'une seule connexion en meme temps
s.listen(1);

#On affiche qui se connecte
#conn, addr = s.accept()
#print 'Connected by', addr;
        
while True:
    
    conn, addr = s.accept();
    
    #On recupere les donnees
    print("Donnees recues par : "+addr);
    data = conn.recv(1024);
    #On trie ce qu'on a recu
    trieData(data);




        


