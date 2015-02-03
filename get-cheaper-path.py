"""
Get shortest weighted path between 2 nodes in the graphdb Train stations of US attached
"""

# NODES: Train stations
#	- prop_node_id(int) --> Id
#	- prop_latitude(float) --> latitude
#	- prop_longitude(float) --> longitude

# RELATIONSHIPS: rails
#	- STFIPS1(int): Weight between 2 stations

import sys, re
from neo4jrestclient.client import GraphDatabase

db = GraphDatabase("http://localhost:7474/db/data/")

################ CHECK INPUT PARAMETERS #####################

if len(sys.argv) != 3:
	raise Exception('Input 2 stations')

for i in sys.argv[1:]:
	try:
		int(i)
	except Exception:
		raise Exception('Only integers values are allowed')

################ START #####################

#Constants
id_start = int(sys.argv[1])
id_end = int(sys.argv[2])

#Checking nodes exist in neo4jDB
try:
 	start_Station = db.nodes[id_start]
 	end_Station = db.nodes[id_end]
except (Exception):
	raise Exception('At least 1 node doesnt exist in the neo4jDB')

################ QUERY DB ############################

q = """
MATCH paths = allShortestPaths((n { prop_node_id : {start_id} })-[*]-(m { prop_node_id: {end_id} }))
WITH REDUCE(dist = 0, rel in rels(paths) | dist + toInt(rel.STFIPS1)) AS distance, paths
RETURN paths, distance
ORDER BY distance
LIMIT 1
"""
result = db.query(q, params={"start_id": id_start, "end_id": id_end})

################ RESULT ###########################

if len(result) == 0:
	print "There is no path"
else:
	path = [re.search(r'\d+$', node).group(0) for node in result[0][0]['nodes']]
	print "Cheaper path: {path}".format(path = '-'.join(path))
