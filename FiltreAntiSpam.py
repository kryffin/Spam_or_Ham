import sys
import re
import math

DOSSIER_SPAM = "baseapp/spam/"
DOSSIER_HAM = "baseapp/ham/"
DICTIONNAIRE = "dictionnaire1000en.txt"
EPS = 1.	#epsilon utilisé pour régler l'apprentissage

def main (argv):
	if len(sys.argv) != 4:
		print("Utilisation du programme : FiltreAntiSpam dossier_base_test nb_spam nb_ham")
		return

	#récupération des arguments
	baseTests = sys.argv[1]
	nbSPAMtest = int(sys.argv[2])
	nbHAMtest = int(sys.argv[3])
	print("Dossier de tests :", baseTests, "sur", nbSPAMtest, "SPAM et", nbHAMtest, "HAM")

	#input utilisateur pour déterminer la taille des bases d'apprentissage
	print("Combien de SPAM dans la base d'apprentissage ? ")
	nbSPAMapp = int(input())
	print("Combien de HAM dans la base d'apprentissage ? ")
	nbHAMapp = int(input())

	print("Chargement du dictionnaire...")
	dictionnaire = charger_dictionnaire()

	print("Taille du dictionnaire :", len(dictionnaire))

	P_Y_spam = nbSPAMapp / (nbSPAMapp + nbHAMapp)
	P_Y_ham = nbHAMapp / (nbSPAMapp + nbHAMapp)

	print("P(Y = SPAM) =", P_Y_spam)
	print("P(Y = HAM) =", P_Y_ham)

	print("Apprentissage...")
	b_spam = apprentissageSPAM(dictionnaire, nbSPAMapp)
	b_ham = apprentissageHAM(dictionnaire, nbHAMapp)

	print("Test :")

	err_spam = 0.
	for i in range(nbSPAMtest):
		probaSPAM = probaPosteriori(baseTests + "/spam/" + str(i) + ".txt", b_spam, P_Y_spam, dictionnaire)
		probaHAM = probaPosteriori(baseTests + "/spam/" + str(i) + ".txt", b_ham, P_Y_ham, dictionnaire)
		if probaSPAM > probaHAM:
			print("SPAM numéro", i, "identifié comme un SPAM")
		else:
			print("SPAM numéro", i, "identifié comme un HAM ***erreur***")
			err_spam = err_spam + 1.
	err_spam = err_spam / nbSPAMtest

	err_ham = 0.
	for i in range(nbHAMtest):
		probaSPAM = probaPosteriori(baseTests + "/ham/" + str(i) + ".txt", b_spam, P_Y_spam, dictionnaire)
		probaHAM = probaPosteriori(baseTests + "/ham/" + str(i) + ".txt", b_ham, P_Y_ham, dictionnaire)
		if probaSPAM > probaHAM:
			print("HAM numéro", i, "identifié comme un SPAM ***erreur***")
			err_ham = err_ham + 1.
		else:
			print("HAM numéro", i, "identifié comme un HAM")
	err_ham = err_ham / nbHAMtest

	print("Erreur de test sur les", nbSPAMtest, "SPAM\t\t:", err_spam*100, "%")
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
def apprentissageSPAM (dictionnaire, nbApp):
	b_spam = [0.]*len(dictionnaire)
	for i in range(nbApp):
		occurences = lire_message(dictionnaire, DOSSIER_SPAM + str(i) + ".txt")
		for j in range(len(dictionnaire)):
			if occurences[j]:
				b_spam[j] += 1.

	for i in range(len(dictionnaire)):
		b_spam[i] = (b_spam[i] + EPS) / (nbApp + (2*EPS))
		
	return b_spam

# apprentissage sur les fichiers SPAM
def apprentissageHAM (dictionnaire, nbApp):
	b_ham = [0.]*len(dictionnaire)
	for i in range(nbApp):
		occurences = lire_message(dictionnaire, DOSSIER_HAM + str(i) + ".txt")
		for j in range(len(dictionnaire)):
			if occurences[j]:
				b_ham[j] += 1.

	for i in range(len(dictionnaire)):
		b_ham[i] = (b_ham[i] + EPS) / (nbApp + (2*EPS))

	return b_ham

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
