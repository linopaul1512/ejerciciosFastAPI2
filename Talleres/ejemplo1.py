import threading
import time

#función que se ejecutará de forma asincrona
def  saluda(nombre):
    #Espera 2 segundos
    time.sleep(2)
    print(f"Hola, {nombre}")


#Declaro un hilo de ejeución 
threadin_emails = threading.Thread(target=saluda, args=("Snake", ))

#Resto del código que se ejecutará mientras trancure el tiempo de espera
threadin_emails.start()
print("función para ejecutar")