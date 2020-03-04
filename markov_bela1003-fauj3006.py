###
###  Gabarit pour l'application de traitement des frequences de mots dans les oeuvres d'auteurs divers
###  Le traitement des arguments a ete inclus:
###     Tous les arguments requis sont presents et accessibles dans args
###     Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments
###
###  Frederic Mailhot, 26 fevrier 2018
###    Revise 16 avril 2018
###    Revise 7 janvier 2020

###  Parametres utilises, leur fonction et code a generer
###
###  -d   Deja traite dans le gabarit:  la variable rep_auth contiendra le chemin complet vers le repertoire d'auteurs
###       La liste d'auteurs est extraite de ce repertoire, et est comprise dans la variable authors
###
###  -P   Si utilise, indique au systeme d'utiliser la ponctuation.  Ce qui est considÃ©re comme un signe de ponctuation
###       est defini dans la liste PONC
###       Si -P EST utilise, cela indique qu'on dÃ©sire conserver la ponctuation (chaque signe est alors considere
###       comme un mot.  Par defaut, la ponctuation devrait etre retiree
###
###  -m   mode d'analyse:  -m 1 indique de faire les calculs avec des unigrammes, -m 2 avec des bigrammes.
###
###  -a   Auteur (unique a traiter).  Utile en combinaison avec -g, -G, pour la generation d'un texte aleatoire
###       avec les caracteristiques de l'auteur indique
###
###  -G   Indique qu'on veut generer un texte (voir -a ci-haut), le nombre de mots Ã  generer doit Ãªtre indique
###
###  -g   Indique qu'on veut generer un texte (voir -a ci-haut), le nom du fichier en sortie est indique
###
###  -F   Indique qu'on desire connaitre le rang d'un certain mot pour un certain auteur.  L'auteur doit etre
###       donnÃ© avec le parametre -a, et un mot doit suivre -F:   par exemple:   -a Verne -F Cyrus
###
###  -v   Deja traite dans le gabarit:  mode "verbose",  va imprimer les valeurs donnÃ©es en parametre
###
###
###  Le systeme doit toujours traiter l'ensemble des oeuvres de l'ensemble des auteurs.  Selon la presence et la valeur
###  des autres parametres, le systeme produira differentes sorties:
###
###  avec -a, -g, -G:  generation d'un texte aleatoire avec les caracteristiques de l'auteur identifie
###  avec -a, -F:  imprimer la frequence d'un mot d'un certain auteur.  Format de sortie:  "auteur:  mot  frequence"
###                la frequence doit Ãªtre un nombre reel entre 0 et 1, qui represente la probabilite de ce mot
###                pour cet auteur
###  avec -f:  indiquer l'auteur le plus probable du texte identifie par le nom de fichier qui suit -f
###            Format de sortie:  "nom du fichier: auteur"
###  avec ou sans -P:  indique que les calculs doivent etre faits avec ou sans ponctuation
###  avec -v:  mode verbose, imprimera l'ensemble des valeurs des paramÃ¨tres (fait deja partie du gabarit)


import math
import argparse
import glob
import sys
import os
from pathlib import Path
from random import randint
from random import choice
import time
from operator import itemgetter

### Ajouter ici les signes de ponctuation Ã  retirer
from typing import List, Any, Union

PONC = ["!", '"', "'", ")", "(", ",", ".", ";", ":", "?", "-", "_", "*", '\n']


###  Vous devriez inclure vos classes et mÃ©thodes ici, qui seront appellÃ©es Ã  partir du main
def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the mid of the array
        L = arr[:mid]  # Dividing the array elements
        R = arr[mid:]  # into 2 halves

        mergeSort(L)  # Sorting the first half
        mergeSort(R)  # Sorting the second half

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] > R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


