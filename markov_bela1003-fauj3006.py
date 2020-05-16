
import math
import argparse
import glob
import sys
import os
from pathlib import Path
from random import randint
from random import choice
import time

### Ajouter ici les signes de ponctuation Ã  retirer
from typing import List, Any, Union

PONC = ["!", '"', "'", ")", "(", ",", ".", ";", ":", "?", "-", "_", "*", "[", "]"]


###  Vous devriez inclure vos classes et mÃ©thodes ici, qui seront appellÃ©es Ã  partir du main
def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        mergeSort(L)
        mergeSort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] > R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


class Text:
    def __init__(self, path, name):
        self.listText = []
        directory = path + '\\' + name
        self.name = name
        self.nbpunc = 0
        for entry in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, entry)):
                self.listText.append(entry)

    def __TextToWordsList__(self, punc,rootdirectory):
        self.word = []
        for text in self.listText:
            path = rootdirectory + "\\" + self.name + "\\" + text
            self.__openText__(path, punc)
        return self.word

    def __backToDic__(self, arr, bucket_count, nb):
        cpt = 0
        Sorted = dict()
        for instance in arr:
            alreadyfound = False
            for key in bucket_count.keys():
                if bucket_count.get(key) == instance:
                    if nb == cpt:
                        return Sorted
                    if not alreadyfound:
                        if not Sorted.get(key):
                            cpt += 1
                            alreadyfound = True
                            Sorted[key] = instance
                            break

    def __openText__(self, path, punc):
        file = open(path, "r", encoding="utf-8")
        allLine = file.read().lower()
        self.punctuation = list()
        allLine = allLine.replace('\n', ' ')
        if not punc:
            for c in PONC:
                allLine = allLine.replace(c, ' ')
        else:
            for caract in allLine:
                for c in PONC:
                    if c == caract:
                        self.punctuation.append(caract)
            for c in PONC:
                allLine = allLine.replace(c, ' ')
        word1 = allLine.split(' ')
        self.word += word1
        self.nbpunc = len(self.punctuation)/(len(self.word + self.punctuation))*100
        file.close()
        del word1
        del allLine

    def __Proximite__(self, path, d1, punc):
        self.commonWordList = list()
        self.word = []
        self.__openText__(path, punc)
        u = UniGramme(self.word)
        d2 = u.__createDic__()
        commonkeys = list(set(d1.keys() & d2.keys()))
        Result = 0
        count = 0
        for keys in commonkeys:
            count += len(d1.get(keys)) + len(d2.get(keys))
        for keys in commonkeys:
            NormalisedFreq = math.pow((len(d1.get(keys)) / count) - (len(d2.get(keys)) / count), 2)
            Result += NormalisedFreq
        Result = math.sqrt(Result)
        return Result

    def __Proximite2__(self, basepath, path, punc):
        resultList = []
        result = 0
        for text in self.listText:
            self.word = []
            self.__openText__(basepath + '\\' + self.name + '\\' + text, punc)
            u = UniGramme(self.word)
            d = u.__createDic__()
            result += self.__Proximite__(path, d, punc)
        resultList.append(result / len(self.listText))
        resultList.append(self.name)
        return resultList

    def __Generation__(self, output, dictionary, nb_word, mode):
        file = open(output, "a", encoding="utf-8")
        file.write(self.name + " ::Debut\n")
        if mode == 1:
            self.listForGeneration = list()
            for word in dictionary.keys():
                for i in range(dictionary[word]):
                    self.listForGeneration.append(word)
            for i in range(1, nb_word + 1):
                index = randint(0, len(self.listForGeneration) - 1)
                file.write(self.listForGeneration[index] + " ")
                if i % 15 == 0 and not i == 0:
                    file.write('\n')
        else:
            currentword = choice(list(dictionary))
            file.write(currentword + ' ')
            listtemp = dictionary[currentword]
            indexfornextword = randint(0, len(listtemp) - 1)
            nextword = listtemp[indexfornextword]
            for i in range(1, nb_word + 1):
                ifPunc = randint(0, round(self.nbpunc) - 1)
                if ifPunc == 1:
                    puncindex = randint(0, len(self.punctuation) - 1)
                    file.write(self.punctuation[puncindex] + ' ')
                    continue
                currentword = nextword
                file.write(currentword + ' ')
                listtemp = dictionary[currentword]
                indexfornextword = randint(0, len(listtemp) - 1)
                nextword = listtemp[indexfornextword]
                if i % 15 == 0 and not i == 0:
                    file.write('\n')
        file.write("\n" + self.name + " ::Fin")
        file.close()


class UniGramme:
    def __init__(self, word):
        self.word = word

    def __createDic__(self):
        self.d = {}
        for word1 in self.word:
            if len(word1) > 2 or (PONC.count(word1) and len(word1) == 1):
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
        self.lastWord = ''

    def __createDic__(self, modification):
        self.d = {}
        for word1 in self.word:
            if not word1 in PONC and len(word1) > 2:
                    if len(self.lastWord) > 2 or not self.lastWord:
                        if modification and self.lastWord:
                            self.__addBucket__(self.lastWord, word1)
                        if not modification and self.lastWord:
                            self.__addBucket2__(self.lastWord, word1)
                        self.lastWord = word1
        return self.d

    def __addBucket__(self, bucket, word2):

        if bucket in self.d:
            self.d[bucket].append(word2)
        else:
            self.d[bucket] = [word2]

    def __addBucket2__(self, word1, word2):
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


