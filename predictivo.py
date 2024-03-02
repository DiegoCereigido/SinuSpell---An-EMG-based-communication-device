import re
import os

defaultTrieWordSearchDepth = 10

wordFromBookWeight: int = 1
wordFromUserWeight: int = 20

dictDeTriesPorLetra = {}    #Un diccionario que contiene un TrieNode por cada letra (raiz del Trie)
                            #que contiene todas las palabras que empiezan con esa letra
dictDePalabrasYFrecuencias = {}

class TrieNode(object):
    def __init__(self, char: str):
        super().__init__()
        self.char = char
        self.wordCount = 0
        self.children = {}
        self.endWord = False

    def addWord(self, word: str, currCharIndex: int):
        self.wordCount += 1
        nextCharIndex = currCharIndex + 1

        if nextCharIndex >= len(word):
            self.endWord = True
            return

        if word[nextCharIndex] not in self.children:
            nextNode = TrieNode(word[nextCharIndex])
            self.children[word[nextCharIndex]] = nextNode

        self.children[word[nextCharIndex]].addWord(word, nextCharIndex)
        

    def __getTrieNodeForLastCharacterInWord(self, incompleteWord: str, currCharIndex: int):
        if currCharIndex == len(incompleteWord) - 1: #Llegue al final, devuelvo las predicciones
            return self
            
        nextLetter = incompleteWord[currCharIndex + 1]
        if nextLetter not in self.children:
            return None

        trieOfNextLetter: TrieNode = self.children[nextLetter]
        return trieOfNextLetter.__getTrieNodeForLastCharacterInWord(incompleteWord, currCharIndex + 1)

    def predictNextLetter(self, incompleteWord: str):
        trieOfNextLetter: TrieNode = self.__getTrieNodeForLastCharacterInWord(incompleteWord, 0)
        if(trieOfNextLetter == None):
            return []
        
        listOfTries = list(trieOfNextLetter.children.values())
        listOfTries.sort(key=lambda trie: trie.wordCount, reverse=True)
        return listOfTries

    def predictNextWord(self, incompleteWord: str, maxDepth: int):
        trieOfNextLetter: TrieNode = self.__getTrieNodeForLastCharacterInWord(incompleteWord, 0)
        if(trieOfNextLetter == None):
            return []

        listWords = []
        trieOfNextLetter.digForNextWords(maxDepth, incompleteWord, listWords)
        sorted(listWords, key=lambda word: dictDePalabrasYFrecuencias[word], reverse=True)
        return listWords

    def digForNextWords(self, remainingDepth, currentWord, listWords):
        if(self.endWord == True):
            listWords.append(currentWord)

        if remainingDepth > 0:
            for trie in self.children.values():
                trie.digForNextWords(remainingDepth - 1, currentWord + trie.char, listWords)

#Codigo al inicio, para cargar entrenamiento previo, cada vez que se abre el programa
def OpenExistingDictionaryWithFrequencies(dictionaryFilePath: str):
    if not ( os.path.exists(dictionaryFilePath)):
        return

    with open(dictionaryFilePath, 'r', encoding='utf-8') as f:
        listaDePalabras = f.read().splitlines()

    abecedario = "abcdefghijklmnñopqrstuvwxyz"
    for letter in abecedario:
        dictDeTriesPorLetra[letter] = TrieNode(letter)

    for linea in listaDePalabras:
        if ',' in linea:
            palabra, frecuencia = linea.split(",")
            frecuencia = int(frecuencia)
        else:
            palabra = linea
            frecuencia = 0

        if(len(palabra) > 0):
            palabra = palabra.lower()
            LearnNewWord(palabra, frecuencia)

#Codigo por cada prediccion
def NextMostProbableLetters(incompleteWord: str, maxPredictionsFromTrie: int):
    trie: TrieNode = dictDeTriesPorLetra[incompleteWord[0]]
    triesPredicciones = trie.predictNextLetter(incompleteWord) #primeras N letras mas probables, ordenadas
    
    triePrediccionesLetras = [triesPredicciones[i].char for i in range(min(len(triesPredicciones), maxPredictionsFromTrie))]

    otherLetters = MostUsedGlobalLettersInRange(0, len(dictDeTriesPorLetra))
    otherLetters = [letter for letter in otherLetters if letter not in triePrediccionesLetras]
    
    triePrediccionesLetras.extend(otherLetters)

    return triePrediccionesLetras

#Codigo por cada prediccion
def NextMostProbableWords(incompleteWord: str, searchDepth: int):
    trie: TrieNode = dictDeTriesPorLetra[incompleteWord[0]]
    #probables (por frecuencia), a una profundidad maxima searchDepth del nodo donde termina la palabra incompleta escrita por el usuario
    return trie.predictNextWord(incompleteWord, searchDepth)

