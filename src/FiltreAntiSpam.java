import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;

public class FiltreAntiSpam {

    private static final String DICTIONNAIRE = "res/dictionnaire1000en.txt";

    public static void main (String[] args) {
        if (args.length != 3) {
            System.out.println("Utilisation du programme : FiltreAntiSpam dossier_base_test nb_spam nb_ham");
            return;
        }

        //récupération des arguments
        String baseTests = args[0];
        int nbSPAM = Integer.parseInt(args[1]), nbHAM = Integer.parseInt(args[2]);
        System.out.println("Dossier de tests : " + baseTests + " sur " + nbSPAM + " SPAM et " + nbHAM + " HAM"); //DEBUG

        ArrayList<String> dictionnaire = charger_dictionnaire(DICTIONNAIRE);
        System.out.println("Le dico contient " + dictionnaire.size() + " mots"); //DEBUG

        HashMap<Integer, Integer> vecteurMots = lire_message(dictionnaire, "res/basetest/spam/0.txt");
        int res = 0;
        for (Integer i : vecteurMots.values()) if(i == 1) res+=1;
        System.out.println("Vecteur de mots de taille : " + vecteurMots.size() + " avec " + res + " mots du dico présents");
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

}
