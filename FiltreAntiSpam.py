import sys
import re
import math
import numpy as np

DOSSIER_SPAM = "baseapp/spam/"
DOSSIER_HAM = "baseapp/ham/"
DICTIONNAIRE = "dictionnaire1000en.txt"
EPS = 1.	#epsilon utilisé pour régler l'apprentissage

def main (argv):
	if len(sys.argv) != 3:
		print("Utilisation du programme : FiltreAntiSpam.py mon_classifieur.cla message.txt")
		return

	#récupération des arguments
	fichierClassifieur = sys.argv[1]
	fichierMessage = sys.argv[2]
	print("Test du message", fichierMessage, "avec le classifieur", fichierClassifieur)

	print("Chargement du dictionnaire...")
	dictionnaire = charger_dictionnaire()

	print("Chargement du classifieur...")
	classifieur = chargementClassifieur(fichierClassifieur)

	P_Y_spam = classifieur[0]
	P_Y_ham = classifieur[1]

	#conversion des b de string à float
	b_spam = [float(b) for b in classifieur[2]]
	b_ham = [float(b) for b in classifieur[3]]

	#test du message
	probaSPAM = probaPosteriori(fichierMessage, b_spam, P_Y_spam, dictionnaire)
	probaHAM = probaPosteriori(fichierMessage, b_ham, P_Y_ham, dictionnaire)
	P_X = math.exp(probaSPAM) + math.exp(probaHAM)
	if (P_X == 0.):
		probaSPAM = 0.
		probaHAM = 0.
	else:
		probaSPAM = np.float64(1. / P_X * math.exp(probaSPAM))
		probaHAM = np.float64(1 / P_X * math.exp(probaHAM))
	if probaSPAM > probaHAM:
		print("D'après", fichierClassifieur, ", le message", fichierMessage, "est un SPAM !")
	else:
		print("D'après", fichierClassifieur, ", le message", fichierMessage, "est un HAM !")

# charge le dictionnaire situé dans DICTIONNAIRE dans une liste de mots
def charger_dictionnaire ():
	f = open(DICTIONNAIRE, "r")
	dictionnaire = []
	line = f.readlines()
	for l in line:
		l = l.rstrip()
		if len(l) >= 3:
			dictionnaire.append(str(l))

	return dictionnaire

#Chargement du classifieur passé en argument du programme
#returne une liste de la forme : [P(Y = SPAM), P(Y = HAM), b_spam[], b_ham[]]
def chargementClassifieur (fichierClassifieur):
	classifieur = []
	fichier = open(fichierClassifieur, "r")
	contenu = fichier.read().split()
	classifieur.append(float(contenu[0])) #P_Y_spam
	classifieur.append(float(contenu[1])) #P_Y_ham
	tailleBSpam = int(contenu[2]) #len(b_spam)
	tailleBHam = int(contenu[3]) #len(b_spam)
	classifieur.append(contenu[4:tailleBSpam+4]) #b_spam
	classifieur.append(contenu[tailleBSpam+4:tailleBSpam+tailleBHam+4]) #b_ham
	return classifieur

# lit un message spécifié par fichier, renvoie une liste ordonnée dans
# l'ordre des mots du dictionnaire si le mot est présent ou non (True / False)
def lire_message (dictionnaire, fichier):
	f = open(fichier, "r", errors="replace")
	mots = [False]*len(dictionnaire)
	line = f.readlines()
	for l in line:
		l = l.rstrip()
		words = l.split()
		for w in words:
			w = re.sub("[^a-zA-Z]", "", w)
			w = w.upper()
			if w in dictionnaire:
				mots[dictionnaire.index(w)] = True

	return mots

# calcul de la probabilité à posteriori
def probaPosteriori (fichier, b, P, dictionnaire):
	P_X_x_Y = 0.
	occurences = lire_message(dictionnaire, fichier)
	for j in range(len(dictionnaire)):
		if occurences[j]:
			P_X_x_Y = P_X_x_Y + math.log(b[j])
		else:
			P_X_x_Y = P_X_x_Y + math.log(1. - b[j])

	return P_X_x_Y + math.log(P)

#lance la fonction main du programme
if __name__ == "__main__":
	main(sys.argv[1:])