class Text:
    def __init__(self):
        self.Sorted = dict()

    def __TextToWordsList__(self, author):
        self.word = []
        for text in author.__getListText__():
            path = "..\\bela1003-fauj3006\\TextesPourEtudiants\\" + author.__getname__() + "\\" + text
        self.__openText__(path)
        return self.word

    def __backToDic__(self, arr, bucket_count, nb):
        cpt = 0
        for instance in arr:
            for key in bucket_count.keys():
                if bucket_count.get(key) == instance:
                    if nb == cpt:
                        return self.Sorted
                    cpt += 1
                    self.Sorted[key] = instance
                    break

    def __openText__(self, path):
        file = open(path, "r", encoding="utf-8")
        allLine = str()
        for line in file:
            allLine += ' ' + line.lower()
        for c in PONC:
            allLine = allLine.replace(c, '')
        word1 = allLine.split(' ')
        self.word += word1
        file.close()
        del word1
        del allLine

    def __Proximite__(self,path,d1):
        self.commonWordList = list()
        self.word = []
        self.__openText__(path)
        u = UniGramme(self.word)
        d2 = u.__createDic__()
        commonkeys = list(set(d1.keys() & d2.keys()))
        Result = 0
        for keys in commonkeys:
            NormalisedFreq = math.sqrt(math.pow((len(d1.get(keys))/len(d1.keys()))-(len(d2.get(keys))/len(d2.keys())), 2))
            Result += NormalisedFreq
        return Result

    def __Proximite2__(self,basepath,path,authorlist):
        resultList = []
        for authors in authorlist:
            a = Auteur(basepath,authors)
            self.word = []
            for text in a.__getListText__():
                self.__openText__(basepath+'\\'+a.__getname__()+'\\'+ text)
            u = UniGramme(self.word)
            d = u.__createDic__()
            result = self.__Proximite__(path,d)
            resultList.append(result)
            resultList.append(a.__getname__())
        return resultList


class UniGramme:
    def __init__(self, word):
        self.word = word

    def __createDic__(self):
        self.d = {}
        for word1 in self.word:
            if len(word1) > 2:
                self.__addBucket__(word1)
        return self.d

    def __addBucket__(self, bucket):
        if bucket in self.d:
            self.d[bucket].append(bucket)
        else:
            self.d[bucket] = [bucket]

    def __BucketLength__(self, dictionary):
        self.ListLength = {}
        for bucket in dictionary:
            cpt = 0
            for b in self.d.get(bucket):
                cpt += 1
            self.ListLength[bucket] = cpt
        return self.ListLength


class BiGramme:
    def __init__(self, word):
        self.word = word

    def __createDic__(self):
        self.d = {}
        for word1 in self.word:
            if len(word1) > 2:
                if self.lastWord != '':
                    self.__addBucket__(word1, self.lastWord)
            self.lastWord = word1
        return self.d

    def __addBucket__(self, word1, word2):
        bucket = str()
        bucket = word1 + ' ' + word2
        if bucket in self.d:
            self.d[bucket].append(bucket)
        else:
            self.d[bucket] = [bucket]

    def __BucketLength__(self, dictionary):
        self.ListLength = {}
        for bucket in dictionary:
            cpt = 0
            for b in self.d.get(bucket):
                cpt += 1
            self.ListLength[bucket] = cpt
        return self.ListLength


class Auteur:

    def __init__(self, path, name):
        self.listText = []
        directory = path + '\\' + name
        self.nom = name
        for entry in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, entry)):
                self.listText.append(entry)

    def __getListText__(self):
        return self.listText

    def __getname__(self):
        return self.nom


