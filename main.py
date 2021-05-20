# piedra papel tijera, jugaremos con una letra R(piedra) P(papel) S(tijeras)
#  o salir(X)... guardar tras salir
# Ahora pueden jugar varios usuarios:
# nuestro diccionario tendra varios jugadores y cada uno su propia puntuacion
# por otra parte añadir  una parte "grafica"
import random
import json
import os
import time
# import curses
import asciiArt
from diccionario import tags
nombreCarpeta = "20210506_rockPaperScissor"
# funciona desde visualcodium
# nombreFichero = "./"+nombreCarpeta + "/leaderBoard.json"
# funciona desde linea de comandos
nombreFichero = "./save.json"

SAVE_ON_EXIT = True
SAVE_EACH_CYCLE = False

ESCAPE = "X"
VICTORIA = "V"
PERDIDA = "D"
EMPATE = "E"
iPOINTS = 0
iSTATS = 1
iVICTORIA = 0
iPERDIDA = 1
iEMPATE = 2
iTIEMPOTOTAL = 0
iINPUTBUENO = 1
iINPUTTOTAL = 2
victorias = 0
derrotas = 0
empates = 0


opciones = ["R", "P", "S", "L", "K", ESCAPE]
# opciones = ["R", "P", "S"]
superiores = [["R", "S"], ["R", "L"], ["P", "R"], ["P", "K"], ["S", "P"],
              ["S", "L"], ["K", "S"], ["K", "K"]]
# superiores = [ "RS", "PR", "SP"]
cadenaPregunta1 = tags["preguntaInicio"]
cadenaPregunta2 = tags["preguntaError"]
# cadenaPregunta1 = "Tiene cuatro opciones: R(piedra) P(papel) S(tijeras)"
# cadenaPregunta2 = "Opcion incorrecta, por favor, escoja R P S"


tablaPuntos = [victorias, derrotas, empates]


def entrada(inputTotales, inputBuenos):
    print(cadenaPregunta1)
    devolver = ""
    inputTotales = 0
    inputBuenos = 0
    while devolver not in opciones:
        devolver = input(tags["jugar"])
        # if devolver == "X":
        #   exit
        devolver = validar(devolver)
        if devolver not in opciones:
            print(cadenaPregunta2)
        inputTotales += 1
    inputBuenos += 1
    # arrayentrada = [jugadorM, currentTotalInput, currentSuccessInput]
    return (devolver, inputTotales, inputBuenos)


def validar(entrada):
    if entrada in opciones or str.capitalize(entrada) in opciones:
        return str.capitalize(entrada)
    else:
        return None


def aleatorio():
    # -2: 1 por empezar en 0 y otra por salir
    return opciones[random.randint(0, (len(opciones)-2))]


def comparar(jugador, maquina, compaList):
    # victoriaVariable = [jugador, maquina]
    # victoriaVariable = str(jugador) + str(maquina)
    if jugador == maquina:
        puntuar(EMPATE, compaList)
        return tags["empate"]
    elif [jugador, maquina] in superiores:
        puntuar(VICTORIA, compaList)
        return tags["ganas"]
    elif jugador == ESCAPE:
        return tags["sales"]
    else:
        puntuar(PERDIDA, compaList)
        return tags["pierdes"]


def traductor(opc):
    if opc == "R":
        return tags["piedra"]
    elif opc == "P":
        return tags["papel"]
    elif opc == "S":
        return tags["tijera"]
    elif opc == "L":
        return tags["lagarto"]
    elif opc == "K":
        return tags["spock"]
    elif opc == "X":
        return tags["salir"]


def salida(resultado, seleccionJugador, seleccionMaquina):
    # "resultado" : "{resultado}, la maquina jugo: {seleccionMaquina} y
    # tu jugaste {seleccionJugador}",
    salidaTagger = {
        "resultado": resultado,
        "seleccionMaquina": traductor(seleccionMaquina),
        "seleccionJugador": traductor(seleccionJugador)
    }
    if not seleccionJugador == ESCAPE:
        ventana(seleccionJugador, seleccionMaquina, salidaTagger)


def ventana(seleccionJugador, seleccionMaquina, salidaTagger):
    print(tags["resultado"].format(**(salidaTagger)))
    for linea in range(0, 6):
        print("                           "+asciiArt.printAsciiArt(
            seleccionMaquina, linea) + "\r" + asciiArt.printAsciiArt(
            seleccionJugador, linea))


def puntuar(tipo, listaPuntua):
    if tipo == VICTORIA:
        listaPuntua[iVICTORIA] += 1
    elif tipo == PERDIDA:
        listaPuntua[iPERDIDA] += 1
    else:
        listaPuntua[iEMPATE] += 1
    return listaPuntua


def cargarPartida(nombre):
    print(tags["cargo"])
    leaderBoardData = {}
    with open(nombreFichero) as leaderBoardFile:
        leaderBoardData = json.load(leaderBoardFile)
    nombres = leaderBoardData["nombres"]
    stats = leaderBoardData["stats"]
    tiempoEjecucion = stats["tiempoEjecucion"]
    inputsTotales = stats["inputsTotales"]
    inputsBuenos = stats["inputsBuenos"]
    if nombres.get(nombre) is None:
        primeraVez(nombre, False)
        # se devuelve la lista de puntuaciones y los stats
        return [[0, 0, 0], [tiempoEjecucion, inputsTotales, inputsBuenos]]
    else:
        leaderBoardDataUser = nombres[nombre]
        cargaVictoria = int(leaderBoardDataUser['ganadas'])
        cargaDerrota = int(leaderBoardDataUser['perdidas'])
        cargaEmpates = int(leaderBoardDataUser['empatadas'])
        return [[cargaVictoria, cargaDerrota, cargaEmpates],
                [tiempoEjecucion, inputsTotales, inputsBuenos]]


