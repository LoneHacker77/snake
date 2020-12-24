# Snake - Mars 2020
# subscribe: https://www.youtube.com/channel/UCXW1DF8zRbYTo4xRcFSUW7Q




# Initialisation

# Modules
from kandinsky import *
from ion import keydown
from time import monotonic
from random import choice

def wait(buttons = range(53)): # Attends qu'une des touches précisées soit pressée
    while True:
        for i in buttons:
            if keydown(i):
                while keydown(i): True # Fonction anti-rebond
                return i

def omega(): # Vérificateur d'OS
    try: get_keys()
    except: return False
    else: return True

# Positionnement
mh = 20 # Marge du haut
mg = 20 # Marge à gauche
ae = 15 # Aération
esp = 5 # Espacement
b = [150,300] # Bornes pour les options

# Couleurs
ome = (192,53,53) # Couleur d'Omega
eps = (255,183,52) # Couleur d'Epsilon
act = eps # Couleur de l'objet actif
n = (0,0,0) # Titre, options
g = (70,70,70) # Paramètres, curseur

def menu(titre, action, *para):
    # Fonctions graphiques
    def draw_action(col): # Actualise l'apparence de l'action
        draw_string(action, int(160-5*len(action)), mh+20+ae, col)
    def draw_option(i, col): # Actualise l'apparence de l'option du paramètre i
        draw_string(" "*int((b[1]-b[0])/10), b[0], mh+2*(20+ae)+i*(20+esp))
        txt = str(para[i][aff[i]])
        if txt.find("$") != -1: # Affichage de plusieurs lignes
            txt, txt2 = txt[:txt.find("$")], txt[txt.find("$")+1:] # Séparation de l'option
            draw_string(" "*32, 0, mh+2*(20+ae)+(i+1)*(20+esp)) # Effacement de la ligne suivante
            draw_string(str(txt2), 160-5*len(txt2), mh+2*(20+ae)+(i+1)*(20+esp), col)
        draw_string(txt, int(b[0]+(b[1]-b[0]-10*len(str(txt)))/2), mh+2*(20+ae)+i*(20+esp), col)
        draw_string(("<"*(col==act)+" ")[0], b[0]-10, mh+2*(20+ae)+i*(20+esp), g) # Curseur gauche
        draw_string((">"*(col==act)+" ")[0], b[1], mh+2*(20+ae)+i*(20+esp), g) # Curseur droit

    # Initialisation du menu
    fill_rect(0,0,320,222,(255,255,255))
    if omega(): act = ome # Adaptation de la couleur à l'OS
    else: act = eps
    aff = [1 for i in para]
    curs = 0 # Initialisation sur l'action
    draw_string(titre, int(160-5*len(titre)), mh, n) # Titre
    draw_action(act) # Action
    for i in range(len(para)): # Paramètres
        draw_string(para[i][0], mg, mh+2*(20+ae)+i*(20+esp), n)
        draw_option(i, g)

    # Naviguation dans le menu
    while True:
        if curs == 0: # Action
            draw_action(act)
            r = wait([1,2,4])
            if r == 4: # Retourne les valeurs validées
                return [para[i][aff[i]] for i in range(len(para))]
            else:
                draw_action(n)
        else: # Paramètre
            draw_option(curs-1, act)
            r = wait([0,1,2,3])
            if r in [1,2]: draw_option(curs-1, g)

        # Actualisation des options actuelles et du curseur
        if r == 0: aff[curs-1] = (aff[curs-1]-2)%(len(para[curs-1])-1)+1
        elif r == 1: curs = (curs-1)%(len(para)+1)
        elif r == 2: curs = (curs+1)%(len(para)+1)
        elif r == 3: aff[curs-1] = (aff[curs-1])%(len(para[curs-1])-1)+1


# Couleurs
back = (255,255,255) # Arrière-plan
imp = (0,0,0) # Bordure, titres, menus
sub = (70,70,70) # Score, auteur
body = (0, 204, 0) # Corps du serpent
bord = (0, 104, 0) # Bordures du serpent
red = (248, 0, 0) # Langue, yeux, pomme
red_dark = (200, 0, 0) # Pomme




# Fonctionnement

def start(): # Lance le jeu
    try: para = menu("SNAKE", "Lancer la partie", ["Mode","Classique","Dingue"], ["Difficulté","Moyen","Difficile"," Extrême","Facile"], ["Bordures","Mortelles","  Téléportation"], ["Commandes"," Nav: Flèches","Menu: HOME","Rejouer: OK"], ["Crédits","Arthur J.","Vincent R."])
    except: para = ["Classique","Moyen","Mortelles"]
    play(para)




# Boucle principale

