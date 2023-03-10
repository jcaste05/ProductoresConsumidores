# -*- coding: utf-8 -*-
"""
PRÁCTICA 1 PARTE OPCIONAL

JAVIER CASTELLANO SORIA

"""

from multiprocessing import Process, Manager
from multiprocessing import Semaphore, BoundedSemaphore, Lock
from multiprocessing import current_process
import random
from time import sleep

def delay(factor):
    sleep(random.random()/factor)


vueltas = 5
N_prods = 3
CAP = 2

def take(values, pos_cons, mutex): #El take va a devolver directamente si han acabado o no de producir en la variable no_fin y si no ha acabado también devuelve el valor a consumir y su respectivo productor
    mutex.acquire()
    print('Consumidor va a coger el dato  ', flush=True)
    values_copia = []
    for x in range(N_prods):
        values_copia.append(values[x][pos_cons[x]])
    if no_acabado(values_copia):
        min_d = min_pos_positive(values_copia)
        minim = values_copia[min_d]
        values[min_d][pos_cons[min_d]] = -2
        print(f'Consumidor ha cogido el dato {minim} del productor {min_d}.  ', flush=True)
        mutex.release()
        return (min_d, minim, True)
    else:
        print('No se puede consumir más  ', flush = True)
        mutex.release()
        return (-1,-1,False)


def consumer(result, sems_nonFull, sems_nonEmty, values, mutex):
     
    pos_cons = [0]*N_prods #Lista de posiciones que alberga dónde debe consumir
    
    for s in sems_nonEmty: #Nos aseguramos de que todos han producido antes de entrar al bucle
        s.acquire()
    
    
    (min_d, minim, no_fin) = take(values, pos_cons, mutex) #Nos ayudamos de un Lock (mutex) para que al hacer el take no se esté modificando values
        #LOOP
    while no_fin: #Mientras no todos los elementos sean -1
        
        pos_cons[min_d] = (pos_cons[min_d]+1)%CAP
        
        sems_nonFull[min_d].release() #Ahora libero en una unidad el almacenamiento
        
        delay(5)
        print(f'Consumidor va a consumir {minim} del productor {min_d}  ', flush = True)
        result.append((minim,f'Productor {min_d}')) #Consumo
        print(f'Estado de la lista final: {result}  ', flush=True)
        
        sems_nonEmty[min_d].acquire() #Para la siguiente vuelta del bucle esperamos a que no esté vacío el buffer de donde hemos producido
        delay(3)
        
        (min_d, minim, no_fin) = take(values, pos_cons, mutex)
    

def min_pos_positive(val):
    
    
    result=0
    while val[result]<0:
        
        result += 1
        
    primero_no_neg = result
    for j in range(primero_no_neg, N_prods):
        if val[j]>=0 and val[j]<val[result]:
            result = j
    return result
        

def no_acabado(values_copia):
    
    for x in range(N_prods):
        if values_copia[x] != -1:
            return True
    return False
   
   

def producer(val, sem_nonFull, sem_nonEmpty, mutex):
    
    pos = 0 #Posición donde tendrá que producir
    num_al = random.randint(0, 10)
    
    
    for _ in range(vueltas):
        
        print(f'{current_process().name} va a producir  ', flush = True)
        num_al = num_al + random.randint(1, 10) #Produce un número
        delay(5)
        print(f'{current_process().name} ha producido el número {num_al}  ', flush = True)
        sem_nonFull.acquire() #Espera a que no esté lleno
        
        mutex.acquire()
        print(f'{current_process().name} va a añadir el elemento y el estado de su almacen es {val}  ', flush = True)
        val[pos] = num_al #Añade el elemento producido
        delay(5)
        print(f'{current_process().name} ha añadido el elemento y el estado de su almacen es {val}  ', flush = True)
        mutex.release()
        
        
        sem_nonEmpty.release() #Ahora ya no está vacío
        pos = (pos+1)%CAP
    
    #Tomamos -1 como la última producción
    sem_nonFull.acquire()
    
    
    mutex.acquire()
    print(f'{current_process().name} va a terminar y el estado de su almacen es {val}', flush = True)
    val[pos] = -1
    print(f'{current_process().name} ha terminado y el estado de su almacen es {val}', flush = True)
    mutex.release()
    
    
    sem_nonEmpty.release() 
       

def main():
    
    manager = Manager()
    result = manager.list()
    
    values = [ manager.list([-2]*CAP) 
              for _ in range(N_prods)]
   
    sems_nonFull = [ BoundedSemaphore(CAP)  
                     for _ in range(N_prods)] #Un semáforo para cada productor
   
    sems_nonEmpty = [ Semaphore(0)
                     for _ in range(N_prods)]
    
    mutex = Lock()
   
    prodlst = [ Process(target=producer,
                        name=f'Productor_{i}',
                        args=(values[i], sems_nonFull[i], sems_nonEmpty[i], mutex))
                for i in range(N_prods) ]
    
   
    consum = Process(target=consumer, name='consumidor', args=(result, sems_nonFull, sems_nonEmpty, values, mutex))
   
    prodlst.append(consum)
    
    for p in prodlst:
        p.start()
   
    for p in prodlst:
        p.join()
    
    print('La lista resultado es:')
    print(result)


if __name__ == "__main__":
    main()