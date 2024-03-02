import sys  
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from time import perf_counter as timer
from PyQt5.QtCore import QThread
import time
import queue
from gtts import gTTS
from playsound import playsound
import os
import re
import serial
import string
import random
import numpy as np

################################################################################################
# Predictivo

defaultTrieWordSearchDepth = 10

wordFromBookWeight: int = 1
wordFromUserWeight: int = 20

Tiempo_Busqueda_Binaria = 1
Tiempo_Busqueda_Lineal = 1
Idioma = 'es' #Codigos = Esp,Ing,Ita
lista_actual = 'lista-español-copia.txt'
abecedario = 'abcdefghijklmnñopqrstuvwxyz'

def CambiarTodo(idioma: str):
    if idioma == 'español':
        botonfrases = 'Frases'
        botonteclado = 'Teclado'
        bienvenida = 'Bienvenido'
        texto1 = 'Elija modo de uso'
        frase1 = 'Hola'
        frase2 = 'Ayuda'
        frase3 = 'Quiero comer'
        frase4 = 'Quiero ir a dormir'
        frase5 = 'Tengo calor'
        frase6 = 'Por favor'
        frase7 = 'Ir a Configuración'
        frase8 = 'Chau'
        frase9 = 'Estoy bien'
        frase10 = 'Gracias'
        frase11 = 'Quiero ir al baño'
        frase12 = 'Tengo frío'
        frase13 = 'Ir al Teclado'
        frase14 = 'Ir al Menú de Inicio'
        botonvoz = 'Voz'
        botonpalabras = 'Palabras'
        botonfrases = 'Frases'
        botoninicio = 'Inicio'
        botonborrar = 'Borrar'
        botonespacio = 'Espacio'
        botonactualizar = 'Actua-\nlizar'
        textobusqbin = 'Tiempo: Búsqueda binaria'
        textobusqlin = 'Tiempo: Búsqueda lineal'
        textoidioma = 'Idioma'
        volver = 'Volver'

    if idioma == 'frances':
        botonfrases = 'Phrases'
        botonteclado = 'Clavier'
        bienvenida = 'Bienvenue'
        texto1 = 'Choisissez comment utilizer'
        frase1 = 'Salut'
        frase2 = 'Aider'
        frase3 = 'Je veux manger'
        frase4 = 'Je veux dormir'
        frase5 = "J'ai chaud"
        frase6 = "S'il vous plaît"
        frase7 = 'Aller aux paramètres'
        frase8 = 'Au revoir'
        frase9 = 'Je vais bien'
        frase10 = 'Merci'
        frase11 = 'Je veux aller au toilettes'
        frase12 = "J'ai froid"
        frase13 = 'Aller au clavier'
        frase14 = 'Aller au écran de début'
        botonvoz = 'Voix'
        botonpalabras = 'Mots'
        botonfrases = 'Phrases'
        botoninicio = 'Début'
        botonborrar = 'Effacer'
        botonespacio = 'Espacer'
        botonactualizar = 'Actua-\nlizer'
        textobusqbin = 'Temps: recherche binaire'
        textobusqlin = 'Temps: recherche linéaire'
        textoidioma = 'Langue'
        volver = 'Revenir'

    if idioma == 'ingles':
        botonfrases = 'Phrases'
        botonteclado = 'Keyboard'
        bienvenida = 'Welcome'
        texto1 = 'Choose mode'
        frase1 = 'Hello'
        frase2 = 'Help'
        frase3 = "I'm hungry "
        frase4 = "I'm tired"
        frase5 = "It's hot in here"
        frase6 = 'Please'
        frase7 = 'Configuration'
        frase8 = 'Bye'
        frase9 = "I'm fine"
        frase10 = 'Thank you'
        frase11 = "I want to go to the toilet"
        frase12 = "It's cold in here"
        frase13 = 'Go to the keyboard'
        frase14 = 'Go to the Menu'
        botonvoz = 'Voice'
        botonpalabras = 'Words'
        botonfrases = 'Phrases'
        botoninicio = 'Menu'
        botonborrar = 'Delete'
        botonespacio = 'Space'
        botonactualizar = 'Update'
        textobusqbin = 'Time: Binary search'
        textobusqlin = 'Time: Linear search'
        textoidioma = 'Language'
        volver = 'Back'

    if idioma == 'italiano':
        botonfrases = 'Frasi'
        botonteclado = 'Tastiera'
        bienvenida = 'Benvenuto'
        texto1 = 'Scegliere modalità di utilizzo'
        frase1 = 'Ciao'
        frase2 = 'Aiuto'
        frase3 = 'Voglio mangiare'
        frase4 = 'Voglio dormire'
        frase5 = 'Ho caldo'
        frase6 = 'Per favore'
        frase7 = 'Configurazione'
        frase8 = 'Ciao'
        frase9 = 'Tutto apposto'
        frase10 = 'Grazie'
        frase11 = 'Voglio andare in bagno'
        frase12 = 'Ho freddo'
        frase13 = 'Andare alla tastiera'
        frase14 = 'Andare allo schermo iniziale'
        botonvoz = 'Voce'
        botonpalabras = 'Parole'
        botonfrases = 'Frasi'
        botoninicio = 'Inizio'
        botonborrar = 'Cancel-\nlare'
        botonespacio = 'Spazie'
        botonactualizar = 'Aggior-\nnare'
        textobusqbin = 'Tempo: Ricerca binaria'
        textobusqlin = 'Tempo: Ricerca lineale'
        textoidioma = 'Lingua'
        volver = 'Ritornare'

    if idioma == 'aleman':
        botonfrases = 'Sätze'
        botonteclado = 'Tastatur'
        bienvenida = 'Willkommen'
        texto1 = 'Wählen sie die Verwendung aus'
        frase1 = 'Hallo'
        frase2 = 'Hilfe'
        frase3 = 'Ich will essen'
        frase4 = 'Ich möchte schlafen'
        frase5 = 'Ich bin heiß'
        frase6 = 'Bitte'
        frase7 = 'Gehe zu den Einstellungen'
        frase8 = 'Wiedersehen'
        frase9 = 'Es geht mir gut'
        frase10 = 'Vielen Dank'
        frase11 = 'Ich möchte auf die Toilette gehen'
        frase12 = 'Es ist mir kalt'
        frase13 = 'Zur tastatur gehen'
        frase14 = 'Gehe ins Startmenü'
        botonvoz = 'Laut\nsprechen'
        botonpalabras = 'Worten'
        botonfrases = 'Sätze'
        botoninicio = 'Anfang'
        botonborrar = 'Löschen'
        botonespacio = 'Leer\ntaste'
        botonactualizar = 'Aktuali-\nsieren'
        textobusqbin = 'Zeit: Binäre Suche'
        textobusqlin = 'Zeit: Lineare Suche'
        textoidioma = 'Idiom'
        volver = 'Zurückgehen'
    
    
    pantalla_principal.label.setText(bienvenida)
    pantalla_principal.label_2.setText(texto1)
    pantalla_principal.Frases.setText(botonfrases)
    pantalla_principal.Teclado.setText(botonteclado)
    pantalla_principal_bloqueada.label.setText(bienvenida)
    pantalla_principal_bloqueada.label_2.setText(texto1)
    pantalla_principal_bloqueada.Frases.setText(botonfrases)
    pantalla_principal_bloqueada.Teclado.setText(botonteclado)
    frases.frase1.setText(frase1)
    frases.frase2.setText(frase2)
    frases.frase3.setText(frase3)
    frases.frase4.setText(frase4)
    frases.frase5.setText(frase5)
    frases.frase6.setText(frase6)
    frases.frase7.setText(frase7)
    frases.frase8.setText(frase8)
    frases.frase9.setText(frase9)
    frases.frase10.setText(frase10)
    frases.frase11.setText(frase11)
    frases.frase12.setText(frase12)
    frases.IrTeclado_2.setText(frase13)
    frases.VolverInicio_2.setText(frase14)
    frases_bloqueada.frase1.setText(frase1)
    frases_bloqueada.frase2.setText(frase2)
    frases_bloqueada.frase3.setText(frase3)
    frases_bloqueada.frase4.setText(frase4)
    frases_bloqueada.frase5.setText(frase5)
    frases_bloqueada.frase6.setText(frase6)
    frases_bloqueada.frase7.setText(frase7)
    frases_bloqueada.frase8.setText(frase8)
    frases_bloqueada.frase9.setText(frase9)
    frases_bloqueada.frase10.setText(frase10)
    frases_bloqueada.frase11.setText(frase11)
    frases_bloqueada.frase12.setText(frase12)
    frases_bloqueada.IrTeclado_2.setText(frase13)
    frases_bloqueada.VolverInicio_2.setText(frase14)    
    teclado.c4.setText(botonvoz)
    teclado.c8.setText(botonpalabras)
    teclado.c12.setText(botonfrases)
    teclado.c13.setText(botonactualizar)
    teclado.c14.setText(botonespacio)
    teclado.c15.setText(botonborrar)
    teclado.c16.setText(botoninicio)
    teclado_bloqueado.c4.setText(botonvoz)
    teclado_bloqueado.c8.setText(botonpalabras)
    teclado_bloqueado.c12.setText(botonfrases)
    teclado_bloqueado.c13.setText(botonactualizar)
    teclado_bloqueado.c14.setText(botonespacio)
    teclado_bloqueado.c15.setText(botonborrar)
    teclado_bloqueado.c16.setText(botoninicio)
    teclado_predictivo.c4.setText(botonvoz)
    teclado_predictivo.c8.setText(botonpalabras)
    teclado_predictivo.c12.setText(botonfrases)
    teclado_predictivo.c13.setText(botonactualizar)
    teclado_predictivo.c14.setText(botonespacio)
    teclado_predictivo.c15.setText(botonborrar)
    teclado_predictivo.c16.setText(botoninicio)    
    configuracion.label.setText(textoidioma)
    configuracion.label_2.setText(textobusqbin)
    configuracion.label_4.setText(textobusqlin)
    configuracion.Volver.setText(volver)
    configuracion_bloqueado.label.setText(textoidioma)
    configuracion_bloqueado.label_2.setText(textobusqbin)
    configuracion_bloqueado.label_4.setText(textobusqlin)
    configuracion_bloqueado.Volver.setText(volver)
    return

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
        listWords = sorted(listWords, key=lambda word: dictDePalabrasYFrecuencias[word], reverse=True)
        return listWords

    def digForNextWords(self, remainingDepth, currentWord, listWords):
        if(self.endWord == True):
            listWords.append(currentWord)

        if remainingDepth > 0:
            for trie in self.children.values():
                trie.digForNextWords(remainingDepth - 1, currentWord + trie.char, listWords)

#Codigo al inicio, para cargar entrenamiento previo, cada vez que se abre el programa
def OpenExistingDictionaryWithFrequencies(dictionaryFilePath: str, abecedario):
    if not ( os.path.exists(dictionaryFilePath)):
        return

    with open(dictionaryFilePath, 'r', encoding='utf-8-sig') as f:
        listaDePalabras = f.read().splitlines()

    #abecedario = "abcdefghijklmnñopqrstuvwxyzè"
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
    with open(dictionaryFilePath, 'w', encoding='utf-8-sig') as f:
        for palabra, frecuencia in dictDePalabrasYFrecuencias.items():
            f.write(f"{palabra},{frecuencia}\n")

def Train(bookFilePath: str):
    if not (os.path.exists(bookFilePath)):
        return

    with open(bookFilePath, 'r', encoding='utf-8-sig') as f:
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
        dictDePalabrasYFrecuencias[word] = frecuencia

#Main

dictDeTriesPorLetra = {}    #Un diccionario que contiene un TrieNode por cada letra (raiz del Trie)
                            #que contiene todas las palabras que empiezan con esa letra
dictDePalabrasYFrecuencias = {}

#Codigo al inicio, para "entrenar", cada vez que se abre el programa

################################################################################################
class AnotherThread(QThread):  
    
    def __init__(self):
        super(AnotherThread,self).__init__()
        self.funcion = 0

        self.modo = 0

    def run(self):
        while 1:
            if self.funcion == 0:
                worker.Teclado_o_Frases()
            if self.funcion == 1:
                worker.SeleccionFrases()
            if self.funcion == 2:
                worker.SeleccionCaracteres()
            if self.funcion == 3:
                worker.SeleccionPalabra()
            if self.funcion == 4:
                worker.Configuracion()
            if self.funcion == 5:
                worker.SeleccionOpcionesConfiguracion(self.modo)

