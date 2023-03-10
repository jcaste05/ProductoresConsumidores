# -*- coding: utf-8 -*-
"""
PRÁCTICA 1

JAVIER CASTELLANO SORIA

"""

from multiprocessing import Process, Manager
from multiprocessing import Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value
import random
from time import sleep

def delay(factor):
    sleep(random.random()/factor)


vueltas = 5
N_prods = 4



def consumer(result, sems_nonFull, sems_nonEmty, values):
      
    
    for s in sems_nonEmty: #Nos aseguramos de que todos han producido antes de entrar al bucle
        s.acquire()
       
        #LOOP
    while no_acabado(values): #Mientras no todos los elementos sean -1. Values no se modifica al no poder añadir los productores
        
        print('Consumidor va a coger datos  ', flush=True)
        values_copia = [v.value for v in values] #NOTA: mientras se hace la copia no se modifica values porque los productores podrán producir pero no podrán añadir el elemento producido a su respectivo buffer
        print(f'Estado de los almacenes: {values_copia}  ', flush=True)
        
        delay(5)
        
        min_d = min_pos_positive(values_copia) #Hallo la posición del mínimo positivo
        minim = values_copia[min_d]
        values[min_d].value = -2 #Una vez cogido el elemento actualizo a -2
        print(f'Consumidor ha cogido el dato del productor {min_d}.  ', flush=True)
        sems_nonFull[min_d].release() #Ahora permito que el productor del que hemos cogido el dato vuelva a añadir
        
        delay(5)
        print(f'Consumidor va a consumir {minim} del productor {min_d}  ', flush = True)
        result.append((minim,f'Productor {min_d}')) #Consumo
        print(f'Estado de la lista final: {result}  ', flush=True)
        
        sems_nonEmty[min_d].acquire() #Para la siguiente vuelta del bucle esperamos a que produzca el productor del que consumimos
        
    

def min_pos_positive(val):
    result=0
    while val[result]<0:
        
        result += 1
        
    primero_no_neg = result
    for j in range(primero_no_neg, N_prods):
        if val[j]>=0 and val[j]<val[result]:
            result = j
    return result
        

def no_acabado(values):
    
    for x in range(N_prods):
        if values[x].value != -1:
            return True
    return False
   
   

def producer(val, sem_nonFull, sem_nonEmpty):
    
    num_al = random.randint(0, 10)
    
    
    for _ in range(vueltas):
        
        print(f'{current_process().name} va a producir  ', flush = True)
        num_al = num_al + random.randint(1, 10) #Produce un número
        delay(5)
        print(f'{current_process().name} ha producido el número {num_al}  ', flush = True)
        sem_nonFull.acquire() #Espera a que no esté lleno
        print(f'{current_process().name} va a añadir el elemento y el estado de su almacen es {val.value}  ', flush = True)
        val.value = num_al #Añade el elemento producido
        delay(5)
        print(f'{current_process().name} ha añadido el elemento y el estado de su almacen es {val.value}  ', flush = True)
        sem_nonEmpty.release() #Ahora ya no está vacío
    
    #Tomamos -1 como la última producción
    sem_nonFull.acquire()
    print(f'{current_process().name} va a terminar y el estado de su almacen es {val.value}', flush = True)
    val.value = -1
    print(f'{current_process().name} ha terminado y el estado de su almacen es {val.value}', flush = True)
    sem_nonEmpty.release() 
       

def main():
    
    manager = Manager()
    result = manager.list()
    
    values = [ Value('i', -2) 
              for _ in range(N_prods)]
   
    sems_nonFull = [ Lock()  
                     for _ in range(N_prods)] #Un semáforo para cada productor
   
    sems_nonEmpty = [ Semaphore(0)
                     for _ in range(N_prods)]
   
    prodlst = [ Process(target=producer,
                        name=f'Productor_{i}',
                        args=(values[i], sems_nonFull[i], sems_nonEmpty[i]))
                for i in range(N_prods) ]
    
   
    consum = Process(target=consumer, name='consumidor', args=(result, sems_nonFull, sems_nonEmpty, values))
   
    prodlst.append(consum)
    
    for p in prodlst:
        p.start()
   
    for p in prodlst:
        p.join()
    
    print('La lista resultado es:')
    print(result)


if __name__ == "__main__":
    main()

