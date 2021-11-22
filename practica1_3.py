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

semContadorDones = threading.Semaphore(3) 
semContadorHomes = threading.Semaphore(3)  
semDones = threading.Semaphore(1) 
semHomes = threading.Semaphore(1) 
semBuit = threading.Semaphore(1)

contador = 0
nomsHomes = ["GORI", "COSME", "JAUME", "DAMIA", "ANTONI", "BERNAT"]
nomsDones = ["AINA", "GERONIA", "CATALINA", "ELISABET", "JOANA", "FRANCESCA"]

def dona():
    global contador
    semDones.acquire()
    threading.current_thread().name = nomsDones.pop()
    semDones.release()

    print("\t"+ threading.current_thread().name + " arriba al despatx")
    time.sleep(random.randint(5, 10) / 100) 

    for i in range(VEGADES_AL_BANY): 
        print("\t"+ threading.current_thread().name + " treballa")
        time.sleep(random.randint(5, 10) / 100) # esta trabajando

        semDones.acquire()  # sirve para proteger el contador de dones 
        
        if contador < 3:
            contador += 1
            print("\t" + threading.current_thread().name + " entra " + str(i+1) + "/2. Personas en el baño: ", contador) 
        semDones.release()
        

        # esta en el baño 
        time.sleep(random.randint(5, 10) / 100) # esta 

        semDones.acquire()
        contador -= 1
        print("\t" + threading.current_thread().name + " surt.")

        if contador == 0:
            print("***** El baño esta vacio")
        semDones.release()

        time.sleep(random.randint(5, 10) / 100) # esta trabajando
    print("\t" + threading.current_thread().name + " acaba la feina")
    

def home():
    global contador
    semHomes.acquire()
    threading.current_thread().name = nomsHomes.pop()
    semHomes.release()
    
    print(threading.current_thread().name + " arriba al despatx")
    time.sleep(random.randint(5, 10) / 100) 

    for i in range(VEGADES_AL_BANY): 
        print(threading.current_thread().name + " treballa")
        time.sleep(random.randint(5, 10) / 100) # esta trabajando
        

        semHomes.acquire()
        
        if contador <3:
            contador += 1
            print(threading.current_thread().name + " entra " + str(i+1) + "/2. Personas en el baño: ", contador) 
        semHomes.release()

        # esta en el baño 
        time.sleep(random.randint(5, 10) / 100) # esta 

        semHomes.acquire()
        contador -= 1
        print(threading.current_thread().name + " surt.")
        if contador == 0:
            print("***** El baño esta vacio")
        semHomes.release()


        time.sleep(random.randint(5, 10) / 100) # esta trabajando
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