class ThreadGuino(QThread):  

    def __init__(self, umbral):
        super(ThreadGuino,self).__init__()
        self.umbral = umbral


    def run(self):
        thread.workerguino.Guino(self.umbral)

class WorkerGuino(QtCore.QObject):
    Guiño = False
    
    def __init__(self,serial):
        super(WorkerGuino,self).__init__()
        self.ser = serial
    def Guino(self, umbral):
        t0 = 0
        V = 0
        while 1:
            if self.ser.in_waiting != 0:
                b = self.ser.readline()
                V = float(b.decode().rstrip())

            
            t1 = timer()
            if V > umbral and self.Guiño == False: #El usuario guiñó. Solo entro una vez
                self.Guiño = True
                
                booleano = True
                q.put(booleano)

                t0 = timer()

      
            elif (t1-t0)>0.3: #Si hay 1000 muestras menor al umbral, considero terminado el guiño del usuario
                self.Guiño = False
                V = 0
    
class Worker(QtCore.QObject):
    #Señales para actualizar colores y seleccionar letras/palabras
    lista_con_colores_teclado = QtCore.pyqtSignal(list)
    lista_con_colores_frases = QtCore.pyqtSignal(list)
    lista_con_colores_predictivo = QtCore.pyqtSignal(list)
    lista_con_booleanos_teclado = QtCore.pyqtSignal(list)
    lista_con_booleanos_teclado_bloqueado = QtCore.pyqtSignal(list)
    lista_con_booleanos_teclado_predictivo = QtCore.pyqtSignal(list)
    lista_con_booleanos_frases = QtCore.pyqtSignal(list)
    lista_con_booleanos_predictivo_tecladocomun = QtCore.pyqtSignal(list)
    lista_con_booleanos_predictivo_tecladobloqueado = QtCore.pyqtSignal(list)
    lista_con_booleanos_predictivo_tecladopredictivo = QtCore.pyqtSignal(list)
    lista_con_booleanos_config = QtCore.pyqtSignal(list)
    lista_colores_seleccion_config = QtCore.pyqtSignal(list)


    #Señales para mostrar pantallas
    Frases = QtCore.pyqtSignal()
    Teclado = QtCore.pyqtSignal()
    Teclado_bloqueado = QtCore.pyqtSignal()
    Teclado_predictivo = QtCore.pyqtSignal()
    Pantalla_principal = QtCore.pyqtSignal()
    Pantalla_principal_bloqueada = QtCore.pyqtSignal()
    Frases_bloqueada = QtCore.pyqtSignal()
    Config_bloqueada = QtCore.pyqtSignal()
    Config = QtCore.pyqtSignal()


    #Señales para mostrar la frase elegida en los teclados
    MostrarFraseEnTeclado = QtCore.pyqtSignal(str)
    MostrarFraseEnTecladoBloqueado = QtCore.pyqtSignal(str)
    MostrarFraseEnTecladoPredictivo = QtCore.pyqtSignal(str)

    #Señales para actualizar caracteres y palabras del predictivo
    CargarTexto = QtCore.pyqtSignal()
    lista_con_caracteres_tecladocomun = QtCore.pyqtSignal(list)
    lista_con_palabras_tecladocomun = QtCore.pyqtSignal(list)
    lista_con_caracteres_tecladobloqueado = QtCore.pyqtSignal(list)
    lista_con_palabras_tecladobloqueado = QtCore.pyqtSignal(list)
    lista_con_caracteres_tecladopredictivo = QtCore.pyqtSignal(list)
    lista_con_palabras_tecladopredictivo = QtCore.pyqtSignal(list)

    lista_con_palabras_tecladocomun = QtCore.pyqtSignal(list)
    lista_con_palabras_tecladobloqueado = QtCore.pyqtSignal(list)
    lista_con_palabras_tecladopredictivo = QtCore.pyqtSignal(list)

    def __init__(self):
        super(Worker,self).__init__()

    def Teclado_o_Frases(self):     
        
        self.Pantalla_principal_bloqueada.emit()
        guiño = False
        while 1:

            guiño = q.get() #Espera hasta recibir un guiño

            self.Pantalla_principal.emit()
            if guiño:
                guiño = False
                t0 = timer()
                while 1:
                    
                    if not q.empty():
                        guiño = q.get()
                    
                    t1 = timer()
                    if guiño:
                        thread.funcion = 1                        
                        return
                        
                    elif (t1-t0) > Tiempo_Busqueda_Binaria:
                        thread.funcion = 2
                        return

    def SeleccionCaracteres(self):
        ActualizarCaracteres = False

        numberOfLettersToPredictEachTime = 9
        letterOrderFirstPrediction = 0
        letterOrderLastPrediction = numberOfLettersToPredictEachTime

        lista_todas_palabras = ['']*100
        lista_todos_caracteres = ['E', 'A' , 'O', 'S', 'R', 'N', 'I', 'D', 'L', 'C', 'T', 'U', 'M', 'P', 'B', 'G', 'V', 'Y', 'Q', 'H', 'F', 'Z', 'J', 'Ñ', 'X', 'K', 'W']        

        
        lista_palabras = ['']*5       
        lista_caracteres = ['E', 'A' , 'O', 'S', 'R', 'N', 'I', 'D', 'L']

        self.lista_con_caracteres_tecladocomun.emit(lista_caracteres)
        self.lista_con_caracteres_tecladobloqueado.emit(lista_caracteres)
        self.lista_con_caracteres_tecladopredictivo.emit(lista_caracteres)

        self.lista_con_palabras_tecladocomun.emit(lista_palabras)
        self.lista_con_palabras_tecladobloqueado.emit(lista_palabras)
        self.lista_con_palabras_tecladopredictivo.emit(lista_palabras)

        R = 'rgb(255,0,0)'
        A = 'rgb(0,0,255)'
        G = 'rgb(127,127,160)'
        VO = 'rgb(0,127,0)'
        VC = 'rgb(0,255,0)'

        T = True
        F = False
        
        while 1:
            self.Teclado_bloqueado.emit()
            time.sleep(2)
            while not q.empty():
                guiño = q.get()     #Si se guiñó mientras la pantalla estaba bloqueada, agarro los guiños y los desecho
            guiño = False

            lista_colores = [R, R, A, A, R, R, A, A, R, R, A, A, R, R, A, A]
            self.lista_con_colores_teclado.emit(lista_colores)
            self.Teclado.emit()
            time.sleep(0.11)
            #Primera selección
            t0 = timer()
            while 1:
                bloquear = False    #Variable booleana que me permite bloquear la pantalla en el caso de que se use el boon de voz
                t1 = timer()
                if not q.empty():
                    guiño = q.get()

                if guiño:
                    guiño1 = True
                    #Asigno Rojo, Azul, y Gris como corresponda
                    lista_colores = [R, R, G, G, R, R, G, G, A, A, G, G, A, A, G, G]
                    self.lista_con_colores_teclado.emit(lista_colores)
                    break
                elif (t1-t0) > Tiempo_Busqueda_Binaria:
                    guiño1 = False
                    #Asigno Rojo, Azul, y Gris como corresponda
                    lista_colores = [G, G, R, R, G, G, R, R, G, G, A, A, G, G, A, A]
                    self.lista_con_colores_teclado.emit(lista_colores)
                    break
            
            #Segunda selección
            t0 = timer()
            guiño = False
            while 1:
                t1 = timer()

                if not q.empty():
                    guiño = q.get()
                if guiño1:
                    if guiño:
                        guiño2 = True
                        #Asigno Rojo, Azul, y Gris como corresponda
                        lista_colores = [R, A, G, G, R, A, G, G, G, G, G, G, G, G, G, G]
                        self.lista_con_colores_teclado.emit(lista_colores)
                        break
                  
                    elif (t1-t0) > Tiempo_Busqueda_Binaria:
                        guiño2 = False
                        #Asigno Rojo, Azul, y Gris como corresponda
                        lista_colores = [G, G, G, G, G, G, G, G, R, A, G, G, R, A, G, G]
                        self.lista_con_colores_teclado.emit(lista_colores)
                        break


                else:
                    if guiño:
                        guiño2 = True
                        #Asigno Rojo, Azul, y Gris como corresponda
                        lista_colores = [G, G, R, A, G, G, R, A, G, G, G, G, G, G, G, G]
                        self.lista_con_colores_teclado.emit(lista_colores)
                        break
                   
                    elif (t1-t0) > Tiempo_Busqueda_Binaria:
                        guiño2 = False
                        #Asigno Rojo, Azul, y Gris como corresponda
                        lista_colores = [G, G, G, G, G, G, G, G, G, G, R, A, G, G, R, A]
                        self.lista_con_colores_teclado.emit(lista_colores)
                        break            
            #Tercera selección
            t0 = timer()
            guiño = False
            while 1:
                t1 = timer()
                if not q.empty():
                    guiño = q.get()
                if guiño1:
                    if guiño2:
                        if guiño:
                            guiño3 = True
                            #Asigno Rojo, Azul, y Gris como corresponda
                            lista_colores = [R, G, G, G, A, G, G, G, G, G, G, G, G, G, G, G]
                            self.lista_con_colores_teclado.emit(lista_colores)
                            break
                     
                        elif (t1-t0) > Tiempo_Busqueda_Binaria:
                            guiño3 = False
                            #Asigno Rojo, Azul, y Gris como corresponda
                            lista_colores = [G, R, G, G, G, A, G, G, G, G, G, G, G, G, G, G]
                            self.lista_con_colores_teclado.emit(lista_colores)
                            break
                          
                    else:
                        if guiño:
                            guiño3 = True
                            #Asigno Rojo, Azul, y Gris como corresponda
                            lista_colores = [G, G, G, G, G, G, G, G, R, G, G, G, A, G, G, G]
                            self.lista_con_colores_teclado.emit(lista_colores)
                            break                        
                        elif (t1-t0) > Tiempo_Busqueda_Binaria:
                            guiño3 = False
                            #Asigno Rojo, Azul, y Gris como corresponda
                            lista_colores = [G, G, G, G, G, G, G, G, G, R, G, G, G, A, G, G]
                            self.lista_con_colores_teclado.emit(lista_colores)
                            break

                else:
                    if guiño2:
                        if guiño:
                            guiño3 = True
                            #Asigno Rojo, Azul, y Gris como corresponda
                            lista_colores = [G, G, R, G, G, G, A, G, G, G, G, G, G, G, G, G]
                            self.lista_con_colores_teclado.emit(lista_colores)
                            break
                        elif (t1-t0) > Tiempo_Busqueda_Binaria:
                            guiño3 = False
                            #Asigno Rojo, Azul, y Gris como corresponda
                            lista_colores = [G, G, G, R, G, G, G, A, G, G, G, G, G, G, G, G]
                            self.lista_con_colores_teclado.emit(lista_colores)
                            break
                    else:
                        if guiño:
                            guiño3 = True
                            #Asigno Rojo, Azul, y Gris como corresponda
                            lista_colores = [G, G, G, G, G, G, G, G, G, G, R, G, G, G, A, G]
                            self.lista_con_colores_teclado.emit(lista_colores)
                            break

                        elif (t1-t0) > Tiempo_Busqueda_Binaria:
                            guiño3 = False
                            #Asigno Rojo, Azul, y Gris como corresponda
                            lista_colores = [G, G, G, G, G, G, G, G, G, G, G, R, G, G, G, A]
                            self.lista_con_colores_teclado.emit(lista_colores)
                            break
            #Cuarta selección
            t0 = timer()
            guiño = False
            while 1:
                t1 = timer()
                if not q.empty():
                    guiño = q.get()
                if guiño1:
                    if guiño2:
                        if guiño3:
                            if guiño:
                                #BOTON 1 : Primer caracter
                                #Asigno Rojo, Azul, y Gris como corresponda
                                lista_booleanos = [T,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F]
                                self.lista_con_booleanos_teclado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_bloqueado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_predictivo.emit(lista_booleanos)


                                #txt = self.texto.text()+self.c1.text()
                                #self.texto.setText(txt)
                                lista_colores = [VC, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                break

                            elif (t1-t0) > Tiempo_Busqueda_Binaria:
                                #BOTON 5 : Cuarto caracter        
                                #Asigno Rojo, Azul, y Gris como corresponda
                                lista_booleanos = [F,F,F,F,T,F,F,F,F,F,F,F,F,F,F,F]
                                self.lista_con_booleanos_teclado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_bloqueado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_predictivo.emit(lista_booleanos)

                                
                                #txt = self.texto.text()+self.c5.text()
                                #self.texto.setText(txt)
                                lista_colores = [G, G, G, G, VC, G, G, G, G, G, G, G, G, G, G, G]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                break

                        else:
                            if guiño:
                                #BOTON 2 : Segundo caracter 
                                #Asigno Rojo, Azul, y Gris como corresponda
                                lista_booleanos = [F,T,F,F,F,F,F,F,F,F,F,F,F,F,F,F]
                                self.lista_con_booleanos_teclado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_bloqueado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_predictivo.emit(lista_booleanos)

                                
                                #txt = self.texto.text()+self.c2.text()
                                #self.texto.setText(txt)
                                lista_colores = [G, VC, G, G, G, G, G, G, G, G, G, G, G, G, G, G]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                break
                            elif (t1-t0) > Tiempo_Busqueda_Binaria:
                                #BOTON 6 : Quinto caracter
                                #Asigno Rojo, Azul, y Gris como corresponda
                                lista_booleanos = [F,F,F,F,F,T,F,F,F,F,F,F,F,F,F,F]
                                self.lista_con_booleanos_teclado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_bloqueado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_predictivo.emit(lista_booleanos)

                                
                                #txt = self.texto.text()+self.c6.text()
                                #self.texto.setText(txt)                                
                                lista_colores = [G, G, G, G, G, VC, G, G, G, G, G, G, G, G, G, G]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                break
                    else:
                        if guiño3:
                            if guiño:
                                #BOTON 9 : Septimo caracter
                                #Asigno Rojo, Azul, y Gris como corresponda
                                lista_booleanos = [F,F,F,F,F,F,F,F,T,F,F,F,F,F,F,F]
                                self.lista_con_booleanos_teclado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_bloqueado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_predictivo.emit(lista_booleanos)

                                

                                #txt = self.texto.text()+self.c9.text()
                                #self.texto.setText(txt)
                                lista_colores = [G, G, G, G, G, G, G, G, VC, G, G, G, G, G, G, G]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                break
                            
                            elif (t1-t0) > Tiempo_Busqueda_Binaria:
                                #BOTON 13 : Actualizar caracteres
                                #Asigno Rojo, Azul, y Gris como corresponda
                                lista_colores = [G, G, G, G, G, G, G, G, G, G, G, G, VC, G, G, G]
                                self.lista_con_colores_teclado.emit(lista_colores)

                                ActualizarCaracteres = True
                                break
                        else:
                            if guiño:
                                #BOTON 10 : Octavo caracter 
                                #Asigno Rojo, Azul, y Gris como corresponda
                                lista_booleanos = [F,F,F,F,F,F,F,F,F,T,F,F,F,F,F,F]
                                self.lista_con_booleanos_teclado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_bloqueado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_predictivo.emit(lista_booleanos)

                                #txt = self.texto.text()+self.c10.text()
                                #self.texto.setText(txt)                                
                                lista_colores = [G, G, G, G, G, G, G, G, G, VC, G, G, G, G, G, G]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                break
                            elif (t1-t0) > Tiempo_Busqueda_Binaria:
                                #BOTON 14 : Espacio
                                #Asigno Rojo, Azul, y Gris como corresponda
                                lista_booleanos = [F,F,F,F,F,F,F,F,F,F,F,F,F,T,F,F]
                                self.lista_con_booleanos_teclado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_bloqueado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_predictivo.emit(lista_booleanos)


                                
                                lista_colores = [G, G, G, G, G, G, G, G, G, G, G, G, G, VC, G, G]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                break            
                else:        
                    if guiño2:
                        if guiño3:
                            if guiño:
                                #BOTON 3 : Tercer caracter
                                #Asigno Rojo, Azul, y Gris como corresponda
                                lista_booleanos = [F,F,T,F,F,F,F,F,F,F,F,F,F,F,F,F]
                                self.lista_con_booleanos_teclado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_bloqueado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_predictivo.emit(lista_booleanos)


                                #txt = self.texto.text()+self.c3.text()
                                #self.texto.setText(txt)
                                lista_colores = [G, G, VC, G, G, G, G, G, G, G, G, G, G, G, G, G]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                break
                            elif (t1-t0) > Tiempo_Busqueda_Binaria:
                                #BOTON 7 : Sexto caracter
                                #Asigno Rojo, Azul, y Gris como corresponda
                                lista_booleanos = [F,F,F,F,F,F,T,F,F,F,F,F,F,F,F,F]
                                self.lista_con_booleanos_teclado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_bloqueado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_predictivo.emit(lista_booleanos)


                                #txt = self.texto.text()+self.c7.text()
                                #self.texto.setText(txt)
                                lista_colores = [G, G, G, G, G, G, VC, G, G, G, G, G, G, G, G, G]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                break
                        else:
                            if guiño:
                                #BOTON 4 : Voz
                                #Asigno Rojo, Azul, y Gris como corresponda
                                lista_colores = [G, G, G, VC, G, G, G, G, G, G, G, G, G, G, G, G]
                                self.lista_con_colores_teclado.emit(lista_colores)

                                #Aca hago lo de reproducir
                                texto = teclado.texto.text()
                                if texto == '':
                                    texto = 'No hay nada escrito'
                                arc = gTTS(texto, lang = Idioma)
                                
                                nombre_archivo = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)))
                                nombre_archivo = nombre_archivo + '.mp3'

                                #nombre_archivo = 'archivo' + texto + '.mp3'                                
                                arc.save(nombre_archivo)
                                playsound(nombre_archivo)
                                #Aca termina lo de reproducir
                                os.remove(nombre_archivo)
                                bloquear = True
                                break
                            elif (t1-t0) > Tiempo_Busqueda_Binaria:
                                #BOTON 8 : Palabras
                                #Asigno Rojo, Azul, y Gris como corresponda
                                lista_colores = [G, G, G, G, G, G, G, VC, G, G, G, G, G, G, G, G]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                time.sleep(0.11)
                                
                                thread.funcion = 3
                                self.Teclado_predictivo.emit()

                                lista_colores = [R, R, A, A, R, R, A, A, R, R, A, A, R, R, A, A]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                return
                    else:
                        if guiño3:
                            if guiño:
                                #BOTON 11 : Noveno caracter
                                #Asigno Rojo, Azul, y Gris como corresponda
                                lista_booleanos = [F,F,F,F,F,F,F,F,F,F,T,F,F,F,F,F]
                                self.lista_con_booleanos_teclado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_bloqueado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_predictivo.emit(lista_booleanos)


                                #txt = self.texto.text()+self.c11.text()
                                #self.texto.setText(txt)                                
                                lista_colores = [G, G, G, G, G, G, G, G, G, G, VC, G, G, G, G, G]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                break
                            elif (t1-t0) > Tiempo_Busqueda_Binaria:
                                #BOTON 15 : Borrar
                                #Asigno Rojo, Azul, y Gris como corresponda
                                lista_booleanos = [F,F,F,F,F,F,F,F,F,F,F,F,F,F,T,F]
                                self.lista_con_booleanos_teclado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_bloqueado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_predictivo.emit(lista_booleanos)


                                
                                lista_colores = [G, G, G, G, G, G, G, G, G, G, G, G, G, G, VC, G]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                break
                        else:
                            if guiño:
                                #BOTON 12 : Ir a Frases
                                #Asigno Rojo, Azul, y Gris como corresponda

                                lista_colores = [G, G, G, G, G, G, G, G, G, G, G, VC, G, G, G, G]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                time.sleep(0.11)
                                thread.funcion = 1
                                self.Frases.emit()

                                lista_colores = [R, R, A, A, R, R, A, A, R, R, A, A, R, R, A, A]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                
                                lista_booleanos = [False]*16
                                self.lista_con_booleanos_teclado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_bloqueado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_predictivo.emit(lista_booleanos)


                                return

                            elif (t1-t0) > Tiempo_Busqueda_Binaria:
                                #BOTON 16 : Volver al inicio
                                #Asigno Rojo, Azul, y Gris como corresponda
                                lista_colores = [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, VC]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                time.sleep(0.11)
                                thread.funcion = 0
                                self.Pantalla_principal.emit()
                                
                                lista_colores = [R, R, A, A, R, R, A, A, R, R, A, A, R, R, A, A]
                                self.lista_con_colores_teclado.emit(lista_colores)
                                
                                lista_booleanos = [False]*16
                                self.lista_con_booleanos_teclado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_bloqueado.emit(lista_booleanos)
                                self.lista_con_booleanos_teclado_predictivo.emit(lista_booleanos)


                                return

            time.sleep(0.1)                      
            ####Actualizo los caracteres####
            
            self.CargarTexto.emit()
            while 1:
                palabraIncompleta = q.get()
                if type(palabraIncompleta) == str:
                    palabraIncompleta = palabraIncompleta.lower()
                    break
            
            if palabraIncompleta == '' or palabraIncompleta == ' ' or palabraIncompleta == '  ' or (palabraIncompleta[len(palabraIncompleta) - 1] == " "):

                if palabraIncompleta != '' and palabraIncompleta != ' ' and palabraIncompleta != '  ':
                    split = palabraIncompleta.split('')

                    palabraAgregar = str(split[-2])
                    if len(palabraAgregar) > 0:#Este if está al pedo porque si len=0 entra al if anterior pero bueno
                        #Hagamos de cuenta que selecciono esta palabra, para "aprender" que el usuario usa mucho esto y sugerirla mas seguido. Recordar guardar al final.
                        SelectWord(palabraAgregar)
                    print(palabraAgregar)
                if ActualizarCaracteres:
                    letterOrderFirstPrediction = letterOrderLastPrediction
                    letterOrderLastPrediction = letterOrderLastPrediction + numberOfLettersToPredictEachTime
                    ActualizarCaracteres = False 

                    lista_palabras = lista_todas_palabras[letterOrderFirstPrediction:letterOrderFirstPrediction + 5]
                    lista_caracteres = lista_todos_caracteres[letterOrderFirstPrediction:letterOrderLastPrediction]
                    if letterOrderLastPrediction == 27:
                        lista_caracteres = lista_todos_caracteres[letterOrderFirstPrediction:]

                elif palabraIncompleta == '':
                    lista_caracteres = ['E','A','O','S','R','N','I','D','L']
                
                else:
                    lista_caracteres = ['e', 'a' , 'o', 's', 'r', 'n', 'i', 'd', 'l']
        
            else:

                if ActualizarCaracteres:
                    letterOrderFirstPrediction = letterOrderLastPrediction
                    letterOrderLastPrediction = letterOrderLastPrediction + numberOfLettersToPredictEachTime
                    ActualizarCaracteres = False  

                
                else:
                    letterOrderFirstPrediction = 0
                    letterOrderLastPrediction = numberOfLettersToPredictEachTime
                    lista_todas_palabras = NextMostProbableWords(palabraIncompleta, defaultTrieWordSearchDepth)
                    lista_todos_caracteres = NextMostProbableLetters(palabraIncompleta, 24)

                lista_palabras = lista_todas_palabras[letterOrderFirstPrediction:letterOrderFirstPrediction + 5]
                lista_caracteres = lista_todos_caracteres[letterOrderFirstPrediction:letterOrderLastPrediction]
        
            
            
            self.lista_con_caracteres_tecladocomun.emit(lista_caracteres)
            self.lista_con_caracteres_tecladobloqueado.emit(lista_caracteres)
            self.lista_con_caracteres_tecladopredictivo.emit(lista_caracteres)

            self.lista_con_palabras_tecladocomun.emit(lista_palabras)
            self.lista_con_palabras_tecladobloqueado.emit(lista_palabras)
            self.lista_con_palabras_tecladopredictivo.emit(lista_palabras)
                    
            if bloquear:                    
                self.Teclado_bloqueado.emit()
                guiño = q.get() #Espera hasta recibir un guiño
        return

    def SeleccionFrases(self):


        R = 'rgb(255,0,0)'
        A = 'rgb(0,0,255)'
        G = 'rgb(127,127,160)'
        VO = 'rgb(0,127,0)'
        VC = 'rgb(0,255,0)'
        


        T = True
        F = False

        t = np.linspace(0,7*Tiempo_Busqueda_Lineal, num = 8)

        self.Frases_bloqueada.emit()
        time.sleep(1.5)

        while not q.empty():
            guiño = q.get()     #Si se guiñó mientras la pantalla estaba bloqueada, agarro los guiños y los desecho

        guiño = False

        lista_colores = [R, R, R, R, R, R, R, A, A, A, A, A, A, A]
        self.lista_con_colores_frases.emit(lista_colores)


        self.Frases.emit()
        
        #Primera Selección: Binaria
        t0 = timer()
        while 1:
            t1 = timer()

            if not q.empty():
                guiño = q.get()

            if guiño:
                guiño1 = True
                lista_colores = [VO, VO, VO, VO, VO, VO, VO, G, G, G, G, G, G, G]
                self.lista_con_colores_frases.emit(lista_colores)
                break
            elif (t1-t0)>2:
                guiño1 = False
                lista_colores = [G, G, G, G, G, G, G, VO, VO, VO, VO, VO, VO, VO]
                self.lista_con_colores_frases.emit(lista_colores)
                break

        #Segunda Selección: Lineal
        t0 = timer()
        guiño = False
        if guiño1:
            lista_colores = [VC, VO, VO, VO, VO, VO, VO, G, G, G, G, G, G, G]
            self.lista_con_colores_frases.emit(lista_colores)
        else:
            lista_colores = [G, G, G, G, G, G, G, VC, VO, VO, VO, VO, VO, VO]
            self.lista_con_colores_frases.emit(lista_colores)

        NuncaEntre2 = True
        NuncaEntre3 = True
        NuncaEntre4 = True
        NuncaEntre5 = True
        NuncaEntre6 = True
        NuncaEntre7 = True

        while 1:
            t1 = timer()

            if not q.empty():
                guiño = q.get()

            if guiño1:

                if guiño and t[0]<(t1-t0)<t[1]:
                    #Elegir la primera frase
                    lista_booleanos = [T,F,F,F,F,F,F,F,F,F,F]
                    self.lista_con_booleanos_frases.emit(lista_booleanos)
                    break
                
                if t[1]<(t1-t0) and NuncaEntre2:
                    lista_colores = [VO, VC, VO, VO, VO, VO, VO, G, G, G, G, G, G, G]
                    self.lista_con_colores_frases.emit(lista_colores)
                    NuncaEntre2 = False

                if guiño and t[1]<(t1-t0)<t[2]:
                    #Elegir la segunda frase
                    lista_booleanos = [F,T,F,F,F,F,F,F,F,F,F]
                    self.lista_con_booleanos_frases.emit(lista_booleanos)
                    break
                
                if t[2]<(t1-t0) and NuncaEntre3:
                    lista_colores = [VO, VO, VC, VO, VO, VO, VO, G, G, G, G, G, G, G]
                    self.lista_con_colores_frases.emit(lista_colores)
                    NuncaEntre3 = False


                if guiño and t[2]<(t1-t0)<t[3]:
                    #Elegir la tercera frase
                    lista_booleanos = [F,F,T,F,F,F,F,F,F,F,F]
                    self.lista_con_booleanos_frases.emit(lista_booleanos)
                    break
            
                if t[3]<(t1-t0) and NuncaEntre4:
                    lista_colores = [VO, VO, VO, VC, VO, VO, VO, G, G, G, G, G, G, G]
                    self.lista_con_colores_frases.emit(lista_colores)
                    NuncaEntre4 = False

                if guiño and t[3]<(t1-t0)<t[4]:
                    #Elegir la cuarta frase
                    lista_booleanos = [F,F,F,T,F,F,F,F,F,F,F]
                    self.lista_con_booleanos_frases.emit(lista_booleanos)
                    break
                
                if t[4]<(t1-t0) and NuncaEntre5:
                    lista_colores = [VO, VO, VO, VO, VC, VO, VO, G, G, G, G, G, G, G]
                    self.lista_con_colores_frases.emit(lista_colores)
                    NuncaEntre5 = False


                if guiño and t[4]<(t1-t0)<t[5]:
                    #Elegir la quinta frase
                    lista_booleanos = [F,F,F,F,T,F,F,F,F,F,F]
                    self.lista_con_booleanos_frases.emit(lista_booleanos)
                    break
                
                if t[5]<(t1-t0) and NuncaEntre6:
                    lista_colores = [VO, VO, VO, VO, VO, VC, VO, G, G, G, G, G, G, G]
                    self.lista_con_colores_frases.emit(lista_colores)
                    NuncaEntre6 = False


                if guiño and t[5]<(t1-t0)<t[6]:
                    #Elegir la sexta frase
                    lista_booleanos = [F,F,F,F,F,T,F,F,F,F,F]
                    self.lista_con_booleanos_frases.emit(lista_booleanos)
                    break

                if t[6]<(t1-t0) and NuncaEntre7:
                    lista_colores = [VO, VO, VO, VO, VO, VO, VC, G, G, G, G, G, G, G]
                    self.lista_con_colores_frases.emit(lista_colores)
                    NuncaEntre7 = False


                if guiño and t[6]<(t1-t0)<t[7]:
                    #Ir a la pestaña de Configuración
                    thread.funcion = 4
                    return
                
                if (t1-t0)>t[7]:
                    break

            else:

                if guiño and t[0]<(t1-t0)<t[1]:
                    #Elegir la octava frase
                    lista_booleanos = [F,F,F,F,F,F,T,F,F,F,F]
                    self.lista_con_booleanos_frases.emit(lista_booleanos)
                    break
                
                if t[1]<(t1-t0) and NuncaEntre2:
                    lista_colores = [G, G, G, G, G, G, G, VO, VC, VO, VO, VO, VO, VO]
                    self.lista_con_colores_frases.emit(lista_colores)
                    NuncaEntre2 =  False

                if guiño and t[1]<(t1-t0)<t[2]:
                    #Elegir la novena frase
                    lista_booleanos = [F,F,F,F,F,F,F,T,F,F,F]
                    self.lista_con_booleanos_frases.emit(lista_booleanos)
                    break
                
                if t[2]<(t1-t0) and NuncaEntre3:
                    lista_colores = [G, G, G, G, G, G, G, VO, VO, VC, VO, VO, VO, VO]
                    self.lista_con_colores_frases.emit(lista_colores)
                    NuncaEntre3 = False

                if guiño and t[2]<(t1-t0)<t[3]:
                    #Elegir la decima frase
                    lista_booleanos = [F,F,F,F,F,F,F,F,T,F,F]
                    self.lista_con_booleanos_frases.emit(lista_booleanos)
                    break
            
                if t[3]<(t1-t0) and NuncaEntre4:
                    lista_colores = [G, G, G, G, G, G, G, VO, VO, VO, VC, VO, VO, VO]
                    self.lista_con_colores_frases.emit(lista_colores)
                    NuncaEntre4 = False

                if guiño and t[3]<(t1-t0)<t[4]:
                    #Elegir la onceava frase
                    lista_booleanos = [F,F,F,F,F,F,F,F,F,T,F]
                    self.lista_con_booleanos_frases.emit(lista_booleanos)
                    break
                
                if t[4]<(t1-t0) and NuncaEntre5:
                    lista_colores = [G, G, G, G, G, G, G, VO, VO, VO, VO, VC, VO, VO]
                    self.lista_con_colores_frases.emit(lista_colores)
                    NuncaEntre5 = False

                if guiño and t[4]<(t1-t0)<t[5]:
                    #Elegir la doceava frase
                    lista_booleanos = [F,F,F,F,F,F,F,F,F,F,T]
                    self.lista_con_booleanos_frases.emit(lista_booleanos)
                    break
                
                if t[5]<(t1-t0) and NuncaEntre6:
                    lista_colores = [G, G, G, G, G, G, G, VO, VO, VO, VO, VO, VC, VO]
                    self.lista_con_colores_frases.emit(lista_colores)
                    NuncaEntre6 = False

                if guiño and t[5]<(t1-t0)<t[6]:
                    #Elegir ir al teclado
                    thread.funcion = 2
                    self.Teclado.emit()


                    ##Ya que no se esta viendo la pantalla de frases, seteo los colores iniciales para que la proxima vez no se inicie con los colores verdes
                    lista_colores = [R, R, R, R, R, R, R, A, A, A, A, A, A, A]
                    self.lista_con_colores_frases.emit(lista_colores)
                    return


                if t[6]<(t1-t0) and NuncaEntre7:
                    lista_colores = [G, G, G, G, G, G, G, VO, VO, VO, VO, VO, VO, VC]
                    self.lista_con_colores_frases.emit(lista_colores)
                    NuncaEntre7 = False

                if guiño and t[6]<(t1-t0)<t[7]:
                    #Elegir volver a la pantalla de inicio
                    thread.funcion = 0
                    self.Pantalla_principal.emit()

                    ##Ya que no se esta viendo la pantalla de frases, seteo los colores iniciales para que la proxima vez no se inicie con los colores verdes
                    lista_colores = [R, R, R, R, R, R, R, A, A, A, A, A, A, A]
                    self.lista_con_colores_frases.emit(lista_colores)
                    return
                
                if (t1-t0)>t[7]:
                    break

        if guiño:   #Si guiñó, tomo la frase elegida y la muestro en las pantallas del teclado
            frase = q.get()
        
            self.MostrarFraseEnTeclado.emit(frase)
            self.MostrarFraseEnTecladoBloqueado.emit(frase)
            self.MostrarFraseEnTecladoPredictivo.emit(frase)

            thread.funcion = 2
            self.Teclado.emit()
            return
        else:
            thread.funcion = 2
            self.Teclado.emit()


            ##Ya que no se esta viendo la pantalla de frases, seteo los colores iniciales para que la proxima vez no se inicie con los colores verdes
            lista_colores = [R, R, R, R, R, R, R, A, A, A, A, A, A, A]
            self.lista_con_colores_frases.emit(lista_colores)
            return

    def SeleccionPalabra(self):
        
        VO = 'rgb(0,127,0)'
        VC = 'rgb(0,255,0)'
        lista_colores = [VO,VO,VO,VO,VO]
        self.lista_con_colores_predictivo.emit(lista_colores)
        time.sleep(2)
        
        while not q.empty():
            guiño = q.get()     #Si se guiñó mientras la pantalla estaba bloqueada, agarro los guiños y los desecho

        T = True
        F = False


        guiño = False

        lista_colores = [VC,VO,VO,VO,VO]
        self.lista_con_colores_predictivo.emit(lista_colores)

        #Segunda Lineal
        t0 = timer()
        guiño = False
    
        NuncaEntre2 = True
        NuncaEntre3 = True
        NuncaEntre4 = True
        NuncaEntre5 = True

        t = np.linspace(0,7*Tiempo_Busqueda_Lineal, num = 6)

        while 1:
            t1 = timer()

            if not q.empty():
                guiño = q.get()
        

            if guiño and t[0]<(t1-t0)<t[1]:
                #Elegir la primera palabra
                lista_booleanos = [T,F,F,F,F]
                self.lista_con_booleanos_predictivo_tecladocomun.emit(lista_booleanos)
                self.lista_con_booleanos_predictivo_tecladobloqueado.emit(lista_booleanos)
                self.lista_con_booleanos_predictivo_tecladopredictivo.emit(lista_booleanos)
                break
            
            if t[1]<(t1-t0) and NuncaEntre2:
                lista_colores = [VO, VC, VO, VO, VO]
                self.lista_con_colores_predictivo.emit(lista_colores)
                NuncaEntre2 = False

            if guiño and t[1]<(t1-t0)<t[2]:
                #Elegir la segunda palabra
                lista_booleanos = [F,T,F,F,F]
                self.lista_con_booleanos_predictivo_tecladocomun.emit(lista_booleanos)
                self.lista_con_booleanos_predictivo_tecladobloqueado.emit(lista_booleanos)
                self.lista_con_booleanos_predictivo_tecladopredictivo.emit(lista_booleanos)
                break
            
            if t[2]<(t1-t0) and NuncaEntre3:
                lista_colores = [VO, VO, VC, VO, VO]
                self.lista_con_colores_predictivo.emit(lista_colores)
                NuncaEntre3 = False

            if guiño and t[2]<(t1-t0)<t[3]:
                #Elegir la tercera palabra
                lista_booleanos = [F,F,T,F,F]
                self.lista_con_booleanos_predictivo_tecladocomun.emit(lista_booleanos)
                self.lista_con_booleanos_predictivo_tecladobloqueado.emit(lista_booleanos)
                self.lista_con_booleanos_predictivo_tecladopredictivo.emit(lista_booleanos)
                break
        
            if t[3]<(t1-t0) and NuncaEntre4:
                lista_colores = [VO, VO, VO, VC, VO]
                self.lista_con_colores_predictivo.emit(lista_colores)
                NuncaEntre4 = False

            if guiño and t[3]<(t1-t0)<t[4]:
                #Elegir la cuarta palabra
                lista_booleanos = [F,F,F,T,F]
                self.lista_con_booleanos_predictivo_tecladocomun.emit(lista_booleanos)
                self.lista_con_booleanos_predictivo_tecladobloqueado.emit(lista_booleanos)
                self.lista_con_booleanos_predictivo_tecladopredictivo.emit(lista_booleanos)
                break
            
            if t[4]<(t1-t0) and NuncaEntre5:
                lista_colores = [VO, VO, VO, VO, VC]
                self.lista_con_colores_predictivo.emit(lista_colores)
                NuncaEntre5 = False

            if guiño and t[4]<(t1-t0)<t[5]:
                #Elegir la quinta palabra
                lista_booleanos = [F,F,F,F,T]
                self.lista_con_booleanos_predictivo_tecladocomun.emit(lista_booleanos)
                self.lista_con_booleanos_predictivo_tecladobloqueado.emit(lista_booleanos)
                self.lista_con_booleanos_predictivo_tecladopredictivo.emit(lista_booleanos)
                break

            if (t1-t0)>t[5]:
                break
        time.sleep(0.1)    
        
        thread.funcion = 2
        self.Teclado_bloqueado.emit()
        lista_colores = [VC,VO,VO,VO,VO]
        self.lista_con_colores_predictivo.emit(lista_colores)

        return

    def Configuracion(self):
              
        T = True
        F = False
        t = [0,1.5,3,4.5,6,7.5]
        
        self.Config_bloqueada.emit()
        time.sleep(1.5)

        while not q.empty():
            guiño = q.get()     #Si se guiñó mientras la pantalla estaba bloqueada, agarro los guiños y los desecho

        guiño = False
        self.Config.emit()
        t0 = timer()        
        

        NuncaEntre1 = True
        NuncaEntre2 = True
        NuncaEntre3 = True
        NuncaEntre4 = True

        while 1:
            t1 = timer()
            if not q.empty():
                guiño = q.get()

            
            if (t1-t0) < t[1]:      #Selección tiempos búsqueda binaria
                if NuncaEntre1:
                    NuncaEntre1 = False
                    lista_bool = [T,F,F,F]
                    self.lista_con_booleanos_config.emit(lista_bool)

                if guiño:      #Selección tiempos búsqueda binaria
                    #Ejecuto función de moverse entre tiempos de busqueda binaria
                    thread.modo = 1
                    thread.funcion = 5
                    return

            if t[1] < (t1-t0) < t[2]:   #Selección tiempos búsqueda lineal
                if NuncaEntre2:
                    NuncaEntre2 = False
                    lista_bool = [F,T,F,F]
                    self.lista_con_booleanos_config.emit(lista_bool)

                if guiño:
                    #Ejecuto función de moverse entre tiempos de busqueda lineal
                    thread.modo = 2
                    thread.funcion = 5
                    return

            if t[2] < (t1-t0) < t[3]:   #Selección idiomas
                if NuncaEntre3:   
                    NuncaEntre3 = False
                    lista_bool = [F,F,T,F] 
                    self.lista_con_booleanos_config.emit(lista_bool)
                
                if guiño:     
                     #Ejecuto función de moverse entre tiempos de busqueda binaria
                    thread.modo = 3
                    thread.funcion = 5
                    return

            if t[3] < (t1-t0) < t[4]:   #Volver a Frases
                if NuncaEntre4:
                    NuncaEntre4 = False
                    lista_bool = [F,F,F,T]
                    self.lista_con_booleanos_config.emit(lista_bool)

                if guiño: 
                    thread.funcion = 1
                    return  
            
            elif t[4] < (t1-t0):
                thread.funcion = 0
                return
     
        return

    def SeleccionOpcionesConfiguracion(self,Modo):

        VO = 'rgb(0,127,0)'
        VC = 'rgb(0,255,0)'

        t0 = timer()
        guiño = False
    
        NuncaEntre1 = True
        NuncaEntre2 = True
        NuncaEntre3 = True
        NuncaEntre4 = True
        NuncaEntre5 = True

        t = [0,1,2,3,4,5]

        global Tiempo_Busqueda_Binaria
        global Tiempo_Busqueda_Lineal
        global Idioma
        global dictDeTriesPorLetra
        global dictDePalabrasYFrecuencias
        global abecedario
        global lista_actual
        while 1:
            t1 = timer()

            if not q.empty():
                guiño = q.get()
        

            if (t1-t0)<t[1]:
                if NuncaEntre1:
                    lista_colores = [Modo,VC,VO,VO,VO,VO]
                    self.lista_colores_seleccion_config.emit(lista_colores)
                    NuncaEntre1 = False
                if guiño:
                    if Modo == 1:
                        Tiempo_Busqueda_Binaria = 0.75
                    elif Modo == 2:
                        Tiempo_Busqueda_Lineal = 0.75
                    else:
                        Idioma = 'es'
                        SaveCurrentDictionary(lista_actual)
                        lista_actual = 'lista-español-copia.txt'
                        dictDeTriesPorLetra = {}
                        dictDePalabrasYFrecuencias = {}
                        abecedario='abcdefghijklmnñopqrstuvwxyz'
                        OpenExistingDictionaryWithFrequencies(lista_actual,abecedario)
                        #Se Setea el lenguaje a Español
                        CambiarTodo('español')        
                    break
            
            if t[1]<(t1-t0)<t[2]:
                if NuncaEntre2:
                    lista_colores = [Modo,VO,VC,VO,VO,VO]
                    self.lista_colores_seleccion_config.emit(lista_colores)
                    NuncaEntre2 = False
                if guiño:
                    if Modo == 1:
                        Tiempo_Busqueda_Binaria = 1
                    elif Modo == 2:
                        Tiempo_Busqueda_Lineal = 1                                        
                    else:
                        Idioma = 'en'
                        SaveCurrentDictionary(lista_actual)
                        lista_actual = 'lista-ingles-copia.txt'
                        dictDeTriesPorLetra = {}
                        dictDePalabrasYFrecuencias = {}
                        abecedario='abcdefghijklmnñopqrstuvwxyz'
                        OpenExistingDictionaryWithFrequencies(lista_actual,abecedario)
                        CambiarTodo('ingles')
                        
                    break

            if t[2]<(t1-t0)<t[3]:
                if NuncaEntre3:    
                    lista_colores = [Modo,VO,VO,VC,VO,VO]
                    self.lista_colores_seleccion_config.emit(lista_colores)
                    NuncaEntre3 = False
                if guiño:
                    if Modo == 1:
                        Tiempo_Busqueda_Binaria = 1.25
                    elif Modo == 2:
                        Tiempo_Busqueda_Lineal = 1.25
                    else:
                        #Se Setea el lenguaje a Alemán
                        Idioma='de'
                        SaveCurrentDictionary(lista_actual)
                        lista_actual = 'lista-aleman-copia.txt' 
                        dictDeTriesPorLetra = {}
                        dictDePalabrasYFrecuencias = {}
                        abecedario='abcdefghijklmnopqrstuvwxyzäëïöü'
                        OpenExistingDictionaryWithFrequencies(lista_actual,abecedario)
                        CambiarTodo('aleman')  
                    break
            
            if t[3]<(t1-t0)<t[4]:
                if NuncaEntre4:    
                    lista_colores = [Modo,VO,VO,VO,VC,VO]
                    self.lista_colores_seleccion_config.emit(lista_colores)
                    NuncaEntre4 = False
                if guiño:
                    if Modo == 1:
                        Tiempo_Busqueda_Binaria = 1.5
                    elif Modo == 2:
                        Tiempo_Busqueda_Lineal = 1.5
                    else:
                        Idioma = 'it'
                        SaveCurrentDictionary(lista_actual)
                        lista_actual = 'lista-italiano-copia.txt'
                        dictDeTriesPorLetra = {}
                        dictDePalabrasYFrecuencias = {}                        
                        abecedario='abcdefghijklmnopqrstuvwxyzè'
                        OpenExistingDictionaryWithFrequencies(lista_actual,abecedario)                     
                        CambiarTodo('italiano')
                    break
            
            if t[4]<(t1-t0)<t[5]:
                if NuncaEntre5:
                    lista_colores = [Modo,VO,VO,VO,VO,VC]
                    self.lista_colores_seleccion_config.emit(lista_colores)
                    NuncaEntre5 = False

                if guiño:
                    if Modo == 1:
                        Tiempo_Busqueda_Binaria = 2
                    elif Modo == 2:
                        Tiempo_Busqueda_Lineal = 2
                    else:
                        #Se Setea el lenguaje a Francés
                        Idioma = 'fr'
                        SaveCurrentDictionary(lista_actual)
                        lista_actual = 'lista-frances-copia.txt'
                        dictDeTriesPorLetra = {}
                        dictDePalabrasYFrecuencias = {}                        
                        abecedario='abcdefghijklmnñopqrstuvwxyzâêôîèéçàœ'
                        OpenExistingDictionaryWithFrequencies(lista_actual,abecedario)                    
                        CambiarTodo('frances')
                    break
            
            if (t1-t0)>t[5]:
                break
        
        time.sleep(0.1)        
        thread.funcion = 0





