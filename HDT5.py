'''
Autor: José Pablo Santisteban Vargas
Clase: Algoritmos y estructuras de datos
Maestro: Moisés Alonso

'''
import simpy
import random


# setup del programa
slots_ram = 100 #slots de RAM
cant_procesos = 25 #cantidad de procesos a realizar  (optimizable)
intervalos = 10 #(optimizable)
tiempo_total = 0 #empieza por 0, despues se sumara
instrucc_ciclo = 3
op_ciclo = 1

# setup de ambiente
env = simpy.Environment() #Creando el ambiente de simulación
ram_inicial = simpy.Container(env, slots_ram, slots_ram)
nucleos = simpy.Resource(env, capacity=1) #cantidad de nucleos (optimizable).