def play(para):
    # Power-ups
    def pom():
        up = [choice(range(32)), choice(range(20))]
        while get_pixel(10*up[0], 22 + 10*up[1]) == bord: up = [choice(range(32)), choice(range(20))]
        Xp, Yp = 10*up[0], 22 + 10*up[1]
        fill_rect(Xp,Yp+4,10,4,red_dark)
        fill_rect(Xp+2,Yp+2,6,8,red_dark)
        fill_rect(Xp+1,Yp+3,8,6,red)
        set_pixel(Xp+1,Yp+3,red_dark)
        set_pixel(Xp+1,Yp+8,red_dark)
        set_pixel(Xp+8,Yp+3,red_dark)
        set_pixel(Xp+8,Yp+8,red_dark)
        fill_rect(Xp+2,Yp,3,1,bord)
        fill_rect(Xp+1,Yp+1,5,1,bord)
        fill_rect(Xp+2,Yp+1,2,1,body)
        fill_rect(Xp+3,Yp+2,3,1,body)


    # Initialisation
    di, sn = 3, [30, 52, 80, 52] # Direction et corps (queue et tête) du serpent
    score = to_add = 0 # Score et croissance
    time = monotonic() # Temps
    if para[1]=="Facile": speed, add = 0.25, 5
    elif para[1]=="Moyen": speed, add = 0.2, 10
    elif para[1]=="Difficile": speed, add = 0.16, 15
    elif para[1]==" Extrême": speed, add = 0.12, 20

    # Dessin de l'interface
    fill_rect(0,0,320,222,back) # Nettoyage
    fill_rect(0,21,320,1,imp) # Bordure supérieure
    draw_string("SNAKE",135,2,imp) # Titre
    draw_string("0",304,2,sub) # Score
    fill_rect(30,52,60,10,bord) # Serpent initial
    fill_rect(31,53,58,8,body)
    if para[0] == "Classique": pom()

    # Boucle principale
    while True:
        # Gestion du temps et de la direction
        direction = di
        while monotonic() < time + speed:
            for k in range(4):
                if keydown(k) and direction+k != 3: di = k
            if keydown(6): start() # Retour au menu
        time = monotonic()


        # Rafraîchissement de la queue
        if int(to_add): to_add -= 1
        else:
            if get_pixel(sn[0],sn[1]+1) == body: sens = 0
            elif get_pixel(sn[0]+9,sn[1]+1) == body: sens = 3
            elif get_pixel(sn[0]+1,sn[1]) == body: sens = 1
            elif get_pixel(sn[0]+1,sn[1]+9) == body: sens = 2
            fill_rect(sn[0],sn[1],10,10,back)
            sn[0], sn[1] = (sn[0] + 10*(sens==3) - 10*(sens==0))%320, (sn[1] + 10*(sens==2) - 10*(sens==1)-22)%200+22
            if sens == 0: fill_rect(sn[0]+9,sn[1],1,10,bord)
            elif sens == 3: fill_rect(sn[0],sn[1],1,10,bord)
            elif sens == 1: fill_rect(sn[0],sn[1]+9,10,1,bord)
            elif sens == 2: fill_rect(sn[0],sn[1],10,1,bord)

        # Rafraîchissement de la tête - Partie 1
        fill_rect(sn[2]+1,sn[3]+1,8,8,body)
        if di == 0: fill_rect(sn[2],sn[3]+1,1,8,body)
        elif di == 1: fill_rect(sn[2]+1,sn[3],8,1,body)
        elif di == 3: fill_rect(sn[2]+9,sn[3]+1,1,8,body)
        elif di == 2: fill_rect(sn[2]+1,sn[3]+9,8,1,body)
        sn[2], sn[3] = sn[2] + 10*(di==3) - 10*(di==0), sn[3] + 10*(di==2) - 10*(di==1)
        if para[2]=="  Téléportation": sn[2], sn[3] = sn[2]%320, (sn[3]-22)%200 + 22

        # Traitement et power-ups
        if get_pixel(sn[2], sn[3]) == bord or not(sn[2] in range(320)) or not(sn[3] in range(22, 222)): break # Rencontre bordure mortelle ou corps
        if get_pixel(sn[2] + 4,sn[3] + 4) == red: # Pomme
            score += 15
            to_add += add
            pom()

        # Rafraîchissement de la tête - Partie 2
        fill_rect(sn[2],sn[3],10,10,bord)
        fill_rect(sn[2]+1,sn[3]+1,8,8,body)
        if di == 0:
            fill_rect(sn[2]+4,sn[3]+2,1,6,bord)
            fill_rect(sn[2]+3,sn[3]+3,1,4,red)
            fill_rect(sn[2]+3,sn[3]+4,2,2,body)
            fill_rect(sn[2]+9,sn[3]+1,1,8,body)
        elif di == 1:
            fill_rect(sn[2]+2,sn[3]+4,6,1,bord)
            fill_rect(sn[2]+3,sn[3]+3,4,1,red)
            fill_rect(sn[2]+4,sn[3]+3,2,2,body)
            fill_rect(sn[2]+1,sn[3]+9,8,1,body)
        elif di == 3:
            fill_rect(sn[2]+5,sn[3]+2,1,6,bord)
            fill_rect(sn[2]+6,sn[3]+3,1,4,red)
            fill_rect(sn[2]+5,sn[3]+4,2,2,body)
            fill_rect(sn[2],sn[3]+1,1,8,body)
        elif di == 2:
            fill_rect(sn[2]+2,sn[3]+5,6,1,bord)
            fill_rect(sn[2]+3,sn[3]+6,4,1,red)
            fill_rect(sn[2]+4,sn[3]+5,2,2,body)
            fill_rect(sn[2]+1,sn[3],8,1,body)

        # Traitement final
        score += speed
        draw_string("  "+str(int(score)),int(314-10*len("  "+str(int(score)))),2,sub) # Rafraichissement du score
        if para[0] == "Dingue":
            if speed > 0.04: speed *= 0.99
            to_add += 0.2


    # Procédure de perte
    draw_string("YOU LOST !",110,2,(255,0,0))
    while not(keydown(4)): pass
    play(para)

start()

""" # # #
Script alourdi pour peser *.42 ko car c'est la réponse à la gran
"""