class PantallaPrincipal(QDialog):
    def __init__(self):
        super(PantallaPrincipal,self).__init__()    #Adjudico a esta clase atributos y métodos de la clase QDialog
        loadUi('Inicio.ui',self)
        self.botonguino.clicked.connect(self.Guino)

    def Guino(self):
        elemento = True
        q.put(elemento)
        return    

    def MostrarPestana(self):
        widget.setCurrentIndex(0)
        
        return
   
class FrasesHechas(QDialog):
    def __init__(self):
        super(FrasesHechas,self).__init__()     #Adjudico a esta clase atributos y métodos de la clase QDialog
        loadUi('Frases.ui',self)  
        self.botonguino.clicked.connect(self.Guino)

    def Guino(self):
        elemento = True
        q.put(elemento)
        return 

    def MostrarPestana(self):
        widget.setCurrentIndex(1)

        return

    def CambiarColorFrases(self, lista):
        
        str1 = 'color:white; background-color:'+lista[0]+';font: 16pt "Verdana";border-radius: 3px;'
        self.frase1.setStyleSheet(str1)

        str2 = 'color:white; background-color:'+lista[1]+';font: 16pt "Verdana";border-radius: 3px;'
        self.frase2.setStyleSheet(str2)

        str3 = 'color:white; background-color:'+lista[2]+';font: 16pt "Verdana";border-radius: 3px;'
        self.frase3.setStyleSheet(str3)

        str4 = 'color:white; background-color:'+lista[3]+';font: 16pt "Verdana";border-radius: 3px;'
        self.frase4.setStyleSheet(str4)

        str5 = 'color:white; background-color:'+lista[4]+';font: 16pt "Verdana";border-radius: 3px;'
        self.frase5.setStyleSheet(str5)

        str6 = 'color:white; background-color:'+lista[5]+';font: 16pt "Verdana";border-radius: 3px;'
        self.frase6.setStyleSheet(str6)

        str7 = 'color:white; background-color:'+lista[6]+';font: 16pt "Verdana";border-radius: 3px;'
        self.frase7.setStyleSheet(str7)

        str8 = 'color:white; background-color:'+lista[7]+';font: 16pt "Verdana";border-radius: 3px;'
        self.frase8.setStyleSheet(str8)

        str9 = 'color:white; background-color:'+lista[8]+';font: 16pt "Verdana";border-radius: 3px;'
        self.frase9.setStyleSheet(str9)

        str10 = 'color:white; background-color:'+lista[9]+';font: 16pt "Verdana";border-radius: 3px;'
        self.frase10.setStyleSheet(str10)

        str11 = 'color:white; background-color:'+lista[10]+';font: 16pt "Verdana";border-radius: 3px;'
        self.frase11.setStyleSheet(str11)

        str12 = 'color:white; background-color:'+lista[11]+';font: 16pt "Verdana";border-radius: 3px;'
        self.frase12.setStyleSheet(str12)

        str13 = 'color:white; background-color:'+lista[12]+';font: 16pt "Verdana";border-radius: 3px;'
        self.IrTeclado_2.setStyleSheet(str13)

        str14 = 'color:white; background-color:'+lista[13]+';font: 16pt "Verdana";border-radius: 3px'
        self.VolverInicio_2.setStyleSheet(str14)

        return
    
    def CambiarFrase(self,lista):

        if lista[0]:
            txt = self.frase1.text()
        elif lista[1]:
            txt = self.frase2.text()
        elif lista[2]:
            txt = self.frase3.text()
        elif lista[3]:
            txt = self.frase4.text()
        elif lista[4]:
            txt = self.frase5.text()
        elif lista[5]:
            txt = self.frase6.text()
        elif lista[6]:
            txt = self.frase8.text()
        elif lista[7]:
            txt = self.frase9.text()
        elif lista[8]:
            txt = self.frase10.text()
        elif lista[9]:
            txt = self.frase11.text()
        elif lista[10]:
            txt = self.frase12.text()

        
        q.put(txt)
        return

