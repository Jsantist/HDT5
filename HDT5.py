'''
Autor: José Pablo Santisteban Vargas
Clase: Algoritmos y estructuras de datos
Maestro: Moisés Alonso

'''
import simpy
import random


#Función para realizar procesos
def procesos(env, espera_inicio, nombre, cantidad_ram, cantidad_instrucciones, instrucciones_ciclo, operaciones_ciclo, ram_inicial, nucleos):
    estado = False #not terminated

    yield env.timeout(espera_inicio)
    start = env.now

    print("%s proceso en cola [NEW]. Tiempo: %d .  RAM requerida: %d .  RAM disponible: %d" % (nombre, env.now, cantidad_ram, ram_inicial.level))
    yield ram_inicial.get(cantidad_ram)
    print("%s proces en cola [READY] en tiempo %d. Cantidad de instrucciones pendientes %d" % (nombre, env.now, cantidad_instrucciones))


    while cantidad_instrucciones > 0:
        with nucleos.request() as req:
            yield req
            cantidad_instrucciones -= instrucciones_ciclo
            yield env.timeout(operaciones_ciclo) #ciclos cada operacion
            print("%s proces en cola [READY] en tiempo %d. Cantidad de instrucciones pendientes %d" % (nombre, env.now, cantidad_instrucciones))

        if cantidad_instrucciones > 0:
            evento_random = random.randint(1, 2)


    yield ram_inicial.put(cantidad_ram)
    global tiempo_total
    tiempo_total += env.now - start
    print("%s proceso [TERMINATED] en tiempo %d. Cantidad de RAM devuelta: %d. Cantidad de memoria disponible %d" % (nombre, env.now, cantidad_ram, ram_inicial.level))


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
