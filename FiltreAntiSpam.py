import sys
import re
import math

DICTIONNAIRE = "dictionnaire1000en.txt"

def main (argv):
	if len(sys.argv) != 3:
		print("Utilisation du programme : FiltreAntiSpam.py mon_classifieur.cla message.txt")
		return

	#récupération des arguments
	fichierClassifieur = sys.argv[1]
	fichierMessage = sys.argv[2]

	dictionnaire = charger_dictionnaire()

	classifieur = chargementClassifieur(fichierClassifieur)

	P_Y_spam = classifieur[0]
	P_Y_ham = classifieur[1]

	#conversion des b de string à float
	b_spam = [float(b) for b in classifieur[2]]
	b_ham = [float(b) for b in classifieur[3]]

	print("Test du message " + fichierMessage + "...")

	#test du message
	probaSPAM = probaPosteriori(fichierMessage, b_spam, P_Y_spam, dictionnaire)
	probaHAM = probaPosteriori(fichierMessage, b_ham, P_Y_ham, dictionnaire)
	P_X = math.exp(probaSPAM) + math.exp(probaHAM)
	if (P_X == 0.):
		probaSPAM = 0.
		probaHAM = 0.
	else:
		probaSPAM = 1. / P_X * math.exp(probaSPAM)
		probaHAM = 1 / P_X * math.exp(probaHAM)
	print(fichierMessage + " : P(Y = SPAM | X = x) =", probaSPAM, ", P(Y = HAM | X = x) =", probaHAM)
	if probaSPAM > probaHAM:
		print("D'après " + fichierClassifieur + ", le message " + fichierMessage + " est un SPAM !")
	else:
		print("D'après " + fichierClassifieur + ", le message " + fichierMessage + " est un HAM !")

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

#lisse les données brutes du classifieur
def lissage (b, nbApp, eps):
	b_lisse = [0.]*len(b)
	for i in range(len(b)):
		b_lisse[i] = (float(b[i]) + eps) / (nbApp + (2*eps))
	return b_lisse

#Chargement du classifieur passé en argument du programme
#returne une liste de la forme : [P(Y = SPAM), P(Y = HAM), nbSPAMapp, nbHAMapp, epsilon, b_spam[], b_ham[]]
def chargementClassifieur (fichierClassifieur):
	classifieur = []
	fichier = open(fichierClassifieur, "r")
	contenu = fichier.read().split()
	classifieur.append(float(contenu[0])) #P_Y_spam
	classifieur.append(float(contenu[1])) #P_Y_ham
	nbSPAMapp = int(contenu[2]) #nbSPAMapp
	nbHAMapp = int(contenu[3]) #nbHAMapp
	epsilon = float(contenu[4]) #epsilon
	tailleBSpam = int(contenu[5]) #len(b_spam)
	tailleBHam = int(contenu[6]) #len(b_spam)
	classifieur.append(lissage(contenu[7:tailleBSpam+7], nbSPAMapp, epsilon)) #b_spam
	classifieur.append(lissage(contenu[tailleBSpam+7:tailleBSpam+tailleBHam+7], nbHAMapp, epsilon)) #b_ham
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