class Teclado(QDialog):
    def __init__(self):
        super(Teclado,self).__init__()     #Adjudico a esta clase atributos y métodos de la clase QDialog
        loadUi('Teclado.ui',self)
        self.botonguino.clicked.connect(self.Guino)

    def Guino(self):
        elemento = True
        q.put(elemento)
        return 
  
    def MostrarPestana(self):
        widget.setCurrentIndex(2)
        
        R = 'rgb(255,0,0)'
        A = 'rgb(0,0,255)'
       

        lista_colores = [R, R, A, A, R, R, A, A, R, R, A, A, R, R, A, A]
        self.CambiarColor(lista_colores)


        return

    def CambiarColor(self, lista):
        
        str1 = 'font: 16pt "Verdana"; color: rgb(255, 255, 255); background-color: '+lista[0]+'; border-color: rgb(170, 0, 0);border-radius: 3px;'
        self.c1.setStyleSheet(str1)

        str2 = 'font: 16pt "Verdana"; color: rgb(255, 255, 255); background-color: '+lista[1]+'; border-color: rgb(170, 0, 0);border-radius: 3px;'
        self.c2.setStyleSheet(str2)

        str3 = 'font: 16pt "Verdana"; color: rgb(255, 255, 255); background-color: '+lista[2]+'; border-color: rgb(170, 0, 0);border-radius: 3px;'
        self.c3.setStyleSheet(str3)

        str4 = 'font: 8pt "Verdana"; color: rgb(255, 255, 255); background-color: '+lista[3]+'; border-color: rgb(170, 0, 0);border-radius: 3px;'
        self.c4.setStyleSheet(str4)

        str5 = 'font: 16pt "Verdana"; color: rgb(255, 255, 255); background-color: '+lista[4]+'; border-color: rgb(170, 0, 0);border-radius: 3px;'
        self.c5.setStyleSheet(str5)

        str6 = 'font: 16pt "Verdana"; color: rgb(255, 255, 255); background-color: '+lista[5]+'; border-color: rgb(170, 0, 0);border-radius: 3px;'
        self.c6.setStyleSheet(str6)

        str7 = 'font: 16pt "Verdana"; color: rgb(255, 255, 255); background-color: '+lista[6]+'; border-color: rgb(170, 0, 0);border-radius: 3px;'
        self.c7.setStyleSheet(str7)

        str8 = 'font: 7pt "Verdana"; color: rgb(255, 255, 255); background-color: '+lista[7]+'; border-color: rgb(170, 0, 0);border-radius: 3px;'
        self.c8.setStyleSheet(str8)

        str9 = 'font: 16pt "Verdana"; color: rgb(255, 255, 255); background-color: '+lista[8]+'; border-color: rgb(170, 0, 0);border-radius: 3px;'
        self.c9.setStyleSheet(str9)

        str10 = 'font: 16pt "Verdana"; color: rgb(255, 255, 255); background-color: '+lista[9]+'; border-color: rgb(170, 0, 0);border-radius: 3px;'
        self.c10.setStyleSheet(str10)

        str11 = 'font: 16pt "Verdana"; color: rgb(255, 255, 255); background-color: '+lista[10]+'; border-color: rgb(170, 0, 0);border-radius: 3px;'
        self.c11.setStyleSheet(str11)

        str12 = 'font: 7pt "Verdana"; color: rgb(255, 255, 255); background-color: '+lista[11]+'; border-color: rgb(170, 0, 0);border-radius: 3px;'
        self.c12.setStyleSheet(str12)

        str13 = 'font: 8pt "Verdana"; color: rgb(255, 255, 255); background-color: '+lista[12]+'; border-color: rgb(170, 0, 0);border-radius: 3px;'
        self.c13.setStyleSheet(str13)

        str14 = 'font: 7pt "Verdana"; color: rgb(255, 255, 255); background-color: '+lista[13]+'; border-color: rgb(170, 0, 0);border-radius: 3px;'
        self.c14.setStyleSheet(str14)

        str15 = 'font: 8pt "Verdana"; color: rgb(255, 255, 255); background-color: '+lista[14]+'; border-color: rgb(170, 0, 0);border-radius: 3px;'
        self.c15.setStyleSheet(str15)

        str16 = 'font: 8pt "Verdana"; color: rgb(255, 255, 255); background-color: '+lista[15]+'; border-color: rgb(170, 0, 0);border-radius: 3px;'
        self.c16.setStyleSheet(str16)

        time.sleep(0.1)

        return

    def CambiarTexto(self,lista, texto_actual = None):
        if texto_actual == None:
            txt1 = self.texto.text()
        else:
            txt1 = texto_actual
        txt2 = ''
        if lista[0]:
            txt2 = self.c1.text()
        elif lista[1]:
            txt2 = self.c2.text()
        elif lista[2]:
            txt2 = self.c3.text()
        elif lista[4]:
            txt2 = self.c5.text()
        elif lista[5]:
            txt2 = self.c6.text()
        elif lista[6]:
            txt2 = self.c7.text()
        elif lista[8]:
            txt2 = self.c9.text()
        elif lista[9]:
            txt2 = self.c10.text()
        elif lista[10]:
            txt2 = self.c11.text()
        elif lista[13]:
            txt2 = ' '
        elif lista[14]:
            txt = txt1[:-1]
            self.texto.setText(txt)
            return
        else:
            txt1 = ''
            txt2 = ''
        
        txt = txt1 + txt2
        self.texto.setText(txt)
        return

    def MostrarFraseEnTeclado(self,frase):
        self.texto.setText(frase)
        return

    def CambiarTextoPalabra(self,lista, texto_actual = None):
        if texto_actual == None:
            txt1 = self.texto.text()
        else:
            txt1 = texto_actual
        
        lista_txt = txt1.split(' ')[:-1]
        txt1 = ' '.join(lista_txt) + ' '
 
        txt2 = ''
        if lista[0]:
            txt2 = self.palabra1.text()
        elif lista[1]:
            txt2 = self.palabra2.text()
        elif lista[2]:
            txt2 = self.palabra3.text()
        elif lista[3]:
            txt2 = self.palabra4.text()
        elif lista[4]:
            txt2 = self.palabra5.text()
        
        txt = txt1 + txt2
        self.texto.setText(txt)
        
        return

    ## Esta función agrega los caracteres que hagan falta
    ## También acomoda los caracteres o las palabras en caso de que ya estén en los botones
    def ActualizarCaract(self,lista_chars):
        
        lista_chars_frec = ['e', 'a' , 'o', 's', 'r', 'n', 'i', 'd', 'l', 'c', 't', 'u', 'm', 'p', 'b', 'g', 'v', 'y', 'q', 'h', 'f', 'z', 'j', 'ñ', 'x', 'k', 'w']        

        ind = 0
        while len(lista_chars)<9:
            if lista_chars_frec[ind] not in lista_chars:
                lista_chars.append(lista_chars_frec[ind])
            ind = ind + 1

        lista_acond = ['']*9 
        
        for element in lista_chars:
            comp = element
            i = lista_chars.index(element)
            if comp == self.c1.text():
                lista_acond[0] = lista_chars.pop(i)
            if comp == self.c2.text():
                lista_acond[1] = lista_chars.pop(i)
            if comp == self.c3.text():
                lista_acond[2] = lista_chars.pop(i)
            if comp == self.c5.text():
                lista_acond[3] = lista_chars.pop(i)
            if comp == self.c6.text():
                lista_acond[4] = lista_chars.pop(i)
            if comp == self.c7.text():
                lista_acond[5] = lista_chars.pop(i)
            if comp == self.c9.text():
                lista_acond[6] = lista_chars.pop(i)
            if comp == self.c10.text():
                lista_acond[7] = lista_chars.pop(i)
            if comp == self.c11.text():
                lista_acond[8] = lista_chars.pop(i)
        
        
        for element in lista_acond:
            i = lista_acond.index(element)
            if element == '':
                lista_acond[i] = lista_chars.pop(0)
        
        self.c1.setText(lista_acond[0])
        self.c2.setText(lista_acond[1])
        self.c3.setText(lista_acond[2])
        self.c5.setText(lista_acond[3])
        self.c6.setText(lista_acond[4])
        self.c7.setText(lista_acond[5])
        self.c9.setText(lista_acond[6])
        self.c10.setText(lista_acond[7])
        self.c11.setText(lista_acond[8])

    def ActualizarPalabras(self,lista_words):
        lista_acond = ['']*5
        
        for element in lista_words:
            comp = element
            i = lista_words.index(element)
            if comp == self.palabra1.text():
                lista_acond[0] = lista_words.pop(i)
            if comp == self.palabra2.text():
                lista_acond[1] = lista_words.pop(i)
            if comp == self.palabra3.text():
                lista_acond[2] = lista_words.pop(i)
            if comp == self.palabra4.text():
                lista_acond[3] = lista_words.pop(i)
            if comp == self.palabra5.text():
                lista_acond[4] = lista_words.pop(i)

        for i in range(len(lista_words)):
            if lista_acond[i] == '':
                lista_acond[i] = lista_words.pop(0)
        for i in range(len(lista_acond)):
            if lista_acond[i] == '':
                lista_acond.pop(i)
                lista_acond.append('')

        self.palabra1.setText(lista_acond[0])
        self.palabra2.setText(lista_acond[1])
        self.palabra3.setText(lista_acond[2])
        self.palabra4.setText(lista_acond[3])
        self.palabra5.setText(lista_acond[4])

        return

    def CargarTexto(self):
        texto = self.texto.text()
        
        if texto == '':
            q.put('')
        
        elif texto[-1] == ' ':
            q.put(' ')
        else:
            texto = texto.split(' ')[-1]
            q.put(texto)

