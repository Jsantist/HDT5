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

    print("%s proceso en cola [NEW]. Tiempo: %d . RAM requerida: %d . RAM disponible: %d" % (nombre, env.now, cantidad_ram, ram_inicial.level))
    yield ram_inicial.get(cantidad_ram)
    print("%s proceso en cola [READY] en tiempo %d.  Instrucciones pendientes %d" % (nombre, env.now, cantidad_instrucciones))


    while cantidad_instrucciones > 0:
        with nucleos.request() as req:
            yield req
            cantidad_instrucciones -= instrucciones_ciclo
            yield env.timeout(operaciones_ciclo) #ciclos cada operacion
            print("%s procesO en cola [READY] en tiempo %d.  Instrucciones pendientes %d" % (nombre, env.now, cantidad_instrucciones))

        if cantidad_instrucciones > 0:
            evento_random = random.randint(1, 2)
            if evento_random == 1:
                #Cola waiting
                print("%s ha ingresado a la cola [WAITING]" % (nombre))
                yield env.timeout(random.randint(1, 5)) #tiempo en espera
            else:
                pass #regresa inmediatamente a la cola [RUNNING]

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

#repetición por cantidad de procesos 
for i in range(cant_procesos):
    espera_inicio = random.expovariate(1.0/10)
    cantidad_instrucciones = random.randint(1, 10)
    cantidad_ram = random.randint(1, 10)
    env.process(procesos(env=env, espera_inicio=espera_inicio, nombre="Proceso %d" % i, cantidad_ram=cantidad_ram, cantidad_instrucciones=cantidad_instrucciones, instrucciones_ciclo=instrucc_ciclo, operaciones_ciclo=op_ciclo, ram_inicial=ram_inicial, nucleos=nucleos))

env.run()
tiempo_promedio = tiempo_total/cant_procesos
print("tiempo promedio: %d" % (tiempo_promedio))