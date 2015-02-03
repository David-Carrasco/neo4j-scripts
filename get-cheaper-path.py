"""
Get shortest path between 2 nodes in the graphdb Train stations of US attached
"""

# NODES: Train stations
#	- prop_node_id(int) --> Id
#	- prop_latitude(float) --> latitude
#	- prop_longitude(float) --> longitude

# RELACIONES: rails
#	- STFIPS1(int): Weight between 2 stations

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
