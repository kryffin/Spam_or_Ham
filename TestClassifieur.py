import sys
import re
import math
import numpy as np

DICTIONNAIRE = "dictionnaire1000en.txt"

def main (argv):
	if len(sys.argv) != 5:
		print("Utilisation du programme : TestClassifieur.py mon_classifieur.cla dossier_base_test nb_spam nb_ham")
		return

	#récupération des arguments
	fichierClassifieur = sys.argv[1]
	baseTests = sys.argv[2]
	nbSPAMtest = int(sys.argv[3])
	nbHAMtest = int(sys.argv[4])
	print("Test du classifieur", fichierClassifieur, "avec le dossier de test :", baseTests, "sur", nbSPAMtest, "SPAM et", nbHAMtest, "HAM")

	print("Chargement du dictionnaire...")
	dictionnaire = charger_dictionnaire()

	print("Chargement du classifieur...")
	classifieur = chargementClassifieur(fichierClassifieur)

	P_Y_spam = classifieur[0]
	P_Y_ham = classifieur[1]

	#conversion des b de string à float
	b_spam = [float(b) for b in classifieur[2]]
	b_ham = [float(b) for b in classifieur[3]]

	print("P(Y = SPAM) =", P_Y_spam)
	print("P(Y = HAM) =", P_Y_ham)

	print("Test :")

	err_spam = 0.
	for i in range(nbSPAMtest):
		probaSPAM = probaPosteriori(baseTests + "/spam/" + str(i) + ".txt", b_spam, P_Y_spam, dictionnaire)
		probaHAM = probaPosteriori(baseTests + "/spam/" + str(i) + ".txt", b_ham, P_Y_ham, dictionnaire)
		P_X = math.exp(probaSPAM) + math.exp(probaHAM)
		if (P_X == 0.):
			probaSPAM = 0.
			probaHAM = 0.
		else:
			probaSPAM = np.float64(1. / P_X * math.exp(probaSPAM))
			probaHAM = np.float64(1 / P_X * math.exp(probaHAM))
		print("\nSPAM numéro", i, " : P(Y = SPAM | X = x) =", probaSPAM, ", P(Y = HAM | X = x) =", probaHAM)
		if probaSPAM > probaHAM:
			print("\t=> identifié comme un SPAM")
		else:
			print("\t=> identifié comme un HAM ***erreur***")
			err_spam = err_spam + 1.
	err_spam = err_spam / nbSPAMtest

	err_ham = 0.
	for i in range(nbHAMtest):
		probaSPAM = probaPosteriori(baseTests + "/ham/" + str(i) + ".txt", b_spam, P_Y_spam, dictionnaire)
		probaHAM = probaPosteriori(baseTests + "/ham/" + str(i) + ".txt", b_ham, P_Y_ham, dictionnaire)
		P_X = math.exp(probaSPAM) + math.exp(probaHAM)
		if (P_X == 0.):
			probaSPAM = 0.
			probaHAM = 0.
		else:
			probaSPAM = np.float64(1. / P_X * math.exp(probaSPAM))
			probaHAM = np.float64(1. / P_X * math.exp(probaHAM))
		print("\nHAM numéro", i, " : P(Y = SPAM | X = x) =", probaSPAM, ", P(Y = HAM | X = x) =", probaHAM)
		if probaSPAM > probaHAM:
			print("\t=> identifié comme un SPAM ***erreur***")
			err_ham = err_ham + 1.
		else:
			print("\t=> identifié comme un HAM")
	err_ham = err_ham / nbHAMtest

	print("\nErreur de test sur les", nbSPAMtest, "SPAM\t\t:", err_spam*100, "%")
	print("Erreur de test sur les", nbHAMtest, "HAM\t\t:", err_ham*100, "%")
	print("Erreur de test global sur", (nbSPAMtest + nbHAMtest), "mails\t:", ((err_spam + err_ham) / 2)*100, "%")

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