class PantallaPrincipalBloqueada(QDialog):
    def __init__(self):
        super(PantallaPrincipalBloqueada,self).__init__()    #Adjudico a esta clase atributos y métodos de la clase QDialog
        loadUi('InicioBloqueado.ui',self)
        self.botonguino.clicked.connect(self.Guino)

    def Guino(self):
        elemento = True
        q.put(elemento)
        return 
  

    def MostrarPestana(self):
        widget.setCurrentIndex(3)

class FrasesHechasBloqueada(QDialog):
    def __init__(self):
        super(FrasesHechasBloqueada,self).__init__()    #Adjudico a esta clase atributos y métodos de la clase QDialog
        loadUi('FrasesBloqueado.ui',self)
        self.botonguino.clicked.connect(self.Guino)

    def Guino(self):
        elemento = True
        q.put(elemento)
        return 
  
    
    def MostrarPestana(self):
        widget.setCurrentIndex(4)

class TecladoBloqueado(QDialog):
    def __init__(self):
        super(TecladoBloqueado,self).__init__()    #Adjudico a esta clase atributos y métodos de la clase QDialog
        loadUi('TecladoBloqueado.ui',self)   
        self.botonguino.clicked.connect(self.Guino)

    def Guino(self):
        elemento = True
        q.put(elemento)
        return 
  
    def MostrarPestana(self):
        widget.setCurrentIndex(5)

    def CambiarTexto(self,lista, texto_actual = None):
        if texto_actual == None:
            txt1 = self.texto.text()
        else:
            txt1 = texto_actual
        txt2 = ''
        if lista[0]:
            txt2 = self.c1.text()
        elif lista[1]:
            txt2 = self.c2.text()
        elif lista[2]:
            txt2 = self.c3.text()
        elif lista[4]:
            txt2 = self.c5.text()
        elif lista[5]:
            txt2 = self.c6.text()
        elif lista[6]:
            txt2 = self.c7.text()
        elif lista[8]:
            txt2 = self.c9.text()
        elif lista[9]:
            txt2 = self.c10.text()
        elif lista[10]:
            txt2 = self.c11.text()
        elif lista[13]:
            txt2 = ' '
        elif lista[14]:
            txt = txt1[:-1]
            self.texto.setText(txt)
            return
        else:
            txt1 = ''
            txt2 = ''
        
        txt = txt1 + txt2
        self.texto.setText(txt)
        return

    def MostrarFraseEnTeclado(self,frase):
        self.texto.setText(frase)
        return
  
  
    def CambiarTextoPalabra(self,lista, texto_actual = None):
        if texto_actual == None:
            txt1 = self.texto.text()
        else:
            txt1 = texto_actual
        
        lista_txt = txt1.split(' ')[:-1]
        txt1 = ' '.join(lista_txt) + ' '
 
        txt2 = ''
        if lista[0]:
            txt2 = self.palabra1.text()
        elif lista[1]:
            txt2 = self.palabra2.text()
        elif lista[2]:
            txt2 = self.palabra3.text()
        elif lista[3]:
            txt2 = self.palabra4.text()
        elif lista[4]:
            txt2 = self.palabra5.text()
        
        txt = txt1 + txt2
        self.texto.setText(txt)
        
        return

    ## Esta función agrega los caracteres que hagan falta
    ## También acomoda los caracteres o las palabras en caso de que ya estén en los botones
    def ActualizarCaract(self,lista_chars):
        
        lista_chars_frec = ['e', 'a' , 'o', 's', 'r', 'n', 'i', 'd', 'l', 'c', 't', 'u', 'm', 'p', 'b', 'g', 'v', 'y', 'q', 'h', 'f', 'z', 'j', 'ñ', 'x', 'k', 'w']        
        ind = 0
        while len(lista_chars)<9:
            if lista_chars_frec[ind] not in lista_chars:
                lista_chars.append(lista_chars_frec[ind])
            ind = ind + 1


        lista_acond = ['']*9

        for element in lista_chars:
            comp = element
            i = lista_chars.index(element)
            if comp == self.c1.text():
                lista_acond[0] = lista_chars.pop(i)
            if comp == self.c2.text():
                lista_acond[1] = lista_chars.pop(i)
            if comp == self.c3.text():
                lista_acond[2] = lista_chars.pop(i)
            if comp == self.c5.text():
                lista_acond[3] = lista_chars.pop(i)
            if comp == self.c6.text():
                lista_acond[4] = lista_chars.pop(i)
            if comp == self.c7.text():
                lista_acond[5] = lista_chars.pop(i)
            if comp == self.c9.text():
                lista_acond[6] = lista_chars.pop(i)
            if comp == self.c10.text():
                lista_acond[7] = lista_chars.pop(i)
            if comp == self.c11.text():
                lista_acond[8] = lista_chars.pop(i)
        
        
        for element in lista_acond:
            i = lista_acond.index(element)
            if element == '':
                lista_acond[i] = lista_chars.pop(0)
        
        self.c1.setText(lista_acond[0])
        self.c2.setText(lista_acond[1])
        self.c3.setText(lista_acond[2])
        self.c5.setText(lista_acond[3])
        self.c6.setText(lista_acond[4])
        self.c7.setText(lista_acond[5])
        self.c9.setText(lista_acond[6])
        self.c10.setText(lista_acond[7])
        self.c11.setText(lista_acond[8])
    
    def ActualizarPalabras(self,lista_words):
        lista_acond = ['']*5
        
        for element in lista_words:
            comp = element
            i = lista_words.index(element)
            if comp == self.palabra1.text():
                lista_acond[0] = lista_words.pop(i)
            if comp == self.palabra2.text():
                lista_acond[1] = lista_words.pop(i)
            if comp == self.palabra3.text():
                lista_acond[2] = lista_words.pop(i)
            if comp == self.palabra4.text():
                lista_acond[3] = lista_words.pop(i)
            if comp == self.palabra5.text():
                lista_acond[4] = lista_words.pop(i)


        for i in range(len(lista_words)):
            if lista_acond[i] == '':
                lista_acond[i] = lista_words.pop(0)

        self.palabra1.setText(lista_acond[0])
        self.palabra2.setText(lista_acond[1])
        self.palabra3.setText(lista_acond[2])
        self.palabra4.setText(lista_acond[3])
        self.palabra5.setText(lista_acond[4])

        return

