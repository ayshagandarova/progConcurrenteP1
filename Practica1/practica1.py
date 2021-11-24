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
VEGADES_AL_BANY = 2

#Semáforos
semContadorDones = threading.Semaphore(3) 
semContadorHomes = threading.Semaphore(3)  
semDones = threading.Semaphore(1) 
semHomes = threading.Semaphore(1) 
semBuit = threading.Semaphore(1)

contadorHomes = 0
contadorDones = 0

nomsHomes = ["GORI", "COSME", "JAUME", "DAMIA", "ANTONI", "BERNAT"]
nomsDones = ["AINA", "GERONIA", "CATALINA", "ELISABET", "JOANA", "FRANCESCA"]


def dona():
    global contadorDones
    semDones.acquire()
    threading.current_thread().name = nomsDones.pop()
    semDones.release()

    print("\t"+ threading.current_thread().name + " arriba al despatx")
    time.sleep(random.randint(5, 10) / 10000) 

    for i in range(VEGADES_AL_BANY): 
        print("\t"+ threading.current_thread().name + " treballa")
        time.sleep(random.randint(5, 10) / 100000) # esta trabajando

        semDones.acquire()  # sirve para proteger el contador de dones 
        if contadorDones == 0:
            semBuit.acquire()  # el baño esta ocupado por un género
        semDones.release()
        
        semContadorDones.acquire() # 3 recursos para 3 dones

        semDones.acquire()
        contadorDones += 1
        print("\t" + threading.current_thread().name + " entra " + str(i+1) + "/2. Personas en el baño: ", contadorDones) 
        semDones.release()

        # esta en el baño 
        time.sleep(random.randint(5, 10) / 10000) # esta 

        semDones.acquire()
        contadorDones -= 1
        print("\t" + threading.current_thread().name + " surt.")
        semDones.release()

        semContadorDones.release()

        semDones.acquire()
        if contadorDones == 0:
            print("***** El baño esta vacio")
            semBuit.release()
        semDones.release()

        time.sleep(random.randint(5, 10) / 1000) # esta trabajando
    print("\t" + threading.current_thread().name + " acaba la feina")
    

def home():
    global contadorHomes
    semHomes.acquire()
    threading.current_thread().name = nomsHomes.pop()
    semHomes.release()
    
    print(threading.current_thread().name + " arriba al despatx")
    time.sleep(random.randint(5, 10) / 1000) 

    for i in range(VEGADES_AL_BANY): 
        print(threading.current_thread().name + " treballa")
        time.sleep(random.randint(5, 10) / 1000) # esta trabajando
        

        semHomes.acquire()
        if contadorHomes == 0:
            semBuit.acquire()
        semHomes.release()


        semContadorHomes.acquire()
        semHomes.acquire()
        contadorHomes += 1
        print(threading.current_thread().name + " entra " + str(i+1) + "/2. Personas en el baño: ", contadorHomes) 
        semHomes.release()
        # esta en el baño 
        time.sleep(random.randint(5, 10) / 10000) # esta 

        semHomes.acquire()
        contadorHomes -= 1
        print(threading.current_thread().name + " surt.")
        semHomes.release()
        semContadorHomes.release()

        semHomes.acquire()
        if contadorHomes == 0:
            print("***** El baño esta vacio")
            semBuit.release()
        semHomes.release()

        time.sleep(random.randint(5, 10) / 1000) # esta trabajando
    print(threading.current_thread().name + " acaba la feina")
    
def main():
    global cont
    threads = []

    for i in range(HOMES):
        # Create new threads
        t = threading.Thread(target=home)
        threads.append(t)
        t.start() # start the thread

    for i in range(DONES):
        # Create new threads
        t = threading.Thread(target=dona)
        threads.append(t)
        t.start() # start the thread

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print("End")

if __name__ == "__main__":
    main()