### Main: lecture des paramÃ¨tres et appel des mÃ©thodes appropriÃ©es
###
###       argparse permet de lire les paramÃ¨tres sur la ligne de commande
###             Certains paramÃ¨tres sont obligatoires ("required=True")
###             Ces paramÃ¨tres doivent Ãªtres fournis Ã  python lorsque l'application est exÃ©cutÃ©e
if __name__ == "__main__":
    start_time = time.time()
    parser = argparse.ArgumentParser(prog='markov_bela1003-fauj3006.py')
    parser.add_argument('-d', required=True, help='Repertoire contenant les sous-repertoires des auteurs')
    parser.add_argument('-a', help='Auteur a traiter')
    parser.add_argument('-f', help='Fichier inconnu a comparer')
    parser.add_argument('-m', required=True, type=int, choices=range(1, 3),
                        help='Mode (1 ou 2) - unigrammes ou digrammes')
    parser.add_argument('-F', type=int, help='Indication du rang (en frequence) du mot (ou bigramme) a imprimer')
    parser.add_argument('-G', type=int, help='Taille du texte a generer')
    parser.add_argument('-g', help='Nom de base du fichier de texte a generer')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    parser.add_argument('-P', action='store_true', help='Retirer la ponctuation')
    parser.add_argument('-A', action='store_true', help='Analyse sur tout les auteur')
    args = parser.parse_args()

    ### Lecture du rÃ©pertoire des auteurs, obtenir la liste des auteurs
    ### Note:  args.d est obligatoire
    ### auteurs devrait comprendre la liste des rÃ©pertoires d'auteurs, peu importe le systÃ¨me d'exploitation
    cwd = os.getcwd()
    if os.path.isabs(args.d):
        rep_aut = args.d
    else:
        rep_aut = os.path.join(cwd, args.d)

    rep_aut = os.path.normpath(rep_aut)
    authors = os.listdir(rep_aut)

    ### Enlever les signes de ponctuation (ou non) - DÃ©finis dans la liste PONC
    if args.P:
        remove_ponc = True
    else:
        remove_ponc = False

    ### Si mode verbose, reflÃ©ter les valeurs des paramÃ¨tres passÃ©s sur la ligne de commande
    if args.v:
        print("Mode verbose:")
        print("Calcul avec les auteurs du repertoire: " + args.d)
        if args.f:
            print("Fichier inconnu a,"
                  " etudier: " + args.f)

        print("Calcul avec des " + str(args.m) + "-grammes")
        if args.F:
            print(str(args.F) + "e mot (ou digramme) le plus frequent sera calcule")

        if args.a:
            print("Auteur etudie: " + args.a)

        if args.P:
            print("Retirer les signes de ponctuation suivants: {0}".format(" ".join(str(i) for i in PONC)))

        if args.G:
            print("Generation d'un texte de " + str(args.G) + " mots")

        if args.g:
            print("Nom de base du fichier de texte genere: " + args.g)

        print("Repertoire des auteurs: " + rep_aut)
        print("Liste des auteurs: ")
        for a in authors:
            aut = a.split("/")
            print("    " + aut[-1])

### Ã€ partir d'ici, vous devriez inclure les appels Ã  votre code
authorsList = ['Balzac', 'Hugo', 'Ségur', 'Verne', 'Voltaire', 'Zola']
text = Text()
if not args.A or not args.a:
    auteur = Auteur(args.d, args.a)
    WordsList = text.__TextToWordsList__(auteur)
    if args.m == 1:
        unig = UniGramme(WordsList)
        d = unig.__createDic__()
        if args.f:
            print(args.a, " à une proximité de :", text.__Proximite__(args.f, d), " avec le text Emile Zola - Germinal.txt")
    if args.m == 2:
        big = BiGramme(WordsList)
        d = big.__createDic__()
    if args.F:
        if args.m == 1:
            toBeSorted = unig.__BucketLength__(d)
        else:
            toBeSorted = big.__BucketLength__(d)
        instances = list(toBeSorted.values())
        mergeSort(instances)
        WordsInOrder = text.__backToDic__(instances, toBeSorted,args.F)
        print(WordsInOrder)

# -A -f ..\bela1003-fauj3006\TextesPourEtudiants\Ségur\ComtessedeSégur-FrançoisleBossu.txt
if args.A:
    if args.f:
        resultList = text.__Proximite2__(args.d, args.f, authorsList)
        for i in range(0, len(resultList), 2):
            print(resultList[i + 1], " : ", resultList[i])

print("time it took to execute all: %.2f" % (time.time() - start_time))