def salvarPartida(nombre, listaPuntosGuardar, listaStatsGuardar, partialTime):
    print(tags["guardo"])
    dictionaryPoints = {
        "empatadas": listaPuntosGuardar[iEMPATE],
        "ganadas": listaPuntosGuardar[iVICTORIA],
        "perdidas": listaPuntosGuardar[iPERDIDA]
    }
    dictionaryStats = {
        "tiempoEjecucion": listaStatsGuardar[iTIEMPOTOTAL],
        "inputsBuenos": listaStatsGuardar[iINPUTBUENO],
        "inputsTotales": listaStatsGuardar[iINPUTTOTAL]
        }
    if partialTime is not None:
        dictionaryStats["tiempoEjecucion"] += partialTime
    dictionary = {}
    with open(nombreFichero, 'r') as infile:
        dictionary = json.load(infile)
    dictionary["nombres"][nombre] = dictionaryPoints
    dictionary["stats"] = dictionaryStats
    with open(nombreFichero, 'w') as outfile:
        json.dump(dictionary, outfile)


def mostrarPuntuacion(lisPuntos):
    #     "puntuacion" : "V: {victorias}, E: {empates}, D: {derrotas}"
    puntuacionTagger = {
        "victorias": lisPuntos[iVICTORIA],
        "empates": lisPuntos[iEMPATE],
        "derrotas": lisPuntos[iPERDIDA]
    }
    print(tags["puntuacion"].format(**(puntuacionTagger)))


# inicializa el fichero (True) o al nuevo usuario (False)
def primeraVez(nombre, mode):
    """ mode == True inicializa archivo, mode == False inicializa jugador"""
    dictionary = {}
    dictionary["nombres"] = {
    }
    if mode:
        dictionary["stats"] = {
            "tiempoEjecucion": 0,
            "inputsBuenos": 0,
            "inputsTotales": 0
        }
    else:
        with open(nombreFichero, 'r') as infile:
            dictionary = json.load(infile)
    dictionary["nombres"][nombre] = {
        "empatadas": 0,
        "ganadas": 0,
        "perdidas": 0
    }
    with open(nombreFichero, 'w') as outfile:
        json.dump(dictionary, outfile)


def resumen(initialTime, stats, elapsedTime):
    gmTime = time.gmtime(initialTime)
    timestring = time.strftime("%H : %M : %S", gmTime)
    resumenTimeTagger = {
        "timeString": timestring,
        "elapsedTime": elapsedTime
    }
    resumenInputTagger = {
        "inputBuenos": stats[iINPUTBUENO],
        "inputTotales": stats[iINPUTTOTAL]
    }
    resumenTiempoFinalTagger = {
        "totalElapsedTime": int(stats[iTIEMPOTOTAL])
    }
    print(tags["resumen"].format(**(resumenTimeTagger)))
    print(tags["resumen2"].format(**(resumenInputTagger)))
    print(tags["resumen3"].format(**(resumenTiempoFinalTagger)))


def continuar():
    input(tags["continuar"])


def main():
    previousTime = 0
    startTime = time.time()
    # empezamos preguntando el nombre y luego creando el archivo si no existe
    usuario = input(tags["tuNombre"])
    if (not os.path.exists(nombreFichero)):
        primeraVez(usuario, True)
    tablaDatos = cargarPartida(usuario)
    tablaPuntos = tablaDatos[iPOINTS]
    tablaStats = tablaDatos[iSTATS]
    mostrarPuntuacion(tablaPuntos)
    jugadorM = ""
    elapsedTime = 0
    partialElapsedTime = 0
    currentTotalInput = 0
    currentSuccessInput = 0
    while not jugadorM == ESCAPE:
        currentTime = time.time()
        continuar()
        os.system("cls" if os.name == "nt" else "clear")
        # arrayentrada = [jugadorM, currentTotalInput, currentSuccessInput]
        arrayentrada = entrada(currentTotalInput, currentSuccessInput)
        jugadorM = arrayentrada[0]
        tablaStats[iINPUTTOTAL] += arrayentrada[1]
        tablaStats[iINPUTBUENO] += arrayentrada[2]
        maquinaM = aleatorio()
        resultadoM = comparar(jugadorM, maquinaM, tablaPuntos)
        salida(resultadoM, jugadorM, maquinaM)
        mostrarPuntuacion(tablaPuntos)
        partialElapsedTime = time.time() - currentTime
        elapsedTime = time.time() - startTime
        if SAVE_EACH_CYCLE:
            salvarPartida(usuario, tablaPuntos, tablaStats, elapsedTime)
    tablaStats[iTIEMPOTOTAL] += time.time() - startTime
    if SAVE_ON_EXIT:
        salvarPartida(usuario, tablaPuntos, tablaStats, None)
    resumen(startTime, tablaStats, elapsedTime)


main()
