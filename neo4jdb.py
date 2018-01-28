import json
from neo4j.v1 import GraphDatabase

class Neo4jDB:
	_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "pass"))

	def __init__(self):
		self._driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "pass"))

	def close(self):
		self._driver.close()

	def getSuccessorsOf(self,nodeLon, nodeLat):
		successors = []
		with self._driver.session() as session:
			with session.read_transaction() as tx:
				for record in tx.run('MATCH (a:Pixel{long:"{lon}", lat:"{lat}"})-[distance:ISLINKED]-(b:Pixel) RETURN b, distance', lon=nodeLon, lat=nodeLat):
					props = record["b"].properties
					successors.append((Node(props["long"], props["lat"], props["density"]), record["distance"].properties["distance"]))
		return successors

	def getLongLat(self, nodeId):
		with self._driver.session() as session:
			result = session.run('MATCH (a:Pixel) WHERE ID(a) = {nodeId} RETURN a', nodeId=int(nodeId)).single()["a"]
			return result.properties["long"] + ',' + result.properties["lat"]

	def getId(self, nodeLat, nodeLong):
		with self._driver.session() as session:
			return session.run("MATCH (a:Pixel {lat:{latitude}, long:{longitude}}) RETURN ID(a)", {"latitude": str(nodeLat), "longitude": str(nodeLong)}).single()[0]

