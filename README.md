# ProductoresConsumidores
SOBRE LOS ARCHIVOS:
- ProdsCon.py: Programa python con la librería multiprocessing donde se implementa un problema de productor-consumidor. Tenemos NPROD procesos que producen números no negativos de forma creciente y aleatoria. Cada proceso almacena el número producido en la variable compartida con el consumidor. El consumidor debe tomar los números producidos y almacenarlos de forma creciente en una única lista. Debe esperar a que todos los productores tengan listo un elemento e introducir el menor. En este caso, los productores solo pueden crear un elemento a lo sumo.
- ProdsConOpcional_V2.py: Programa python con librería multiprocessing igual que el anterior pero ahora los productores pueden producir más de un elemento almacenándolos en su buffer.
