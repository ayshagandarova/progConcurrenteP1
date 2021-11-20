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

semDones = threading.Semaphore(1)  # empieza desbloqueado
semHomes = threading.Semaphore(1)  # empieza desbloquead
semBany = threading.Semaphore(3) # empieza desbloqueado
semPersonesBany = threading.Semaphore(1)
nomsHomes = ["GORI", "COSME", "JAUME", "DAMIA", "ANTONI", "BERNAT"]
nomsDones = ["AINA", "GERONIA", "CATALINA", "ELISABET", "JOANA", "FRANCESCA"]
personesBany = 0
cont = 0

def dona():
    contador = 0
    semDones.acquire()
    threading.current_thread().name = nomsDones.pop()
    semDones.release()

    print("\t"+ threading.current_thread().name + " arriba al despatx")
    time.sleep(random.randint(5, 10) / 100) 

    for i in range(VEGADES_AL_BANY): 
        print("\t"+ threading.current_thread().name + " treballa")
        time.sleep(random.randint(5, 10) / 100) # esta trabajando
        accedirAlBanyDona(i)
        time.sleep(random.randint(5, 10) / 100) # esta trabajando
    print("\t" + threading.current_thread().name + " acaba la feina")
    

def home():
    semHomes.acquire()
    threading.current_thread().name = nomsHomes.pop()
    semHomes.release()

    print(threading.current_thread().name + " arriba al despatx")
    time.sleep(random.randint(5, 10) / 100) 

    for i in range(VEGADES_AL_BANY): 
        print(threading.current_thread().name + " treballa")
        time.sleep(random.randint(5, 10) / 100) # esta trabajando
        accedirAlBanyHome(i)
        time.sleep(random.randint(5, 10) / 100) # esta trabajando
    print(threading.current_thread().name + " acaba la feina")
    
def accedirAlBanyDona(i):
    global personesBany
    global semDones, semBany, semHomes

    semHomes.acquire()
    if semBany == 3:  # si el baño esta vacio  (si deja pasar a 3 personas entonces empieza con 3, es decir, si ==3 es que está vacio el baño)
        semBany.acquire()  # esto ya bloquearia a los hombres en teoria 
        semDones.acquire()

    personesBany += 1
    print("\t" + threading.current_thread().name + " entra " + str(i+1) + "/2. Personas en el baño: ", personesBany) 
    semDones.release() # la mujer ha entrado al baño
    
    time.sleep(random.randint(5, 10) / 100) # esta en el baño

    semDones.acquire()
    personesBany -= 1      # la mujer sale del baño
    print("\t" + threading.current_thread().name + " surt.")
    if semBany == 3: # no hay nadie
        print("***** El baño esta vacio")
        semHomes.release()
        semBany.release()
    semDones.release()

def accedirAlBanyHome(i):
    global personesBany
    global semHomes, semBany, semDones

    semDones.acquire()
    if semBany == 3:  # si el baño esta vacio  (si deja pasar a 3 personas entonces empieza con 3, es decir, si ==3 es que está vacio el baño)
        semBany.acquire()  # esto ya bloquearia a los hombres en teoria 
        semHomes.acquire()

    personesBany += 1
    print(threading.current_thread().name + " entra " + str(i+1) + "/2. Personas en el baño: ", personesBany) 
    semHomes.release() # la mujer ha entrado al baño
    
    time.sleep(random.randint(5, 10) / 100) # esta en el baño

    semHomes.acquire()
    personesBany -= 1      # la mujer sale del baño
    print(threading.current_thread().name + " surt.")
    if semBany == 3: # no hay nadie
        print("***** El baño esta vacio")
        semDones.release()
        semBany.release()
    semHomes.release()

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