class TecladoPredictivo(QDialog):
    def __init__(self):
        super(TecladoPredictivo,self).__init__()    #Adjudico a esta clase atributos y métodos de la clase QDialog
        loadUi('TecladoPredictivo.ui',self)
        self.botonguino.clicked.connect(self.Guino)

    def Guino(self):
        elemento = True
        q.put(elemento)
        return 
  
    
    def MostrarPestana(self):
        widget.setCurrentIndex(6)

    def MostrarFraseEnTeclado(self,frase):
        self.texto.setText(frase)
        return
    
    def CambiarTexto(self,lista, texto_actual = None):
        if texto_actual == None:
            txt1 = self.texto.text()
        else:
            txt1 = texto_actual
        txt2 = ''
        if lista[0]:
            txt2 = self.c1.text()
        elif lista[1]:
            txt2 = self.c2.text()
        elif lista[2]:
            txt2 = self.c3.text()
        elif lista[4]:
            txt2 = self.c5.text()
        elif lista[5]:
            txt2 = self.c6.text()
        elif lista[6]:
            txt2 = self.c7.text()
        elif lista[8]:
            txt2 = self.c9.text()
        elif lista[9]:
            txt2 = self.c10.text()
        elif lista[10]:
            txt2 = self.c11.text()
        elif lista[13]:
            txt2 = ' '
        elif lista[14]:
            txt = txt1[:-1]
            self.texto.setText(txt)
            return
        else:
            txt1 = ''
            txt2 = ''
        
        txt = txt1 + txt2
        self.texto.setText(txt)
        return

    ##AGREGUÉ ESTA FUNCIÓN PARA CAMBIAR ENTRE LAS DISTINTAS PALABRAS
    def CambiarPalabraPredictivo(self,lista):
        str1 = 'background-color: '+lista[0]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
        self.palabra1.setStyleSheet(str1)

        str2 = 'background-color: '+lista[1]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
        self.palabra2.setStyleSheet(str2)

        str3 = 'background-color: '+lista[2]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
        self.palabra3.setStyleSheet(str3)

        str4 = 'background-color: '+lista[3]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
        self.palabra4.setStyleSheet(str4)

        str5 = 'background-color: '+lista[4]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
        self.palabra5.setStyleSheet(str5)
        return

    
    def CambiarTextoPalabra(self,lista, texto_actual = None):
        if texto_actual == None:
            txt1 = self.texto.text()
        else:
            txt1 = texto_actual
        
        lista_txt = txt1.split(' ')[:-1]
        txt1 = ' '.join(lista_txt) + ' '
 
        txt2 = ''
        if lista[0]:
            txt2 = self.palabra1.text()
        elif lista[1]:
            txt2 = self.palabra2.text()
        elif lista[2]:
            txt2 = self.palabra3.text()
        elif lista[3]:
            txt2 = self.palabra4.text()
        elif lista[4]:
            txt2 = self.palabra5.text()
        
        txt = txt1 + txt2
        self.texto.setText(txt)
        
        return

    ## Esta función agrega los caracteres que hagan falta
    ## También acomoda los caracteres o las palabras en caso de que ya estén en los botones
    def ActualizarCaract(self,lista_chars):
        
        lista_chars_frec = ['e', 'a' , 'o', 's', 'r', 'n', 'i', 'd', 'l', 'c', 't', 'u', 'm', 'p', 'b', 'g', 'v', 'y', 'q', 'h', 'f', 'z', 'j', 'ñ', 'x', 'k', 'w']        

        ind = 0
        while len(lista_chars)<9:
            if lista_chars_frec[ind] not in lista_chars:
                lista_chars.append(lista_chars_frec[ind])
            ind = ind + 1


        lista_acond = ['']*9

        for element in lista_chars:
            comp = element
            i = lista_chars.index(element)
            if comp == self.c1.text():
                lista_acond[0] = lista_chars.pop(i)
            if comp == self.c2.text():
                lista_acond[1] = lista_chars.pop(i)
            if comp == self.c3.text():
                lista_acond[2] = lista_chars.pop(i)
            if comp == self.c5.text():
                lista_acond[3] = lista_chars.pop(i)
            if comp == self.c6.text():
                lista_acond[4] = lista_chars.pop(i)
            if comp == self.c7.text():
                lista_acond[5] = lista_chars.pop(i)
            if comp == self.c9.text():
                lista_acond[6] = lista_chars.pop(i)
            if comp == self.c10.text():
                lista_acond[7] = lista_chars.pop(i)
            if comp == self.c11.text():
                lista_acond[8] = lista_chars.pop(i)
        
        
        for element in lista_acond:
            i = lista_acond.index(element)
            if element == '':
                lista_acond[i] = lista_chars.pop(0)
        
        self.c1.setText(lista_acond[0])
        self.c2.setText(lista_acond[1])
        self.c3.setText(lista_acond[2])
        self.c5.setText(lista_acond[3])
        self.c6.setText(lista_acond[4])
        self.c7.setText(lista_acond[5])
        self.c9.setText(lista_acond[6])
        self.c10.setText(lista_acond[7])
        self.c11.setText(lista_acond[8])

   
    def ActualizarPalabras(self,lista_words):
        lista_acond = ['']*5
        
        for element in lista_words:
            comp = element
            i = lista_words.index(element)
            if comp == self.palabra1.text():
                lista_acond[0] = lista_words.pop(i)
            if comp == self.palabra2.text():
                lista_acond[1] = lista_words.pop(i)
            if comp == self.palabra3.text():
                lista_acond[2] = lista_words.pop(i)
            if comp == self.palabra4.text():
                lista_acond[3] = lista_words.pop(i)
            if comp == self.palabra5.text():
                lista_acond[4] = lista_words.pop(i)

        for i in range(len(lista_words)):
            if lista_acond[i] == '':
                lista_acond[i] = lista_words.pop(0)

        self.palabra1.setText(lista_acond[0])
        self.palabra2.setText(lista_acond[1])
        self.palabra3.setText(lista_acond[2])
        self.palabra4.setText(lista_acond[3])
        self.palabra5.setText(lista_acond[4])

        return