class Test:
    def __init__(self, author, allauthor, directory, punctuation, mode, generation, output, path, rank):
        self.author = author
        self.allauthor = allauthor
        self.directory = directory
        self.punctuation = punctuation
        self.mode = mode
        self.generation = generation
        self.output = output
        self.path = path
        self.rank = rank

    def __testyTest__(self):
        authorsList = ['Balzac', 'Hugo', 'Ségur', 'Verne', 'Voltaire', 'Zola']

        if self.author:
            text = Text(self.directory, self.author)
            WordsList = text.__TextToWordsList__(self.punctuation,args.d)

            if self.path:
                unig = UniGramme(WordsList)
                d = unig.__createDic__()
                print(self.author, " à une proximité de :", text.__Proximite__(self.path, d, self.punctuation),
                      " avec le text Emile Zola - Germinal.txt")

            if self.rank:
                if self.mode == 1:
                    unig = UniGramme(WordsList)
                    d = unig.__createDic__()
                    toBeSorted = unig.__BucketLength__(d)
                else:
                    big = BiGramme(WordsList)
                    d = big.__createDic__(False)
                    toBeSorted = big.__BucketLength__(d)
                instances = list(toBeSorted.values())
                mergeSort(instances)
                WordsInOrder = text.__backToDic__(instances, toBeSorted, self.rank)
                for w in WordsInOrder:
                    print(w, " : ", WordsInOrder[w])

            WordsList = text.__TextToWordsList__(self.punctuation,args.d)
            if self.generation:
                file = open(self.output, 'w')
                file.write("***************************************************************************\n")
                file.close()
                if self.mode == 1:
                    unig = UniGramme(WordsList)
                    d = unig.__createDic__()
                    toBeSorted = unig.__BucketLength__(d)
                    text.__Generation__(self.output, toBeSorted, self.generation, self.mode)
                else:
                    big = BiGramme(WordsList)
                    d = big.__createDic__(True)
                    text.__Generation__(self.output, d, self.generation, self.mode)
                file = open(self.output, 'a')
                file.write('\n\n***************************************************************************\n\n')
                file.close()

        # -A -f ..\bela1003-fauj3006\TextesPourEtudiants\Ségur\ComtessedeSégur-FrançoisleBossu.txt
        if self.allauthor:
            for authors in authorsList:
                text = Text(self.directory, authors)
                WordsList = text.__TextToWordsList__(self.punctuation,args.d)

                if self.path:
                    resultList = text.__Proximite2__(self.directory, self.path, self.punctuation)
                    for i in range(0, len(resultList), 2):
                        print(resultList[i + 1], " : ", "%.4f" % resultList[i])
                if self.generation:
                    file = open(self.output, 'w')
                    file.write("***************************************************************************\n")
                    file.close()
                    if self.mode == 1:
                        unig = UniGramme(WordsList)
                        d = unig.__createDic__()
                        toBeSorted = unig.__BucketLength__(d)
                        text.__Generation__(self.output, toBeSorted, self.generation, self.mode)
                    else:
                        big = BiGramme(WordsList)
                        d = big.__createDic__(True)
                        text.__Generation__(self.output, d, self.generation, self.mode)
                    file = open(self.output, 'a')
                    file.write('\n\n***************************************************************************\n\n')
                    file.close()
                if self.rank:
                    if self.mode == 1:
                        unig = UniGramme(WordsList)
                        d = unig.__createDic__()
                        toBeSorted = unig.__BucketLength__(d)
                    else:
                        big = BiGramme(WordsList)
                        d = big.__createDic__(False)
                        toBeSorted = big.__BucketLength__(d)
                    instances = list(toBeSorted.values())
                    mergeSort(instances)
                    WordsInOrder = text.__backToDic__(instances, toBeSorted, self.rank)
                    print(authors + ': \n')
                    for w in WordsInOrder:
                        print(w, " : ", WordsInOrder[w])
                    print('\n')


### Main: lecture des paramÃ¨tres et appel des mÃ©thodes appropriÃ©es
###
###       argparse permet de lire les paramÃ¨tres sur la ligne de commande
###             Certains paramÃ¨tres sont obligatoires ("required=True")
###             Ces paramÃ¨tres doivent Ãªtres fournis Ã  python lorsque l'application est exÃ©cutÃ©e
if __name__ == "__main__":
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
            print("Fichier inconnu a"
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
start_time = time.time()
t = Test(args.a, args.A, args.d, args.P, args.m, args.G, args.g, args.f, args.F)
t.__testyTest__()

print("time it took to execute all: %.2f" % (time.time() - start_time))
