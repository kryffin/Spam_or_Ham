import sys
import re
import math

DICTIONNAIRE = "dictionnaire1000en.txt"
EPS = 1.	#epsilon utilisé pour régler l'apprentissage

def main (argv):
	if len(sys.argv) != 5:
		print("Utilisation du programme : ApprentissageFiltre.py mon_classifieur dossier_base_app nb_spam nb_ham")
		return

	#récupération des arguments
	fichierClassifieur = sys.argv[1]
	baseApps = sys.argv[2]
	nbSPAMapp = int(sys.argv[3])
	nbHAMapp = int(sys.argv[4])

	dictionnaire = charger_dictionnaire()

	P_Y_spam = nbSPAMapp / (nbSPAMapp + nbHAMapp)
	P_Y_ham = nbHAMapp / (nbSPAMapp + nbHAMapp)

	print("Apprentissage sur " + str(nbSPAMapp) + " SPAM et " + str(nbHAMapp) + " HAM...")
	b_spam = apprentissage(dictionnaire, nbSPAMapp, baseApps + "/spam/")
	b_ham = apprentissage(dictionnaire, nbHAMapp, baseApps + "/ham/")

	#enregistrement du classifieur
	sauvegardeClassifieur(fichierClassifieur, P_Y_spam, P_Y_ham, nbSPAMapp, nbHAMapp, EPS, b_spam, b_ham)

	print("Classifieur enregistré dans \'" + fichierClassifieur + ".cla\'.")

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

# apprentissage sur les fichiers SPAM
def apprentissage (dictionnaire, nbApp, dossier):
	b = [0.]*len(dictionnaire)
	for i in range(nbApp):
		occurences = lire_message(dictionnaire, dossier + str(i) + ".txt")
		for j in range(len(dictionnaire)):
			if occurences[j]:
				b[j] += 1.
		
	return b

#Sauvegarde du classifieur généré grâce à l'apprentissage
#les 2 premières lignes contiennent des probas, puis 2 lignes pour le nombre d'échantillons d'apprentissage
#1 ligne pour stocker l'epsilon, ensuite 2 lignes pour les tailles des tableaux b puis ces tableaux ligne par ligne
def sauvegardeClassifieur (fichierClassifieur, P_Y_spam, P_Y_ham, nbSPAMapp, nbHAMapp, eps, b_spam, b_ham):
	fichier = open(fichierClassifieur + ".cla", "w")
	fichier.write(str(P_Y_spam) + "\n")
	fichier.write(str(P_Y_ham) + "\n")
	fichier.write(str(nbSPAMapp) + "\n")
	fichier.write(str(nbHAMapp) + "\n")
	fichier.write(str(eps) + "\n")
	fichier.write(str(len(b_spam)) + "\n")
	fichier.write(str(len(b_ham)) + "\n")
	for b in range(len(b_spam)):
		fichier.write(str(b_spam[b]) + "\n")
	for b in range(len(b_ham)):
		fichier.write(str(b_ham[b]) + "\n")

#lance la fonction main du programme
if __name__ == "__main__":
	main(sys.argv[1:])