class Configuracion(QDialog):
    def __init__(self):
        super(Configuracion, self).__init__()
        loadUi('Configuración.ui',self)
        self.botonguino.clicked.connect(self.Guino)

    def Guino(self):
        elemento = True
        q.put(elemento)
        return 
      
    def MostrarPestana(self):

        stylesheet_boxes = 'background-color: rgba(180, 220, 190, 180); border-radius: 5px;'
        self.BB0.setStyleSheet(stylesheet_boxes)
        self.BL0.setStyleSheet(stylesheet_boxes)
        self.I0.setStyleSheet(stylesheet_boxes)


        stylesheet = 'background-color: rgba(50, 200, 50, 150); color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
        self.BB1.setStyleSheet(stylesheet)
        self.BB2.setStyleSheet(stylesheet)
        self.BB3.setStyleSheet(stylesheet)
        self.BB4.setStyleSheet(stylesheet)
        self.BB5.setStyleSheet(stylesheet)
        self.BL1.setStyleSheet(stylesheet)
        self.BL2.setStyleSheet(stylesheet)
        self.BL3.setStyleSheet(stylesheet)
        self.BL4.setStyleSheet(stylesheet)
        self.BL5.setStyleSheet(stylesheet)
        self.I1.setStyleSheet(stylesheet)
        self.I2.setStyleSheet(stylesheet)
        self.I3.setStyleSheet(stylesheet)
        self.I4.setStyleSheet(stylesheet)
        self.I5.setStyleSheet(stylesheet)
        self.Volver.setStyleSheet(stylesheet)


        widget.setCurrentIndex(7)
        return

    def CambiarColores(self,lista):
        stylesheet_fondo = 'background-color: rgba(180, 220, 190, 180); border-radius: 5px;'
        stylesheet_botones = 'background-color: rgba(50, 200, 50, 150); color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
        
        stylesheet_fondo_seleccionactual = 'background-color: rgba(100, 255, 120, 190); border-radius: 5px;'
        stylesheet_botones_seleccionactual = 'background-color: rgb(0, 170, 0); color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
        
        self.BB0.setStyleSheet(stylesheet_fondo)
        self.BL0.setStyleSheet(stylesheet_fondo)
        self.I0.setStyleSheet(stylesheet_fondo)

        self.BB1.setStyleSheet(stylesheet_botones)
        self.BB2.setStyleSheet(stylesheet_botones)
        self.BB3.setStyleSheet(stylesheet_botones)
        self.BB4.setStyleSheet(stylesheet_botones)
        self.BB5.setStyleSheet(stylesheet_botones)
        
        self.BL1.setStyleSheet(stylesheet_botones)
        self.BL2.setStyleSheet(stylesheet_botones)
        self.BL3.setStyleSheet(stylesheet_botones)
        self.BL4.setStyleSheet(stylesheet_botones)
        self.BL5.setStyleSheet(stylesheet_botones)

        self.I1.setStyleSheet(stylesheet_botones)
        self.I2.setStyleSheet(stylesheet_botones)
        self.I3.setStyleSheet(stylesheet_botones)
        self.I4.setStyleSheet(stylesheet_botones)
        self.I5.setStyleSheet(stylesheet_botones)

        self.Volver.setStyleSheet(stylesheet_botones)

        if lista[0]:
            self.BB0.setStyleSheet(stylesheet_fondo_seleccionactual)

            self.BB1.setStyleSheet(stylesheet_botones_seleccionactual)
            self.BB2.setStyleSheet(stylesheet_botones_seleccionactual)
            self.BB3.setStyleSheet(stylesheet_botones_seleccionactual)
            self.BB4.setStyleSheet(stylesheet_botones_seleccionactual)
            self.BB5.setStyleSheet(stylesheet_botones_seleccionactual)
        
        elif lista[1]:
            self.BL0.setStyleSheet(stylesheet_fondo_seleccionactual)

            self.BL1.setStyleSheet(stylesheet_botones_seleccionactual)
            self.BL2.setStyleSheet(stylesheet_botones_seleccionactual)
            self.BL3.setStyleSheet(stylesheet_botones_seleccionactual)
            self.BL4.setStyleSheet(stylesheet_botones_seleccionactual)
            self.BL5.setStyleSheet(stylesheet_botones_seleccionactual)

        elif lista[2]:
            self.I0.setStyleSheet(stylesheet_fondo_seleccionactual)

            self.I1.setStyleSheet(stylesheet_botones_seleccionactual)
            self.I2.setStyleSheet(stylesheet_botones_seleccionactual)
            self.I3.setStyleSheet(stylesheet_botones_seleccionactual)
            self.I4.setStyleSheet(stylesheet_botones_seleccionactual)
            self.I5.setStyleSheet(stylesheet_botones_seleccionactual)

        elif lista[3]:
            self.Volver.setStyleSheet(stylesheet_botones_seleccionactual)

        return

    def SeleccionOpciones(self, lista):
        
        if lista[0] == 1:
            str1 = 'background-color:'+lista[1]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
            self.BB1.setStyleSheet(str1)

            str2 = 'background-color:'+lista[2]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
            self.BB2.setStyleSheet(str2)

            str3 = 'background-color:'+lista[3]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
            self.BB3.setStyleSheet(str3)

            str4 = 'background-color:'+lista[4]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
            self.BB4.setStyleSheet(str4)

            str5= 'background-color:'+lista[5]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
            self.BB5.setStyleSheet(str5)

        elif lista[0] == 2:

            str1 = 'background-color:'+lista[1]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
            self.BL1.setStyleSheet(str1)

            str2 = 'background-color:'+lista[2]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
            self.BL2.setStyleSheet(str2)

            str3 = 'background-color:'+lista[3]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
            self.BL3.setStyleSheet(str3)

            str4 = 'background-color:'+lista[4]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
            self.BL4.setStyleSheet(str4)

            str5= 'background-color:'+lista[5]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
            self.BL5.setStyleSheet(str5)

        elif lista[0] == 3:

            str1 = 'background-color:'+lista[1]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
            self.I1.setStyleSheet(str1)

            str2 = 'background-color:'+lista[2]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
            self.I2.setStyleSheet(str2)

            str3 = 'background-color:'+lista[3]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
            self.I3.setStyleSheet(str3)

            str4 = 'background-color:'+lista[4]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
            self.I4.setStyleSheet(str4)

            str5= 'background-color:'+lista[5]+'; color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
            self.I5.setStyleSheet(str5)