def MostUsedGlobalLettersInRange(first: int, last: int):
    listOfTries = list(dictDeTriesPorLetra.values())
    listOfTries.sort(key=lambda trie: trie.wordCount, reverse=True)

    return [listOfTries[i].char for i in range(max(0, first), min(last + 1, len(listOfTries)))]

#Aprende la palabra si no esta en el diccionario, y agrega la frecuencia de uso del usuario 
#para mejorar prediccion
#¡OJO! Pasar solo palabras validas (es decir, que no incluyan tildes, comas, puntos, espacios... solo letras)
def SelectWord(word: str):
    word = word.lower()
    if word not in dictDePalabrasYFrecuencias:
        LearnNewWord(word)

    dictDePalabrasYFrecuencias[word] += wordFromUserWeight #Para que pese mas lo que escribe el usuario que lo que hay en los libros

#Guardar los cmabios en frecuencias cuando se cierre el programa
def SaveCurrentDictionary(dictionaryFilePath: str): 
    with open(dictionaryFilePath, 'w', encoding='utf-8') as f:
        for palabra, frecuencia in dictDePalabrasYFrecuencias.items():
            f.write(f"{palabra},{frecuencia}\n")

def Train(bookFilePath: str):
    if not (os.path.exists(bookFilePath)):
        return

    with open(bookFilePath, 'r', encoding='utf-8') as f:
        text = f.read()
        text = re.sub('[^A-Za-z]+', ' ', text, flags=re.IGNORECASE)
        text = text.lower()
        palabras = text.split(" ")

        for palabra in palabras:
            if len(palabra) > 0:
                if palabra not in dictDePalabrasYFrecuencias:
                    LearnNewWord(palabra)
                    
                dictDePalabrasYFrecuencias[palabra] += wordFromBookWeight

def LearnNewWord(word: str, frecuencia: int = 0):
    if word not in dictDePalabrasYFrecuencias:
        primeraLetra = word[0]
        trie: TrieNode = dictDeTriesPorLetra[primeraLetra]
        trie.addWord(word, 0)
        dictDePalabrasYFrecuencias[word] = frecuencia;

#Main
OpenExistingDictionaryWithFrequencies("listado-general.txt")

#Esto haganlo una sola vez (NO CADA VEZ QUE SE ABRE PORQUE SE APRENDE UNA SOLA VEZ Y LUEGO SE GUARDA) u ofrezcan al usuario la opcion de aprender de un libro que quiera
Train("cien_anos_de_soledad.txt")
SaveCurrentDictionary("listado-general.txt") #Guardaria despues de entrenar para poder hacerlo una sola vez

numberOfLettersToPredictEachTime = 9
letterOrderFirstPrediction = 0
letterOrderLastPrediction = numberOfLettersToPredictEachTime

nextProbableWords = []
nextMostProbableLetters = MostUsedGlobalLettersInRange(letterOrderFirstPrediction, letterOrderLastPrediction)

print(f"Las 9 primeras letras mas usadas del diccionario actual son: {nextMostProbableLetters}")

print() #Linea en blanco


while True:
    palabraIncompleta: str = input().lower()

    if(palabraIncompleta[len(palabraIncompleta) - 1] == " "):
        palabraIncompleta = palabraIncompleta[:-1]
        if(len(palabraIncompleta) > 0):
            #Hagamos de cuenta que selecciono esta palabra, para "aprender" que el usuario usa mucho esto y sugerirla mas seguido. Recordar guardar al final.
            SelectWord(palabraIncompleta)
    else:
        if(palabraIncompleta[len(palabraIncompleta) - 1] == "+"):
            palabraIncompleta = palabraIncompleta[:-1]
            letterOrderFirstPrediction = letterOrderLastPrediction + 1
            letterOrderLastPrediction = letterOrderLastPrediction + numberOfLettersToPredictEachTime        
        else:
            letterOrderFirstPrediction = 0
            letterOrderLastPrediction = numberOfLettersToPredictEachTime
            nextProbableWords = NextMostProbableWords(palabraIncompleta, defaultTrieWordSearchDepth)
            nextMostProbableLetters = NextMostProbableLetters(palabraIncompleta, 24)

        print(f"Posibles proximas letras: {nextMostProbableLetters[letterOrderFirstPrediction:letterOrderLastPrediction]}")    
        print(f"Posibles proximas palabras: {nextProbableWords[letterOrderFirstPrediction:letterOrderLastPrediction]}")

SaveCurrentDictionary("listado-general.txt") #Guarden al salir dle programa, para guardar lo que se aprendio del usuario mismo