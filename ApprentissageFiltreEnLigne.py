import sys
import re
import math

DICTIONNAIRE = "dictionnaire1000en.txt"

def main (argv):
	if len(sys.argv) != 4:
		print("Utilisation du programme : ApprentissageFiltreEnLigne.py mon_classifieur.cla message.txt SPAM|HAM")
		return

	#récupération des arguments
	fichierClassifieur = sys.argv[1]
	fichierMessage = sys.argv[2]
	if sys.argv[3].upper() == "SPAM":
		isSPAM = True
	elif sys.argv[3].upper() == "HAM":
		isSPAM = False
	else:
		print(sys.argv[3], "n'est pas un argument valide, veuillez choisir \'SPAM\' ou \'HAM\'")
		return

	dictionnaire = charger_dictionnaire()

	classifieur = chargementClassifieurBrut(fichierClassifieur)

	P_Y_spam = classifieur[0]
	P_Y_ham = classifieur[1]

	nbSPAMapp = classifieur[2]
	nbHAMapp = classifieur[3]

	epsilon = classifieur[4]

	#conversion des b de string à float
	b_spam = [float(b) for b in classifieur[5]]
	b_ham = [float(b) for b in classifieur[6]]

	if isSPAM:
		print("Modification du filtre \'" + fichierClassifieur + "\' par apprentissage sur le SPAM \'" + fichierMessage + "\'...")
		b_spam = apprentissageFichier(b_spam, dictionnaire, fichierMessage)
		nbSPAMapp = nbSPAMapp + 1
	else:
		print("Modification du filtre \'" + fichierClassifieur + "\' par apprentissage sur le HAM \'" + fichierMessage + "\'...")
		b_ham = apprentissageFichier(b_ham, dictionnaire, fichierMessage)
		nbHAMapp = nbHAMapp + 1

	#enregistrement du classifieur
	sauvegardeClassifieur(fichierClassifieur, P_Y_spam, P_Y_ham, nbSPAMapp, nbHAMapp, epsilon, b_spam, b_ham)

	print("Classifieur \'" + fichierClassifieur + "\' mis à jour.")

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
#returne une liste de la forme : [P(Y = SPAM), P(Y = HAM), nbSPAMapp, nbHAMapp, epsilon, b_spam[], b_ham[]]
def chargementClassifieurBrut (fichierClassifieur):
	classifieur = []
	fichier = open(fichierClassifieur, "r")
	contenu = fichier.read().split()
	classifieur.append(float(contenu[0])) #P_Y_spam
	classifieur.append(float(contenu[1])) #P_Y_ham
	classifieur.append(int(contenu[2])) #nbSPAMapp
	classifieur.append(int(contenu[3])) #nbHAMapp
	classifieur.append(float(contenu[4])) #epsilon
	tailleBSpam = int(contenu[5]) #len(b_spam)
	tailleBHam = int(contenu[6]) #len(b_spam)
	classifieur.append(contenu[7:tailleBSpam+7]) #b_spam
	classifieur.append(contenu[tailleBSpam+7:tailleBSpam+tailleBHam+7]) #b_ham
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

# apprentissage sur les fichiers SPAM
def apprentissageFichier (b, dictionnaire, fichier):
	occurences = lire_message(dictionnaire, fichier)
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
