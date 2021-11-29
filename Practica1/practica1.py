# ENUNCIADO PRÁCTICA 1 - BAÑO MIXTO:
# En un despacho de abogados trabajan 6 hombres y 6 mujeres donde existe un único baño mixto.
# En este, no pueden haber hombres y mujeres a la vez, de la misma forma, solo puede haber un 
# máximo de tres personas siempre. Van al baño dos veces durante la jornada laboral.

# La simulación debe ser con las herramientas de sincronización semáforos, binarios y/o contadores. 
# Mujeres y hombres son procesos concurrentes con un identificador del tipo cadena de carácteres. 
# Después de ir al baño dos veces los procesos acaban. 
# No debe existir inanición y debe haber intercalación de géneros.

# IMPORTACIONES
import threading
import time
import random

# VARIABLES FINALES
MAX_EN_BANYO = 3
HOMES = 6
DONES = 6 
PERSONES = HOMES + DONES
VEGADES_AL_BANY = 2

# SEMÁFOROS
semContadorDones = threading.Semaphore(3)  # explicar que hace cada semaforo
semContadorHomes = threading.Semaphore(3)  
semDones = threading.Semaphore(1) 
semHomes = threading.Semaphore(1) 
semBuit = threading.Semaphore(1)
semInan = threading.Semaphore(1)

# VARIABLES AUXILIARES
contadorHomes = 0
contadorDones = 0

# ARRAY DE NOMBRES
nomsHomes = ["GORI", "COSME", "JAUME", "DAMIA", "ANTONI", "BERNAT"]
nomsDones = ["AINA", "GERONIA", "CATALINA", "ELISABET", "JOANA", "FRANCESCA"]

# MÉTODO "RUN" DE MUJERES
def dona():
    global contadorDones

    # Se prepara para entrar a trabajar al despacho
    print("\t"+ threading.current_thread().name + " arriba al despatx")


    # Los dos accesos de los procesos "hilo" de las mujeres al baño
    for i in range(VEGADES_AL_BANY): 

        # Se pone a trabajar
        print("\t"+ threading.current_thread().name + " treballa")
        time.sleep(random.randint(5, 10) / 10000)
        
        semInan.acquire()

        # Comprueba que el baño está vacío y desocupado por el otro género
        semDones.acquire() 
        if contadorDones == 0:
            semBuit.acquire()
        contadorDones += 1
        semDones.release()

        semInan.release()

        #SECCIÓN CRÍTICA
        # Permite la entrada de un máximo de tres mujeres
        semContadorDones.acquire()
        # Incrementamos la correspondiente variable de control de mujeres dentro del baño,
        # además de imprimir el mensaje correspondiente
        semDones.acquire()
        print("\t" + threading.current_thread().name + " entra " + str(i+1) + "/2. Personas en el baño: ", contadorDones) 
        semDones.release()

        time.sleep(random.randint(5, 10) / 10000) # Se encuentra en el baño

        # Desbloqueamos la entrada de control de un máximo de tres mujeres
        semContadorDones.release()
        #FIN SECCIÓN CRÍTICA

        # Decrementamos la correspondiente variable de control de mujeres dentro del baño,
        # además de imprimir el mensaje correspondiente
        semDones.acquire()
        contadorDones -= 1
        print("\t" + threading.current_thread().name + " surt.")
        

        # Comprueba que el baño está vacío y lo desbloquea para el otro género
     
        if contadorDones == 0:
            print("***** El baño esta vacio")
            semBuit.release()
        semDones.release()
        time.sleep(random.randint(5, 10) / 10000)


    # Acaba de trabajar después de haber entrado dos veces al baño
    print("\t" + threading.current_thread().name + " acaba la feina")
    
# MÉTODO "RUN" DE HOMBRES
def home():
    global contadorHomes
    
    # Se prepara para entrar a trabajar al despacho
    print(threading.current_thread().name + " arriba al despatx")

    # Los dos accesos de los procesos "hilo" de los hombres al baño
    for i in range(VEGADES_AL_BANY): 

        # Se pone a trabajar
        print(threading.current_thread().name + " treballa")


        semInan.acquire()
        # Comprueba que el baño está vacío y desocupado por el otro género
        semHomes.acquire()
        if contadorHomes == 0:
            semBuit.acquire()
        contadorHomes += 1
        semHomes.release()

        semInan.release()

        # Permite la entrada de un máximo de tres hombres
        semContadorHomes.acquire()

        # Incrementamos la correspondiente variable de control de hombres dentro del baño,
        # además de imprimir el mensaje correspondiente
        semHomes.acquire()
        
        print(threading.current_thread().name + " entra " + str(i+1) + "/2. Personas en el baño: ", contadorHomes) 
        semHomes.release()

        time.sleep(random.randint(5, 10) / 10000) # Se encuentra en el baño

         # Desbloqueamos la entrada de control de un máximo de tres hombres
        semContadorHomes.release()

        # Decrementamos la correspondiente variable de control de hombres dentro del baño,
        # además de imprimir el mensaje correspondiente
        semHomes.acquire()
        contadorHomes -= 1
        print(threading.current_thread().name + " surt.")

        # Comprueba que el baño está vacío y lo desbloquea para el otro género

        if contadorHomes == 0:
            print("***** El baño esta vacio")
            semBuit.release()
        semHomes.release()


    # Acaba de trabajar después de haber entrado dos veces al baño
    print(threading.current_thread().name + " acaba la feina")

# PROGRAMA PRINCIPAL    
def main():
    global cont
    threads = []

    # Lanzamos los procesos "hilo" que serán los hombres
    for i in range(HOMES):
        t = threading.Thread(target=home, name=nomsHomes[i])
        threads.append(t)
        t.start()

    # Lanzamos los procesos "hilo" que serán las mujeres
    for i in range(DONES):
        t = threading.Thread(target=dona, name=nomsDones[i])
        threads.append(t)
        t.start()

    # Esperamos a que todos los procesos "hilo" terminen
    for t in threads:
        t.join()

    print("-----------------------------------------End-----------------------------------------")


# DECLARACIÓN PROGRAMA PRINCIPAL
if __name__ == "__main__":
    main()