class ConfiguracionBloqueada(QDialog):
    def __init__(self):
        super(ConfiguracionBloqueada, self).__init__()
        loadUi('ConfiguraciónBloqueado.ui',self)    
    
    def MostrarPestana(self):
        
        stylesheet_boxes = 'background-color: rgba(180, 220, 190, 180); border-radius: 5px;'
        self.BB0.setStyleSheet(stylesheet_boxes)
        self.BL0.setStyleSheet(stylesheet_boxes)
        self.I0.setStyleSheet(stylesheet_boxes)


        stylesheet = 'background-color: rgba(50, 200, 50, 150); color: rgb(255, 255, 255); font: 12pt "Verdana"; border-radius: 3px;'
        self.BB1.setStyleSheet(stylesheet)
        self.BB2.setStyleSheet(stylesheet)
        self.BB3.setStyleSheet(stylesheet)
        self.BB4.setStyleSheet(stylesheet)
        self.BB5.setStyleSheet(stylesheet)
        self.BL1.setStyleSheet(stylesheet)
        self.BL2.setStyleSheet(stylesheet)
        self.BL3.setStyleSheet(stylesheet)
        self.BL4.setStyleSheet(stylesheet)
        self.BL5.setStyleSheet(stylesheet)
        self.I1.setStyleSheet(stylesheet)
        self.I2.setStyleSheet(stylesheet)
        self.I3.setStyleSheet(stylesheet)
        self.I4.setStyleSheet(stylesheet)
        self.I5.setStyleSheet(stylesheet)
        self.Volver.setStyleSheet(stylesheet)

        
        widget.setCurrentIndex(8)



        return

    
#Main



OpenExistingDictionaryWithFrequencies(lista_actual,abecedario)



#Creo una queue
q = queue.Queue(maxsize=10)

app = QApplication(sys.argv)
pantalla_principal = PantallaPrincipal()
frases = FrasesHechas()
teclado = Teclado()
pantalla_principal_bloqueada = PantallaPrincipalBloqueada()
frases_bloqueada = FrasesHechasBloqueada()
teclado_bloqueado = TecladoBloqueado()
teclado_predictivo = TecladoPredictivo()
configuracion = Configuracion()
configuracion_bloqueado = ConfiguracionBloqueada()

widget = QtWidgets.QStackedWidget()
widget.addWidget(pantalla_principal)    #index = 0
widget.addWidget(frases)                #index = 1
widget.addWidget(teclado)               #index = 2
widget.addWidget(pantalla_principal_bloqueada) #index = 3
widget.addWidget(frases_bloqueada)  #index = 4
widget.addWidget(teclado_bloqueado) #index = 5
widget.addWidget(teclado_predictivo) #index = 6
widget.addWidget(configuracion) #index = 7
widget.addWidget(configuracion_bloqueado) #index = 8
widget.setCurrentIndex(3)

widget.setFixedHeight(500)
widget.setFixedWidth(1000)
widget.show()   #Mostramos la interfaz


#Agrego el worker
#serialArduino = serial.Serial('COM3',9600) 
thread = AnotherThread()
worker = Worker()

#Los muevo a los threads en paralelo (el cual todavía no arrancó)
worker.moveToThread(thread)

#Comandos para mostrar las pantallas cuando corresponda
worker.Pantalla_principal.connect(pantalla_principal.MostrarPestana)
worker.Pantalla_principal_bloqueada.connect(pantalla_principal_bloqueada.MostrarPestana)
worker.Frases.connect(frases.MostrarPestana)
worker.Frases_bloqueada.connect(frases_bloqueada.MostrarPestana)
worker.Teclado.connect(teclado.MostrarPestana)
worker.Teclado_bloqueado.connect(teclado_bloqueado.MostrarPestana)
worker.Teclado_predictivo.connect(teclado_predictivo.MostrarPestana)
worker.Config.connect(configuracion.MostrarPestana)
worker.Config_bloqueada.connect(configuracion_bloqueado.MostrarPestana)

#Comandos para iniciar el cambio de colores y selección de caracteres
worker.lista_con_colores_teclado.connect(teclado.CambiarColor)
worker.lista_con_booleanos_teclado.connect(teclado.CambiarTexto)
worker.lista_con_colores_frases.connect(frases.CambiarColorFrases)
worker.lista_con_booleanos_frases.connect(frases.CambiarFrase)
worker.lista_con_booleanos_teclado_bloqueado.connect(teclado_bloqueado.CambiarTexto)
worker.lista_con_booleanos_teclado_predictivo.connect(teclado_predictivo.CambiarTexto)
worker.MostrarFraseEnTeclado.connect(teclado.MostrarFraseEnTeclado)
worker.MostrarFraseEnTecladoBloqueado.connect(teclado_bloqueado.MostrarFraseEnTeclado)
worker.MostrarFraseEnTecladoPredictivo.connect(teclado_predictivo.MostrarFraseEnTeclado)
worker.lista_con_colores_predictivo.connect(teclado_predictivo.CambiarPalabraPredictivo)
worker.lista_con_booleanos_predictivo_tecladocomun.connect(teclado.CambiarTextoPalabra)
worker.lista_con_booleanos_predictivo_tecladobloqueado.connect(teclado_bloqueado.CambiarTextoPalabra)
worker.lista_con_booleanos_predictivo_tecladopredictivo.connect(teclado_predictivo.CambiarTextoPalabra)
worker.lista_con_booleanos_config.connect(configuracion.CambiarColores)
worker.lista_colores_seleccion_config.connect(configuracion.SeleccionOpciones)

#Comandos para actualizar los caracteres y palabras
worker.CargarTexto.connect(teclado.CargarTexto)
worker.lista_con_caracteres_tecladocomun.connect(teclado.ActualizarCaract)
worker.lista_con_palabras_tecladocomun.connect(teclado.ActualizarPalabras)
worker.lista_con_caracteres_tecladobloqueado.connect(teclado_bloqueado.ActualizarCaract)
worker.lista_con_palabras_tecladobloqueado.connect(teclado_bloqueado.ActualizarPalabras)
worker.lista_con_caracteres_tecladopredictivo.connect(teclado_predictivo.ActualizarCaract)
worker.lista_con_palabras_tecladopredictivo.connect(teclado_predictivo.ActualizarPalabras)


#Inicio los procesos en paralelo
thread.start()

try:
    sys.exit(app.exec())
except:
    SaveCurrentDictionary(lista_actual)
    print("Saliendo")
