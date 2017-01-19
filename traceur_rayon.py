from __future__ import division

import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Dioptre(object):
    diametre = 24.5
    def __init__(self, z0, R, n_1, n_2,diametre=None):
        self.z0 = z0
        self.R = float(R)
        if diametre is not None:
            self.diametre = diametre
        self.n_1 = n_1
        self.n_2 = n_2
        self.z_center = z0 + R
        
    def __repr__(self):
        return """Dioptre 
        
                 position z0 = {0}
                 rayon R = {1})
                 centre = {2}""".format(self.z0, self.R, self.z_center)

    def translated(self,d):
        self.z0 = self.z0 + d
                 
    def equation(self, y):
        return self.z_center - np.sqrt(self.R**2 - y**2)*np.sign(self.R)
                 
    def plot(self):
        y = np.linspace(-self.diametre/2, self.diametre/2)
        plt.plot(self.equation(y), y)
        
    def intersection(self, rayon):
        k = rayon.k
        p0 = rayon.p0
        
        # Equation at^2+bt+c=0
        a = norm(k)**2
        p0_moins_z_center = p0 - np.array([0,0, self.z_center])
        b = 2*np.dot(k, p0_moins_z_center)        
        c = norm(p0_moins_z_center)**2 - self.R**2
        
        discriminant = b**2 - 4*a*c  
        if discriminant < 0:
            print "Intersection : pas de solution"          
        if self.R>0:
            t = (-b - np.sqrt(discriminant))/(2*a)
        else:
            t = (-b + np.sqrt(discriminant))/(2*a)            
        return rayon.p0 + t*k # array de taille 3
        
    def traversee(self, rayon):
        p2 = self.intersection(rayon)
        # Dessiner les vecteurs pour le voir
        n = p2 - np.array([0,0, self.z_center])
        n = n/norm(n)
        k_par = rayon.k - np.dot(rayon.k, n)*n
        n_2 = self.n_2
        alpha = np.sqrt(n_2**2 - norm(k_par)**2)
        # Le vecteur doit pointer à droite
        # (faire une dessin)
        if self.R>0:
            k2 = k_par - alpha*n
        else:
            k2 = k_par + alpha*n
        return Rayon(p2, k2)
      
      
class Rayon(object):
    def __init__(self, p0, k, n=None):
        self.p0= p0
        self.k = k
        if n is not None:
            self.normalize(n)

    def normalize(self, n):
        self.k = self.k / norm(self.k) * n

    def __repr__(self):
        return """Rayon
        
                  p0 = {0}
                  k = {1})""".format(self.p0, self.k)
                  
class Faisceau(list):
    def plot(self):               
        # Listes en compréhension pour récupérer 
        # les coordonnées des points de départ
        # des rayons du faisceau
        # (self est une liste) 
        X = [rayon.p0[2] for rayon in self]
        Y = [rayon.p0[1] for rayon in self]
        plt.plot(X, Y)
        
class SystemeOptique(list):
    def calcul_faisceau(self, r0):
        faisceau = Faisceau()
        faisceau.append(r0)
        r = r0
        for dioptre in self:
            r = dioptre.traversee(r)
            faisceau.append(r)
        return faisceau

    def plot(self):
        for dioptre in self:
            dioptre.plot()

    def translate_all(self, d):
        return SystemeOptique([dioptre.translated(d) for dioptre in self])
    
    
#    def translate_one(self, dioptre, d):
#         return 
#    def reverse(self):
#        return SystemeOptique([dioptre.reverse() for dioptre in self])
    
# Exemple d'utilisation
dioptre1 = Dioptre(0, 30.1, 1, 1.5168)
dioptre2 = Dioptre(6, -30.1, 1.5168, 1)
dioptre3 = Dioptre(20, 30.1, 1, 1.5168)
dioptre4 = Dioptre(30, -30.1, 1.5168, 1)

ecran = Dioptre(100, 1E6, 1, 1)


fig1 = plt.figure()
so1 = SystemeOptique([dioptre1, dioptre2, dioptre3, dioptre4, ecran])
so1.plot()
#so1 = SystemeOptique([dioptre1, dioptre2, dioptre3, dioptre4, ecran])
#so1 = so1.translate_all(20)
#so1.plot()

