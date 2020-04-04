import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class FiltreAntiSpam {

    private static int nbSPAMapp; //nb de spam pour l'apprentissage
    private static int nbHAMapp; //nb de ham pour l'apprentissage
    private static ArrayList<String> dictionnaire;
    private static int eps = 1;
    private static double[] b_spam;
    private static double[] b_ham;
    private static double P_Y_spam;
    private static double P_Y_ham;

    private static final String DOSSIER_SPAM = "res/baseapp/spam/";
    private static final String DOSSIER_HAM = "res/baseapp/ham/";
    private static final String DICTIONNAIRE = "res/dictionnaire1000en.txt";

    public static void main (String[] args) {
        if (args.length != 3) {
            System.out.println("Utilisation du programme : FiltreAntiSpam dossier_base_test nb_spam nb_ham");
            return;
        }

        //récupération des arguments
        String baseTests = args[0];
        int nbSPAMtest = Integer.parseInt(args[1]), nbHAMtest = Integer.parseInt(args[2]);
        System.out.println("Dossier de tests : " + baseTests + " sur " + nbSPAMtest + " SPAM et " + nbHAMtest + " HAM"); //DEBUG

        Scanner scan = new Scanner(System.in);

        System.out.print("Combien de SPAM dans la base d'apprentissage ? ");
        nbSPAMapp = scan.nextInt();
        System.out.print("Combien de HAM dans la base d'apprentissage ? ");
        nbHAMapp = scan.nextInt();

        System.out.println("\nChargement du dictionnaire...");
        dictionnaire = charger_dictionnaire(DICTIONNAIRE);

        System.out.println("\nApprentissage...");
        apprentissage();

        P_Y_spam = (double)nbSPAMapp / (double)(nbSPAMapp + nbHAMapp);
        P_Y_ham = (float)nbHAMapp / (float)(nbSPAMapp + nbHAMapp);

        System.out.println("Probas à priori :"); //DEBUG
        System.out.println("P(Y = SPAM) = " + P_Y_spam); //DEBUG
        System.out.println("P(Y = HAM) = " + P_Y_ham); //DEBUG

        //need calcul des probas à priori, qu'est ce que P(X = x) ?
    }

    private static ArrayList<String> charger_dictionnaire (String nomFichier) {
        if (nomFichier == null) return null;

        File fichier = new File(nomFichier); //dictionnaire à ouvrir

        ArrayList<String> dictionnaire = new ArrayList<>(); //dictionnaire à remplir

        try {
            //lecteur des lignes du fichier
            BufferedReader br = new BufferedReader(new FileReader(fichier));

            String ligne; //ligne lue

            //parcours de toutes les lignes du fichier
            while ((ligne = br.readLine()) != null) {
                //si le mot fait plus de 3 lettres on le sauvegarde (spécifié Section 5)
                if (ligne.length() >= 3) {
                    dictionnaire.add(ligne); //ajout du mot au dictionnaire
                }
            }

            return dictionnaire;
        } catch (IOException e) {
            e.printStackTrace();
        }

        return null; //il y a eu une erreur
    }

    private static HashMap<Integer, Integer> lire_message (ArrayList<String> dictionnaire, String nomFichier) {
        if (nomFichier == null) return null;

        File fichier = new File(nomFichier); //message à ouvrir

        HashMap<Integer, Integer> vecteurMots = new HashMap<>(); //vecteur de présence des mots
        for (int i = 0; i < dictionnaire.size(); i++) vecteurMots.put(i, 0);

        try {
            //lecteur des lignes du fichier
            BufferedReader br = new BufferedReader(new FileReader(fichier));

            String ligne;  //ligne lue
            String[] mots; //mots de la ligne

            //parcours de toutes les lignes du fichier
            while ((ligne = br.readLine()) != null) {
                mots = ligne.split(" ");
                for (String mot : mots) {
                    mot = mot.replaceAll("[^a-zA-Z]", ""); //suppression des caractères autre que les lettres
                    mot = mot.toUpperCase();
                    int index = dictionnaire.indexOf(mot);
                    if (index != -1 && vecteurMots.get(index) == 0) {
                        vecteurMots.put(index, 1);
                    }
                }
            }

            return vecteurMots;
        } catch (IOException e) {
            e.printStackTrace();
        }

        return null; //il y a eu une erreur
    }

    private static void apprentissage () {
        apprentissageSPAM();
        apprentissageHAM();
    }

    private static void apprentissageSPAM () {
        //parcours des m_spam et m_ham
        // b_spam^j = nb spam contenant mot j / nb spam
        b_spam = new double[dictionnaire.size()];

        for (int j = 0; j < nbSPAMapp; j++) {
            HashMap<Integer, Integer> occurences = lire_message(dictionnaire, DOSSIER_SPAM + j + ".txt");
            for (int i = 0; i < dictionnaire.size(); i++) {
                if (occurences.get(i) == 1) {
                    b_spam[i]++;
                }
            }
        }

        for (int i = 0; i < dictionnaire.size(); i++) {
            b_spam[i] = (b_spam[i] + eps) / (nbSPAMapp + (2 * eps));
        }
    }

    private static void apprentissageHAM () {
        //parcours des m_spam et m_ham
        // b_ham^j = nb ham contenant mot j / nb ham
        b_ham = new double[dictionnaire.size()];

        for (int j = 0; j < nbHAMapp; j++) {
            HashMap<Integer, Integer> occurences = lire_message(dictionnaire, DOSSIER_HAM + j + ".txt");
            for (int i = 0; i < dictionnaire.size(); i++) {
                if (occurences.get(i) == 1) {
                    b_ham[i]++;
                }
            }
        }

        for (int i = 0; i < dictionnaire.size(); i++) {
            b_ham[i] = (b_ham[i] + eps) / (nbHAMapp + (2 * eps));
        }
    }

}
