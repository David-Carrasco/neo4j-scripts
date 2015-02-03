"""
Pregunta 3
Inicie el servidor con el dataset grahpDb anexo a la actividad.
El grafo almacenado es una parte de la red ferroviaria de los Estados Unidos. Contiene 133 753 nodos y 174 428 relaciones. 
Cada nodo puede ser interpretado como una estacion y cada relacion representa la via de tren que une directamente dos estaciones.
Las relaciones tienen una propiedad llamada STFIPS1 que representa el costo de transporte entre las dos estaciones.
 Esta propiedad es una cadena que contiene un numero entero.
Los nodos tienen una propiedad llamada prop_node_id que identifica las estaciones con un numero entero.
 Ademas, cada nodo tiene un par de propiedades (prop_latitude, prop_longitude) con las coordenadas de la estacion.
Escriba un programa en Python que reciba como parametros los identificadores enteros de dos nodos cualesquiera del grafo 
y devuelva el camino menos costoso entre ambos (aquel donde la suma de los costos de transporte sea menor).
Si no existiera un camino entre las estaciones, que se muestre un mensaje indicandolo.
Nota: Consideraremos que las vias se pueden recorrer en ambas direcciones.
Ejemplo de salidas:
$> python get-cheaper-path.py 13 12
Cheaper path: 13 - 24 - 12
$> python get-cheaper-path.py 15 16
There is no path
"""

# NODOS: Estaciones trenes 
#	- prop_node_id(int) --> Id
#	- prop_latitude(float) --> Coordenada latitud
#	- prop_longitude(float) --> Coordenada longitud

# RELACIONES: Vias
#	- STFIPS1(int): Peso entre 2 estaciones


import sys, re
from neo4jrestclient.client import GraphDatabase

db = GraphDatabase("http://localhost:7474/db/data/")

################ CHECK PARAMETROS #####################

if len(sys.argv) != 3:
	raise Exception('Introduzca exactamente 2 ids de estaciones')

for i in sys.argv[1:]:
	try:
		int(i)
	except Exception:
		raise Exception('Solo permitido valores enteros')

################ INICIO PROGRAMA #####################

#Constantes
id_start = int(sys.argv[1])
id_end = int(sys.argv[2])

#Comprobamos que los nodos existen con los ids introducidos
try:
 	start_Station = db.nodes[id_start]
 	end_Station = db.nodes[id_end]
except (Exception):
	raise Exception('Al menos uno de los 2 nodos introducidos no existe en la DB')

################ QUERY DB ############################

q = """
MATCH paths = allShortestPaths((n { prop_node_id : {start_id} })-[*]-(m { prop_node_id: {end_id} }))
WITH REDUCE(dist = 0, rel in rels(paths) | dist + toInt(rel.STFIPS1)) AS distance, paths
RETURN paths, distance
ORDER BY distance
LIMIT 1
"""
result = db.query(q, params={"start_id": id_start, "end_id": id_end})

################ RESULTADO ###########################

if len(result) == 0:
	print "There is no path"
else:
	#Obtenemos los nodos del camino de la estructura obtenida
	path = [re.search(r'\d+$', node).group(0) for node in result[0][0]['nodes']]
	print "Cheaper path: {path}".format(path = '-'.join(path))