for d in np.linspace(-5, 5, 5):
        r0 = Rayon(p0=np.array([0,d,-10]), k=np.array([0,0,1]), n=1.0)
        so1.calcul_faisceau(r0).plot()
        plt.grid()



#
########################################################################
######################CODE INTERFACE GRAPHIQUE##########################
########################################################################
#
#
#def monplot():
#    """On trace le systeme optique et les rayons"""   
#    
#    fig = plt.figure()
#    so = SystemeOptique([dioptre1, dioptre2, dioptre3, dioptre4, ecran]) # on peut aussi ecrire SystemeOptique([...]).plot() avec l'instance plot de la classe.
#    so.plot()
#    
#    for d in np.linspace(-5, 5, 5):
#        r0 = Rayon(p0=np.array([0,d,-10]), k=np.array([0,0,1]), n=1.0)
#        so.calcul_faisceau(r0).plot()
#    plt.grid()
#    
#    return fig
#
#
#class mongui(Frame):
#    def __init__(self, parent):
#        
#        ##################  CREATION DE LA FENETRE PRINCIPALE ##############
#        Frame.__init__(self, parent)
#        self.parent = parent
#        parent.title("Modification des Dioptre")
#
#        ##################  CREATION DU GRAPH ##############
#        self.fig = monplot()
#        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
#        self.canvas.show()
#        self.canvas.get_tk_widget().pack()
#        self.pack(fill=BOTH, expand=1)
#        
#        ##################  CREATION DES BOUTONS ET PHRASES D'OPTIONS ##############
#        self.Phrase_intro = Label(parent, text="Vous pouvez creer, supprimer ou deplacer des Dioptres... ",width = 50, height = 4)
#        self.Phrase_intro.pack()
#        
#        self.Proposition_1 = Label(parent, text="Creer dioptre de la forme Dioptre'n'(place,rayon de courbure,indice avant,indice apres)", width = 100, height = 2)
#        self.Proposition_1.pack()
#        
#        self.var_texte_1 = StringVar()
#        self.Entree_1 = Entry(parent, textvariable=self.var_texte_1, width=30)
#        self.Entree_1.pack()
#        
#        self.bouton_valider_1 = Button(parent, text="Valider creation", command = self.creer)
#        self.bouton_valider_1.pack()  
#        
#        self.Proposition_2 = Label(parent, text="Supprimer", width = 20, height = 2)
#        self.Proposition_2.pack()
#        
#        self.liste = Listbox(parent, width = 20, height = 2)
#        self.liste.pack()
#        self.liste.insert(END,'dioptre1')
#        self.liste.insert(END,'dioptre2')
#        self.liste.insert(END,'dioptre3')
#        self.liste.insert(END,'dioptre4')
#    
#        self.bouton_valider_2 = Button(parent, text="Valider suppression")
#        self.bouton_valider_2.pack()         
#        
#        self.champ_proposition_3 = Label(parent, text="Deplacer", width = 20, height = 2)
#        self.champ_proposition_3.pack()
#        
#        self.var_texte_3 = StringVar()
#        self.Entree_3 = Entry(parent, textvariable=self.var_texte_3, width=30)
#        self.Entree_3.pack()
#        
#        self.var_texte_4 = StringVar()
#        self.Entree_4 = Entry(parent, textvariable=self.var_texte_4, width=30)
#        self.Entree_4.pack()        
#        
#        self.bouton_valider_3 = Button(parent, text="Valider déplacement")
#        self.bouton_valider_3.pack()
#        
#        self.bouton_quitter = Button(parent, text="Quitter", command=parent.quit)
#        self.bouton_quitter.pack(side = 'right')
#        
#        ##################  CREATION DES FONCTIONS ASSOCIEES AUX BOUTONS ##############
#
#    def creer(self):
#        print self.Entree_1.get()
##        self.liste_dioptres = []
##        liste_dioptres.append(self.Entree_1.get())
##        print liste_dioptres
##    def suppr(self):
##        
##        
##    def deplacer(self):
#    
#
#
#root = Tk()
#app = mongui(root)
#root.mainloop()



