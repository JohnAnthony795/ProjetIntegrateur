import requests, json

from neo4jdb import Neo4jDB
from flask import Flask, request, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
neo4jdb = Neo4jDB()


kml_template = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Path</name>
    <description></description>
    <Style id="yellowLine">
      <LineStyle>
        <color>7f00ffff</color>
        <width>5</width>
      </LineStyle>
    </Style>
    <Placemark>
      <name>Route</name>
      <description>Route calculated</description>
      <styleUrl>#yellowLine</styleUrl>
      <LineString>
        <coordinates> 
			{{coords}}
        </coordinates>
      </LineString>
    </Placemark>
	<Placemark>
		<name>Departure</name>
		<description>Chosen departure point</description>
		<Point>
		  <coordinates>{{departure}},0</coordinates>
		</Point>
	</Placemark>
	<Placemark>
		<name>Destination</name>
		<description>Chosen destination point</description>
		<Point>
		  <coordinates>{{destination}},0</coordinates>
		</Point>
	</Placemark>
  </Document>
</kml>
"""

def calc_route(dx,dy,ax,ay):
	startNode = neo4jdb.getId(dx,dy)
	endNode = neo4jdb.getId(ax,ay)

	url = 'http://neo4j:pass@localhost:7474/db/data/node/%s/path' % (startNode)
	data = '{"to":"http://localhost:7474/db/data/node/%s", "cost_property":"distance", "relationships": {"type":"ISLINKED", "direction":"all"}, "algorithm":"dijkstra"}' % (endNode)

	response = requests.post(url, data=data)

	nodesPath = json.loads(response.text)['nodes']
	fullpath = ""
	for node in nodesPath:
		nodeid = node.rpartition('/')[2]
		fullpath += neo4jdb.getLongLat(nodeid) + ',0\n'

	return fullpath[:-1]


class GetRoute(Resource):
	def get(self,dx,dy,ax,ay):
		dx,dy,ax,ay=float(dx), float(dy), float(ax), float(ay)
		return {'route': calc_route(dx,dy,ax,ay).split("\n")}

class GetRouteKML(Resource):
	def get(self,dx,dy,ax,ay):
		dx,dy,ax,ay=float(dx), float(dy), float(ax), float(ay)
		response = make_response(kml_template.replace("{{coords}}", calc_route(dx,dy,ax,ay)).replace("{{departure}}", str(dy)+","+str(dx)).replace("{{destination}}", str(ay)+","+str(ax)))
		response.headers['content-type'] = 'application/vnd.google-earth.kml+xml'
		response.headers['content-disposition'] = 'attachment; filename="route.kml"'
		return response

api.add_resource(GetRoute, '/route/<string:dx>/<string:dy>/<string:ax>/<string:ay>/data', '/route/<string:dx>/<string:dy>/<string:ax>/<string:ay>')
api.add_resource(GetRouteKML, '/route/<string:dx>/<string:dy>/<string:ax>/<string:ay>/kml')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
