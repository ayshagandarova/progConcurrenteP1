# 6 dones i 6 homes i només hi ha un bany mixt6 dones i 6 homes i només hi ha un bany mixt
# Dins el bany no hi pot haver al mateix temps dones i homes
# Com a màxim hi pot haver 3 dones o 3 homes al mateix temps
# Durant la jornada laboral van al bany dues vegades
# semaforo contadoy y binario
# dones y homes son procesos concurrentes se’ls ha d’assignar un identificador que serà una cadena de caràcters . Després de sortir del bany la segona vegada els processos acaben.
#S’ha de garantir que no hi ha inanició (malgrat l’acabament dels processos) per això una simulació incorrecte seria per exemple que primer hi anessin totes les dones i després tots els homes (o a l’inrevés).
# 1. Llançar els processos i que acabin amb dos missatges d’inici i final
# 2. Accedir al bany amb exclusió mútua, només un procés a la vegada, control de bany buit
# 3. Programar els grups de 3 (homes i dones indiferents)
# 4. Separar homes de dones i manteniment dels comptadors
# 5. Ajustar simulació amb esperes i control de l’intercalat de missatg

import threading
import time
import random

MAX_EN_BANYO = 3
HOMES = 6
DONES = 6 
PERSONES = HOMES + DONES

semDones = threading.Semaphore(0)  # empieza desbloqueado
semHomes = threading.Semaphore(0)  # empieza desbloquead
semBany = threading.Semaphore(3) # empieza desbloqueado

nomsHomes = ["GORI", "COSME", "JAUME", "DAMIA", "ANTONI", "BERNAT"]
nomsDones = ["AINA", "GERONIA", "CATALINA", "ELISABET", "JOANA", "FRANCESCA"]
personesBany = 0

def dona(i):
    print("\t"+ nomsDones[i-6] + " arriba al despatx")
    threading.current_thread().name = nomsDones[i-6]
    accedirAlBany()
    print("\t" + threading.current_thread().name + "acaba la feina")


def home(i):
    print(nomsHomes[i] + " arriba al despatx")
    threading.current_thread().name = nomsHomes[i]
    accedirAlBany()
    print(threading.current_thread().name + "acaba la feina")
    
def accedirAlBany():
    global personesBany

    semBany.acquire()
    personesBany = personesBany + 1
    print(threading.current_thread().name + " entra. Personas en el baño: ", personesBany)
    time.sleep(random.randint(5, 10) / 100) 
    semBany.release()
    personesBany -=1

    if personesBany == 0:
        print("*****El baño esta vacio")



funcions = {0: home, 1: dona}

def main():
    threads = []

    func = funcions[0]

    for i in range(PERSONES):
        # Create new threads
        t = threading.Thread(target=func(i))
        threads.append(t)
        t.start() # start the thread
        if (i == 5):
            func = funcions[1]

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print("End")

if __name__ == "__main__":
    main()
